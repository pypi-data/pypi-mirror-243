"""pyaslengine.patch.resources"""


def resource_patch(func):
    def wrapper(*args, **kwargs):
        # TODO...
        return func(*args, **kwargs)

    return wrapper
