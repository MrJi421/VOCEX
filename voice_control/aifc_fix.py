"""
Fix for missing aifc module in Python 3.13
"""

import sys
import os

# Add aifc module to sys.modules if it doesn't exist
if 'aifc' not in sys.modules:
    # Create a simple aifc module stub
    class AifcModule:
        def __init__(self):
            pass
        
        def open(self, *args, **kwargs):
            raise NotImplementedError("aifc module not fully implemented")
    
    sys.modules['aifc'] = AifcModule() 