# -*- coding: utf-8 -*-
"""
System Service Application
"""

import sys
import os

# 娣诲姞backend鐩綍鍒癙ython璺緞
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)
