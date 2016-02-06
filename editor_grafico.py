# !/usr/bin/python3
# -*- coding: utf-8 -*-

import sys


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

    cmd_alias, params = expr.split(maxsplit=1)
    return cmd_alias, [clean(x) for x in params.split()]


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
    for expr in command_list:
        cmd_alias, params = parse_command(expr)
        print(cmd_alias, params)


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
