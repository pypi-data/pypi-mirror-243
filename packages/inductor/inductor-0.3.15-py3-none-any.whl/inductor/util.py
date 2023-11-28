# Copyright 2023 Inductor, Inc.
"""Inductor utility functions."""

import os
from typing import Callable


def get_module_qualname(f: Callable) -> str:
    """Return the fully qualified name of the module in which f is defined.

    Args:
        f: A function, class, or method.

    Returns:
        The fully qualified name of the module in which f is defined. If f is
        defined in the __main__ module, then the name of the file containing f
        (without its ".py" extension) is returned as the fully qualified module
        name. If f is defined in a Google Colab notebook, then "google_colab" is
        returned as the fully qualified module name.

    Raises:
        RuntimeError if f is defined in the __main__ module, the current
        environment is not Google Colab, and the name of the file
        containing f does not end with ".py".
    """
    qualname = f.__module__
    if qualname == "__main__":
        # Special case for Google Colab.
        try:
            import google.colab
            return "google_colab"
        except ImportError:
            pass

        qualname, ext = os.path.splitext(
            os.path.basename(f.__globals__["__file__"]))
        if ext != ".py":
            raise RuntimeError(
                f"f ({f.__qualname__}) is defined in the __main__ module but "
                f"is contained in a file ({f.__globals__['__file__']}) that "
                "does not have extension '.py'.")
    return qualname
