# !/usr/bin/python3
# -*- coding: utf-8 -*-

import sys


CMD_MAP = {
    'I': 'create',
    'C': 'clear',
    'L': 'draw_pixel',
    'V': 'draw_vertical_line',
    'H': 'draw_horizontal_line',
    'K': 'draw_rectangle',
    'F': 'fill_region',
    'S': 'save_image',
    'X': 'exit'
}


class Matrix():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.data = [[]] * height
        for h in range(height):
            self.data[h] = ['O'] * width

    def clear(self):
        pass

    def __repr__(self):
        output = []
        for h in range(self.height):
            output.append(', '.join(self.data[h]))
        return '\n'.join(output)


class Context():
    def __init__(self, cls):
        self.cls = cls
        self.instance = None

    def create(self, *params):
        self.instance = self.cls(*params)

    def exit(self):
        self.instance = None

    def get_function(self, cmd_alias):
        cmd_name = CMD_MAP[cmd_alias.upper()]
        if hasattr(self, cmd_name):
            return getattr(self, cmd_name)
        if not self.instance:
            raise ValueError('Instance not initialized')
        return getattr(self.instance, cmd_name)


def parse_command(expr):
    '''
    Expect a command expression (str)
        Example: "A 4 6"
    Return a tuple with the command name and the params (tuple)
        Example: ('A', [4, 6]) or ('A', ['test.bmp'])
    '''
    def clean(param):
        try:
            return int(param)
        except ValueError:
            return param

    try:
        cmd_alias, params = expr.split(maxsplit=1)
    except ValueError:
        cmd_alias, params = expr, ''
    params = [clean(x) for x in params.split()]
    return cmd_alias, params


def read_input(filename):
    '''
    Expect a string filename (str)
    Return the sanitized file contents in lines (list)
    '''
    with open(filename) as f:
        return [x.strip() for x in f.readlines() if x.strip()]


def main(command_list):
    '''
    Expect a list of input commands (list)
    '''
    context = Context(Matrix)
    for expr in command_list:
        cmd_alias, params = parse_command(expr)
        if cmd_alias not in CMD_MAP.keys():
            continue
        func = context.get_function(cmd_alias)
        func(params)


if __name__ == '__main__':
    try:
        filename = sys.argv[1]
    except IndexError:
        sys.exit('Expected a input file.')

    try:
        command_lines = read_input(filename)
    except IOError:
        sys.exit('File {!r} not found.'.format(filename))

    main(command_lines)
