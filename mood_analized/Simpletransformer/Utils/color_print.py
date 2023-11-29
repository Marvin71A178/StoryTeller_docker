class Color:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
def cprint(color: Color, *values: object, end: str | None = "\n") -> None:
    """
    Colorful print

    Params:
        color: the color want to print
        *values: objects want to print
        end: end line, default is '\\n' 
    
    Return:
        None
    """
    result: str = "".join(str(value) for value in values)
    
    print(color, result, Color.ENDC, end=end)

def process_print(*values: object, end: str | None = "\n") -> None:
    """
    """
    cprint(Color.CYAN, *values, end=end)

def ok_print(*values: object, end: str | None = "\n") -> None:
    """
    """
    cprint(Color.GREEN, *values, end=end)

def head_print(*values: object, end: str | None = "\n") -> None:
    """
    """
    cprint(Color.HEADER, *values, end=end)

def error_print(*values: object, end: str | None = "\n") -> None:
    """
    """
    cprint(Color.FAIL, *values, end=end)
    
def warning_print(*values: object, end: str | None = "\n") -> None:
    """
    """
    cprint(Color.WARNING, *values, end=end)   