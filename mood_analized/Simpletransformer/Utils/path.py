import sys
import os
import platform

OS: str = platform.system()

def is_in_virtual_environment() -> bool:
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

def get_pip_path() -> str:
    if not is_in_virtual_environment():
        return "pip"
    
    script_dir: str = os.path.dirname(os.path.abspath(sys.argv[0]))
    script_dir: str = os.path.dirname(script_dir)
    
    if OS == "Windows":
        return os.path.join(script_dir, "Scripts", "pip3.exe")
    elif OS == "linux":
        return os.path.join(script_dir, "bin", "pip")
    