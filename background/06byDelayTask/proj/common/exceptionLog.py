import wrapt
import time
from common.log import init_logger, logger
from logging import Logger


def excepition_noparams(func):
    def wrapper(*args, **kwargs):
        customer_logger = init_logger()
        try:
            return func(*args, **kwargs)
        except:
            err = ""
            err += func.__name__
            customer_logger.exception(err)
        #raise

    return wrapper


def exception_containsparams(customer_logger):
    '''
        注意此种凡是无法在类方法上使用
    @param logger:
    @return:
    '''

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                err = ''
                err += func.__name__
                customer_logger.exception(err)

            # raise

        return wrapper

    return decorator


def exception(customer_logger: Logger):
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        try:
            return wrapped(*args, **kwargs)
        except:
            err = ''
            err += wrapped.__name__
            if isinstance(customer_logger, Logger):
                customer_logger.exception(err)
        # raise

    return wrapper



