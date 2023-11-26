""" 
This file is (or part of) COLORPATTERN v1.4.1
Copyright 2023- Croketillo <croketillo@gmail.com> https://github.com/croketillo
 
DESCIPTION:
Effortless console text colorization based on user-defined patterns in Python.

                        LICENSE -   GNU GPL-3

This software is protected by the GNU General Public License version 3 (GNU GPL-3).
You are free to use, modify, and redistribute this software in accordance with the 
terms of the GNU GPL-3. You can find a copy of the license at the following link: 
https://www.gnu.org/licenses/gpl-3.0.html.

This software is provided as-is, without any warranties, whether express or implied. 
Under no circumstances shall the authors or copyright holders be liable for any claims, 
damages, or liabilities arising in connection with the use of this software.
If you make modifications to this software and redistribute it, you must comply with 
the terms of the GNU GPL-3, which includes the obligation to provide the source code 
for your modifications. Additionally, any derived software must also be under the 
GNU GPL-3.

For more information about the GNU GPL-3 and its terms, please carefully read the full
license or visit https://www.gnu.org/licenses/gpl-3.0.html
"""

import re
import builtins
from colorama import Fore, Style, Back


class SetPattern:
    def __init__(self, pattern,
                color=None,
                back=None,
                style=None,
                underline=False,
                strikethrough=False,
                italic=False,
                blink=False):
        # Compile the regular expression pattern
        self.pattern = re.compile(pattern)
        # Set default values for color, background, style, underline,
        # strikethrough, italic, and blink
        self.color = color if color is not None else Fore.RESET
        self.back = back if back is not None else Back.RESET
        self.style = style if style is not None else Style.RESET_ALL
        self.underline = underline
        self.strikethrough = strikethrough
        self.italic = italic
        self.blink = blink

    def colorize_text(self, text):
        # Apply color, background, style, underline, strikethrough,
        # italic, and blink to matched text
        format_str = f"{self.style}{self.color}{self.back}"
        if self.underline:
            format_str += "\033[4m"
        if self.strikethrough:
            format_str += "\033[9m"
        if self.italic:
            format_str += "\033[3m"
        if self.blink:
            format_str += "\033[5m"

        return self.pattern.sub(lambda match: f"{format_str}{match.group()}{Style.RESET_ALL}", text)

# Function to initialize colorization
def start_color(patterns):
    def custom_print(*args, **kwargs):
        # Convert print arguments to a string
        text = " ".join(map(str, args))

        # Apply colorization to the text
        for pattern in patterns:
            text = pattern.colorize_text(text)

        # Print the colorized text
        original_print(text, **kwargs)

    # Replace the print function with the custom version
    original_print = builtins.print
    builtins.print = custom_print

    return original_print  # Return the original print function


# Function to end colorization and restore the original print function
def end_color():
    # Restore the original print function
    builtins.print = builtins.__original_print__

# Save the original print function
builtins.__original_print__ = builtins.print
