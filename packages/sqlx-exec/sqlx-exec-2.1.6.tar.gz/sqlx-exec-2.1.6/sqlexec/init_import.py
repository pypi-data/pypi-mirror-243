import importlib
from .engine import Engine
from .support import DBError
from .log_support import logger
from .constant import DRIVERS, PARAM_PORT, MYSQL, POSTGRESQL, UNKNOW, MYSQL_PORT, POSTGRESQL_PORT, SQLITE


def import_driver(driver, curr_engine):
    creator = None
    if driver:
        if driver not in DRIVERS:
            logger.warning(f"Driver '{driver}' not support now, may be you should adapte it youself.")
        engine = DRIVERS.get(driver)
        creator = do_import(driver, engine)
        engine = engine if engine else curr_engine
    else:
        drivers = dict(filter(lambda x: x[1] == curr_engine, DRIVERS.items())) if curr_engine and curr_engine != UNKNOW else DRIVERS
        for driver, engine in drivers.items():
            try:
                creator = importlib.import_module(driver)
                break
            except ModuleNotFoundError:
                pass
        if not creator:
            raise DBError(f"You may forgot install driver, may be one of {list(DRIVERS.keys())} suit you.")
    return engine, driver, creator


def do_import(driver, Engine):
    try:
        return importlib.import_module(driver)
    except ModuleNotFoundError:
        raise DBError(f"Import {Engine} driver '{driver}' failed, please sure it was installed or change other driver.")


def get_engine(driver: str, *args, **kwargs):
    curr_engine = Engine.current_engine()
    if driver is None and (curr_engine is None or curr_engine == UNKNOW):
        if args and isinstance(args[0], str):
            if 'mysql://' in args[0]:
                return MYSQL
            elif 'postgres://' in args[0]:
                return POSTGRESQL
            elif '://' not in args[0]:
                return SQLITE
        elif  PARAM_PORT in kwargs:
            port = kwargs[PARAM_PORT]
            if port == MYSQL_PORT:
                return MYSQL
            elif port == POSTGRESQL_PORT:
                return POSTGRESQL
    return curr_engine
