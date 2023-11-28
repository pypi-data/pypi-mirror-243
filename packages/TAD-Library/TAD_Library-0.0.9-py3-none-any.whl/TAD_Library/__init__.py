# __init__.py
# Copyright (C) 2022 (yhkim@chakoon.com) and contributors
#
import inspect
import os
import sys

__version__ = '0.0.9'

real_path = os.path.dirname(os.path.abspath(__file__)).replace("\\","/")
sys.path.append(real_path)

try:
    from .Common import *
except ImportError as e:
    print(e,"import fail")


__all__ = [name for name, obj in locals().items()
           if not (name.startswith('_') or inspect.ismodule(obj))]

#__all__ = ['TAD_Library']
