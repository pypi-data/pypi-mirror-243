from .exceptions import length_value_too_long

#### Function to check the specified length
def length_check(length, ignore_max_length=True):

    #### Set max length var
    default_max_length = 1000

    #### Skip only when needed
    if not ignore_max_length:
        if length > default_max_length:
            raise length_value_too_long(default_max_length)