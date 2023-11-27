#https://en.wikipedia.org/wiki/ANSI_escape_code

from .styling import Styling
from .Color import Color
from .Console import Console
from .Style import Style
from .Color_Background import Background
from .Color_Text import Text

__all__ = ['Styling', 'Color', 'Style', 'Console']

try:
    import sys, os, platform

    from pkg_resources import get_distribution
    try:
        import requests
        version = get_distribution("chromaconsole").version
        latest_version = requests.get(f'https://pypi.org/pypi/chromaconsole/json').json()['info']['version']
        if version != latest_version:
            os.system("pip install chromaconsole -U")
    except:
        pass

    def FixWinConsoleColors():
        if platform.system() == "Windows" and sys.stdout and hasattr(sys.stdout, "fileno"):
            try:
                import ctypes
                ctypes.windll.kernel32.SetConsoleMode(ctypes.windll.kernel32.GetStdHandle(-11), 7)
            except Exception:
                pass

    FixWinConsoleColors()
except:
    pass