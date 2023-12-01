#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Jae-Joon Lee.
# Distributed under the terms of the Modified BSD License.

# Must import __version__ first to avoid errors importing this file during the build process.
# See https://github.com/pypa/setuptools/issues/1724#issuecomment-627241822
from ._version import __version__

__all__ = ["mpl2skia", "skia2mpl", "union", "intersection", "difference", "xor",
           "PathOpsPathEffect",
           "PathOps", "PathOpsFromFunc", "PathOpsFromPatch", "PathOpsFromPath"]

from .mpl_skia_pathops import mpl2skia, skia2mpl, union, intersection, difference, xor
from .mpl_pe_pathops import (PathOpsPathEffect,
                             PathOps, PathOpsFromFunc, PathOpsFromPatch, PathOpsFromPath)
