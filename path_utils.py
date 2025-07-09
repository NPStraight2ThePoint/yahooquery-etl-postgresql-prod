import sys
import os

def set_repo_root():
    """
    Ensures the repository root is added to sys.path
    so internal imports work regardless of script location.
    """
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if root_dir not in sys.path:
        sys.path.insert(0, root_dir)