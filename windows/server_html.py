# -*- coding: utf-8 -*-
"""
Re-export templates for Windows 11 Classroom Server
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from student_html import STUDENT_HTML
from teacher_html import TEACHER_HTML

__all__ = ["STUDENT_HTML", "TEACHER_HTML"]
