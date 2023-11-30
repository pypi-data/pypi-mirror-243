import os
import glob
import json
import pkgutil

import astrohack
import functools

import skriba.messenger
import skriba.logger

from inspect import getfullargspec
from auror.protego import Protego


def validate(config_dir=None, custom_checker=None, add_data_type=None, logger=None):
    def function_wrapper(function):
        arguments = {}

        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            arg_list = getfullargspec(function).args

            if kwargs:
                for key, value in kwargs.items():
                    arguments[key] = value
                    index = arg_list.index(key)
                    arg_list.pop(index)

            if args:
                for arg in arg_list:
                    index = arg_list.index(arg)
                    arguments[arg] = args[index]

            verify(
                function=function,
                args=arguments,
                config_dir=config_dir,
                custom_checker=custom_checker,
                add_data_type=add_data_type,
                logger=logger
            )

            return function(*args, **kwargs)

        return wrapper

    return function_wrapper


def config_search(root="/"):
    logger = skriba.logger.get_logger(logger_name="AUROR-LOG")

    paths = []
    if root == "/":
        logger.info("[{warning}] File search from root could take some time ...".format(
            warning=skriba.messenger.SystemMessage.yellow("Warning!")))

    logger.info("Searching fileSystemMessage for configuration files, please wait ...")
    for file in glob.iglob("{root}/**".format(root=root), recursive=True):
        logger.info(file)
        if "param.json" in file:
            basename = os.path.dirname(file)
            if basename not in paths:
                paths.append(basename)

    logger.info(paths)

    return paths


def set_config_directory(path, create=False):
    logger = skriba.logger.get_logger(logger_name="AUROR-LOG")

    if os.path.exists(path):
        logger.info("Setting configuration directory to [{path}]".format(path=path))
        os.environ["AUROR_CONFIG_PATH"] = path
    else:
        logger.info("The configuration directory [{path}] does not currently exist.".format(path=path))
        if create:
            logger.info("Creating empty configuration directory: {path}".format(path=path))
            os.mkdir(path)


def verify_configuration(path, module):
    logger = skriba.logger.get_logger("AUROR-LOG")

    modules = []
    for file in glob.glob("{path}/*.param.json".format(path=path), recursive=True):
        if file.endswith(".param.json"):
            modules.append(os.path.basename(file).strip(".param.json"))

    package_path = os.path.dirname(module.__file__)
    package_modules = [name for _, name, _ in pkgutil.iter_modules([package_path])]

    not_found = []
    for module in package_modules:
        if module not in modules:
            not_found.append(module)

    coverage = (len(package_modules) - len(not_found)) / len(package_modules)

    logger.debug("The following functions were not found: {not_found}".format(not_found=not_found))
    logger.debug("The parameter checking coverage is: {coverage}%".format(coverage=100 * coverage))

    return package_modules


def verify(function, args, config_dir=None, add_data_type=None, custom_checker=None, logger=None):
    function_name = function.__name__
    module_name = function.__module__

    if logger is None:
        logger = skriba.logger.get_logger(
            logger_name="AUROR-LOG"
        )

    # The module call gives the full module chain, but we only want the last
    # module, ex. astrohack.extract_holog would be returned, but we only want
    # extract_holog. This should generally work.

    module_name = module_name.split(".")[-1]

    logger.info(
        "{function}: Checking parameter values for {module}".format(function=function_name, module=module_name))

    logger.info("MODULE CONFIG: ", os.getenv("AUROR_CONFIG_PATH"))
    logger.info("config_dir: ", config_dir)

    # First we need to find the parameter configuration files
    if config_dir is not None:
        path = config_dir

    # If the parameter configuration directory is not passed as an argument this environment variable should be set.
    # In this case, the environment variable is set in the __init__ file of the astrohack module.
    elif os.getenv("AUROR_CONFIG_PATH"):
        path = os.getenv("AUROR_CONFIG_PATH")
        logger.debug("AUROR_CONFIG_PATH: {dir}".format(dir=os.getenv("AUROR_CONFIG_PATH")))

    else:
        logger.error("{function}: Cannot find parameter configuration directory.".format(function=function_name))
        assert False

    # Define parameter file name
    parameter_file = module_name + ".param.json"

    logger.debug(path + "/" + parameter_file)

    # This will check the configuration path and return the available modules
    module_config_list = verify_configuration(path, astrohack)

    # Make sure that required module is present
    if module_name not in module_config_list:
        logger.error("{function}: Parameter file not found in {path}".format(
            function=function_name, path=path + "/" + parameter_file
        ))

        raise FileNotFoundError

    with open(path + "/" + parameter_file) as json_file:
        schema = json.load(json_file)

    if function_name not in schema.keys():
        logger.error("Function [{function}] {not_found} in parameter configuration files.".format(
            function=function_name, not_found=skriba.messenger.SystemMessage.red("not found")))

        raise KeyError

    # Here is where the parameter checking is done
    # First instantiate the validator.
    validator = Protego()

    if add_data_type is not None:
        validator.register_data_type(add_data_type)

    logger.debug(schema)
    # Set up the schema to validate against.
    validator.schema = schema[function_name]

    # If a custom unit custom checker is needed, instantiate the
    # void function in the validator class. In the schema this
    # is used with "check allowed with".
    if custom_checker is not None:
        validator.custom_allowed_function = custom_checker

    assert validator.validate(args), logger.error(validator.errors)
