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

    def __eq__(self, value):
        return self.data == value

    def draw_rectangle(self, x0, y0, x1, y1, color):
        if x1 < x0 or y1 < y0:
            return
        for y in range(y0, y1+1):
            for x in range(x0, x1+1):
                self.set_at(x-1, y-1, color)

    def get_at(self, x, y):
        try:
            return self.data[y][x]
        except IndexError:
            return

    def set_at(self, x, y, value):
        try:
            self.data[y][x] = value
        except IndexError:
            return

    def draw_pixel(self, x, y, color):
        self.set_at(x-1, y-1, color)

    def draw_vertical_line(self, x, y0, y1, color):
        for y in range(y0, y1+1):
            self.set_at(x-1, y-1, color)

    def draw_horizontal_line(self, x0, x1, y, color):
        for x in range(x0, x1+1):
            self.set_at(x-1, y-1, color)

    def clear(self, *_):
        self.draw_rectangle(1, 1, self.width, self.height, 'O')

    def save_image(self, filename):
        with open(filename, 'w') as f:
            f.write(str(self))
        print('Saved file {!r}'.format(filename))

    def _get_adjacent_cells(self, x, y):
        cells = []
        positions = ((x+1, y),
                     (x-1, y),
                     (x, y+1),
                     (x, y-1))

        for x, y in positions:
            if x < 0 or y < 0:
                continue
            try:
                self.get_at(x, y)
            except IndexError:
                continue
            cells.append((x, y))
        return cells

    def _flood_fill(self, x, y, visited, color):
        if (x, y) in visited:
            return
        visited.append((x, y))
        prev_color = self.get_at(x, y)
        self.set_at(x, y, color)
        for cell in self._get_adjacent_cells(x, y):
            if prev_color != self.get_at(cell[0], cell[1]):
                continue
            self._flood_fill(cell[0], cell[1], visited, color)

    def fill_region(self, x, y, color):
        visited = []
        self._flood_fill(x-1, y-1, visited, color)

    def __repr__(self):
        output = []
        for h in range(self.height):
            output.append(''.join(self.data[h]))
        return '\n'.join(output)


class Context():
    '''
    Context in which Matrix functions are handled
    Create and destroy Matrix instances
    Map commands to the equivalent Matrix methods
    '''
    def __init__(self, cls):
        self.cls = cls
        self.instance = None

    def create(self, *params):
        self.instance = self.cls(*params)

    def exit(self, *params):
        self.instance = None

    def get_function(self, cmd_alias):
        '''
        Expect a command alias (str)
            Example: 'I', 'C'...
        Return a function relative to the cmd_alias (function)
        '''
        try:
            cmd_name = CMD_MAP[cmd_alias.upper()]
        except KeyError:
            raise ValueError('Command {!r} does not exist'.format(cmd_alias))
        if hasattr(self, cmd_name):
            return getattr(self, cmd_name)
        if not self.instance:
            raise ValueError('Instance not initialized')
        return getattr(self.instance, cmd_name)


def parse_command(expr):
    '''
    Expect a command expression (str)
        Example: "I 4 6"
    Return the command name and the params (tuple)
        Example: ('I', [4, 6]) or ('S', ['test.bmp'])
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


def run_command(context, expr):
    '''
    Expect a run context instance (Context)
    Expect a command expression (str)
    '''
    cmd_alias, params = parse_command(expr)
    try:
        func = context.get_function(cmd_alias)
    except ValueError:
        return
    func(*params)


def main(command_lines):
    '''
    Expect a list of input commands (list)
        Example: ['A 5 6', 'B 3 4']
    '''
    context = Context(Matrix)
    for expr in command_lines:
        run_command(context, expr)


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
