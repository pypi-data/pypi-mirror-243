#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Jae-Joon Lee.
# Distributed under the terms of the Modified BSD License.

# Must import __version__ first to avoid errors importing this file during the build process.
# See https://github.com/pypa/setuptools/issues/1724#issuecomment-627241822
from ._version import __version__

__all__ = ["AnnotationMergedPatch", "AnnotationBubble",
           "annotate_bubble", "annotate_merged", "BubbleConnectionStyle"]

from .speech_bubble import (AnnotationMergedPatch, AnnotationBubble,
                            annotate_bubble, annotate_merged)

from . import boxstyle # this will register fixed_circle and fixed_square as a boxstyle.
from .connectionstyle  import Bubble as BubbleConnectionStyle
