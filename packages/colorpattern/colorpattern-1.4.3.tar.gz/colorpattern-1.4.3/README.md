# ColorPattern

![PyPI](https://img.shields.io/pypi/v/colorpattern) ![PyPI - Downloads](https://img.shields.io/pypi/dm/colorpattern??color=%2360EE59)
 ![Total Downloads](https://static.pepy.tech/badge/colorpattern)

ColorPattern is a Python module designed for enhancing text output in the console by applying color to specific patterns. It offers a flexible way to define patterns and apply different text colors, background colors, styles, underlines and other options to predefined patterns.

Use regular expressions to define the pattern to color. With the color pattern initialized, any console output that matches the pattern will have the defined styles applied to it.

Since Version 1.4.1 can strikethrough, blink text and italic text

## Installation

You can install ColorPattern using pip:

```pip install colorpattern ```


## Usage

Set the patterns whith SetPatterns(<pattern>, <options>)

Use ```start_color(<patterns>)``` for initialize the color print, and ```end_color()``` for stop colorization.

### Example

```python
from colorpattern.colorpattern import *

def main():
    # Define your color patterns
    pattern1 = SetPattern(r'\d+', color=Fore.GREEN)
    pattern2 = SetPattern(r'Colorpattern', color=Fore.LIGHTRED_EX, underline=True)
    pattern3 = SetPattern(r'Croketillo', color=Fore.BLACK, back=Back.LIGHTWHITE_EX, style=Style.BRIGHT)
    email = SetPattern(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', color=Fore.BLUE)
    strike= SetPattern(r'NEW!!!', strikethrough=True)
    blink=SetPattern(r'BLINK', blink=True)
    italic=SetPattern(r'ITALIC TEXT', italic=True)

    # Initialize colorization and get the original print function and applied patterns
    print("\nSTART COLORIZED PRINT")
    print('-----------------------')
    start_color([pattern1, pattern2, pattern3, email, strike, italic,blink])

    # Use the custom print function with colorization
    print('Colorpattern v1.4.2')
    print('By Croketillo - croketillo@gmail.com')
    print('NEW!!! - NOW YOU CAN INCLUDE STRIKETHROUGH IN PATTERNS')
    print('This is a BLINK and ITALIC TEXT test')

    # End colorization and restore the original print function
    end_color()
    print("\nNORMAL PRINT")
    # Now, printing returns to normal

    print('-----------------------')
    print('Colorpattern v1.4.2')
    print('By Croketillo - croketillo@gmail.com')
    print('NEW!!! - NOW YOU CAN INCLUDE STRIKETHROUGH IN PATTERNS')
    print('This is a BLINK and ITALIC TEXT test')

    # You can re-enable colorization with new patterns if necessary
    new_pattern = SetPattern(r'new pattern', color=Fore.LIGHTCYAN_EX)

    # Use the custom print function with new patterns
    print("\nSTART COLORIZED PRINT AGAIN")
    start_color([pattern1, new_pattern])

    print('-----------------------')
    print('This is a new pattern. 123456')

    # End colorization and restore the original print function
    end_color()
    print("\nNORMAL PRINT AGAIN")
    # Now, printing returns to normal even with the new patterns
    print('-----------------------')
    print('This is a normal message again. 12345')

if __name__ == "__main__":
    main()
```

## Patterns

- `pattern`: Regular expression pattern to match in the text.
- `color`: Text color (e.g., 'green', 'red', 'yellow').
- `back`: Background color (e.g., 'black', 'blue', 'white').
- `style`: Text style (e.g., 'bright', 'dim', 'reset_all').
- `underline`: Set to `True` for underlining matched text.
-  `strike`: Set to `True` for strikethrough matched text.
-  `blink`: Set to `True` for blink matched text.
-  `italic`: Set to `True` for italic matched text.


## Colors (colorama):

### Text Colors (Fore):
- Fore.BLACK
- Fore.RED
- Fore.GREEN
- Fore.YELLOW
- Fore.BLUE
- Fore.MAGENTA
- Fore.CYAN
- Fore.WHITE
- Fore.LIGHTBLACK_EX
- Fore.LIGHTRED_EX
- Fore.LIGHTGREEN_EX
- Fore.LIGHTYELLOW_EX
- Fore.LIGHTBLUE_EX
- Fore.LIGHTMAGENTA_EX
- Fore.LIGHTCYAN_EX
- Fore.LIGHTWHITE_EX
- Fore.RESET

### Background Colors (Back):
- Back.BLACK
- Back.RED
- Back.GREEN
- Back.YELLOW
- Back.BLUE
- Back.MAGENTA
- Back.CYAN
- Back.WHITE
- Back.LIGHTBLACK_EX
- Back.LIGHTRED_EX
- Back.LIGHTGREEN_EX
- Back.LIGHTYELLOW_EX
- Back.LIGHTBLUE_EX
- Back.LIGHTMAGENTA_EX
- Back.LIGHTCYAN_EX
- Back.LIGHTWHITE_EX
- Back.RESET

### Text Styles (Style):
- Style.RESET_ALL
- Style.BRIGHT 
- Style.DIM 
- Style.NORMAL 

## License

This project is licensed under the GNU-GLP,3 License - see the LICENSE file for details.
