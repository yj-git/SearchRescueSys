import wrapt
import logging

def get_err():
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):

        return wrapped(*args, **kwargs)

    return wrapper



