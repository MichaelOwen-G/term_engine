
from abc import ABC


class ParsTypeSensitivity(ABC):
    def __init__(self, parent: str, arguments: list[tuple]):
        ''' Receives tuples as arguments
            - tuples contain 3: an parameter name, object and a type that the object will be validated against
        '''
        # the name of the parent class
        self._par_cls_nm: str = parent

        self._validate_args('', arguments)

    def _validate_args(self, method, arguments):
        # iterate through the given args
        for arg in arguments:
            # validate that the arg is indeed a tuple
            # throw error if not
            if not isinstance(arg, tuple): self._raise_error(self.__name__(), arg, tuple)

            # validating the arg type
            the_arg_name = arg[0]
            the_arg = arg[1]
            the_arg_type = arg[2]

            if not isinstance(the_arg, the_arg_type): self._raise_error(method, the_arg_name, the_arg, the_arg_type)


    def _raise_error(self, method: str, arg_name, arg, arg_type):
        raise TypeError(f"{self._par_cls_nm}.{method} received bad argument. Parameter {arg_name} accepts only type {arg_type}, instead type {arg.__class__.__name__} was given") 