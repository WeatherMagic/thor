#!/usr/bin/env python3
import sys


class _const:
    """
    Purpose: Provide variables which cannot be
    reset once they've been assigned a value.

    example:
        a = 10
        a = 11 # This will throw an exception
    """
    class ConstError(TypeError):
        pass

    def __setattr__(self, name, value):
        # If const.name exists
        if name in self.__dict__:
            # Throw exception
            raise self.ConstError("Can't rebind const(%s)" % name)
        self.__dict__[name] = value

sys.modules[__name__] = _const()
