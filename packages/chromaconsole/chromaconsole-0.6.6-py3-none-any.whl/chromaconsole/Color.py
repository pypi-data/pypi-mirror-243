from .styling import Styling
from .Color_Background import Background as background
from .Color_Text import Text as text

class Color:
    class Text:
        '''
        Set foreground [color](https://en.wikipedia.org/wiki/ANSI_escape_code#3-bit_and_4-bit)
        '''
        black = staticmethod(text.black)
        red = staticmethod(text.red)
        green = staticmethod(text.green)
        yellow = staticmethod(text.yellow)
        blue = staticmethod(text.blue)
        magenta = staticmethod(text.magenta)
        cyan = staticmethod(text.cyan)
        white = staticmethod(text.white)
        br_black = staticmethod(text.br_black)
        br_red = staticmethod(text.br_red)
        br_green = staticmethod(text.br_green)
        br_yellow = staticmethod(text.br_yellow)
        br_blue = staticmethod(text.br_blue)
        br_magenta = staticmethod(text.br_magenta)
        br_cyan = staticmethod(text.br_cyan)
        br_white = staticmethod(text.br_white)
    class Background:
        '''
        Set background [color](https://en.wikipedia.org/wiki/ANSI_escape_code#3-bit_and_4-bit)
        '''
        black = staticmethod(background.black)
        red = staticmethod(background.red)
        green = staticmethod(background.green)
        yellow = staticmethod(background.yellow)
        blue = staticmethod(background.blue)
        magenta = staticmethod(background.magenta)
        cyan = staticmethod(background.cyan)
        white = staticmethod(background.white)
        br_black = staticmethod(background.br_black)
        br_red = staticmethod(background.br_red)
        br_green = staticmethod(background.br_green)
        br_yellow = staticmethod(background.br_yellow)
        br_blue = staticmethod(background.br_blue)
        br_magenta = staticmethod(background.br_magenta)
        br_cyan = staticmethod(background.br_cyan)
        br_white = staticmethod(background.br_white)

    @staticmethod
    def text(*args): #38;2;r;g;bm
        '''
        changes the color of the text\n
        Color.text(r, g, b)\n
        Color.text("#rrggbb")
        '''
        if Styling.is_enabled():
            if len(args) == 1:
                color = args[0].lstrip("#")
                if len(color) == 3:
                    r, g, b = (int(c * 2, 16) for c in color)
                elif len(color) == 6:
                    r, g, b = (int(color[i:i+2], 16) for i in range(0, 6, 2))
                else:
                    raise ValueError("Invalid color format")
            elif len(args) == 3:
                r, g, b = args
            else:
                raise ValueError("Invalid number of arguments")

            return f"\033[38;2;{r};{g};{b}m"
        else:
            return ""
        
    @staticmethod
    def text_gradient(text, start_color, end_color):
        '''
        this can be used to make text gradient\n
        text_gradient(str, (r,g,b) or "#rrggbb" , (r,g,b) or "#rrggbb")
        '''
        gradient_text = ""

        def interpolate_color(start_color, end_color, factor):
            interpolated_color = tuple(
                int(start + (end - start) * factor)
                for start, end in zip(start_color, end_color)
            )
            return interpolated_color

        def parse_color(color):
            if isinstance(color, str):
                if color.startswith("#"):
                    color = color.lstrip("#")
                if len(color) == 3:
                    color = ''.join(c * 2 for c in color)
                if len(color) != 6:
                    raise ValueError("Invalid color format")
                return (
                    int(color[0:2], 16),
                    int(color[2:4], 16),
                    int(color[4:6], 16)
                )
            return color

        start_color = parse_color(start_color)
        end_color = parse_color(end_color)

        # Compute interpolation steps
        interpolation_step = 1 / (len(text) - 1)
        for i, char in enumerate(text):
            factor = i * interpolation_step
            interpolated_color = interpolate_color(start_color, end_color, factor)
            gradient_text += Color.text(*interpolated_color) + char

        return gradient_text + "\033[39m"
        
    @staticmethod
    def default_text(): #39m
        '''
        Default foreground color\n
        Implementation defined (according to standard)
        '''
        return "\033[39m" if Styling.is_enabled() else ""
    
    @staticmethod
    def background(*args): #48;2;r;g;bm
        '''
        changes the color of the text background\n
        Color.background(r, g, b)\n
        Color.background("#rrggbb")
        '''
        if Styling.is_enabled():
            if len(args) == 1:
                color = args[0].lstrip("#")
                if len(color) == 3:
                    r, g, b = (int(c * 2, 16) for c in color)
                elif len(color) == 6:
                    r, g, b = (int(color[i:i+2], 16) for i in range(0, 6, 2))
                else:
                    raise ValueError("Invalid color format")
            elif len(args) == 3:
                r, g, b = args
            else:
                raise ValueError("Invalid number of arguments")

            return f"\033[48;2;{r};{g};{b}m"
        else:
            return ""
        
    @staticmethod
    def background_gradient(text, start_color, end_color):
        '''
        this can be used to make background gradient\n
        background_gradient(str, (r,g,b) or "#rrggbb" , (r,g,b) or "#rrggbb")
        '''
        gradient_text = ""

        def interpolate_color(start_color, end_color, factor):
            interpolated_color = tuple(
                int(start + (end - start) * factor)
                for start, end in zip(start_color, end_color)
            )
            return interpolated_color

        def parse_color(color):
            if isinstance(color, str):
                if color.startswith("#"):
                    color = color.lstrip("#")
                if len(color) == 3:
                    color = ''.join(c * 2 for c in color)
                if len(color) != 6:
                    raise ValueError("Invalid color format")
                return (
                    int(color[0:2], 16),
                    int(color[2:4], 16),
                    int(color[4:6], 16)
                )
            return color

        start_color = parse_color(start_color)
        end_color = parse_color(end_color)

        # Compute interpolation steps
        interpolation_step = 1 / (len(text) - 1)
        for i, char in enumerate(text):
            factor = i * interpolation_step
            interpolated_color = interpolate_color(start_color, end_color, factor)
            gradient_text += Color.background(*interpolated_color) + char

        return gradient_text + "\033[49m"
    
    @staticmethod
    def default_background(): #49m
        '''
        Default background color\n
        Implementation defined (according to standard)
        '''
        return "\033[49m" if Styling.is_enabled() else ""