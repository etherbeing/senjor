import logging


def argument(*args, **kwargs):
    def wrapper(param):
        logging.info("Params %s %s", args, kwargs)
        return param