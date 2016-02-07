# encoding: utf-8

import tempfile
import unittest
from unittest.mock import MagicMock
import editor_grafico as editor


class InputTest(unittest.TestCase):
    def test_input_reader(self):
        test_data = '''
        I 4 5
        C
        S one.bmp
        G 2 3 J
        V 2 3 4 W
        '''
        fp = tempfile.NamedTemporaryFile(mode='w+t')
        fp.write(test_data)
        fp.seek(0)
        file_content = editor.read_input(fp.name)
        assert file_content == [
            'I 4 5',
            'C',
            'S one.bmp',
            'G 2 3 J',
            'V 2 3 4 W'
        ]
        fp.close()

    def test_parse_command_num_params(self):
        test_data = 'A 5 6'
        result = editor.parse_command(test_data)
        assert result == ('A', [5, 6])

    def test_parse_command_file_params(self):
        test_data = 'S img.bmp'
        result = editor.parse_command(test_data)
        assert result == ('S', ['img.bmp'])

    def test_parse_command_no_param(self):
        test_data = 'X'
        result = editor.parse_command(test_data)
        assert result == ('X', [])

    def test_error_on_input_reader(self):
        with self.assertRaises(IOError):
            editor.read_input('nowhere_file.txt')

    def test_run_command_clear_matrix(self):
        ctx = editor.Context(editor.Matrix)
        ctx.create(3, 4)
        mock_matrix = ctx.instance
        mock_matrix.clear = MagicMock()
        editor.run_command(ctx, 'C')
        mock_matrix.clear.assert_called_with([])

    def test_run_command_create_matrix(self):
        ctx = editor.Context(editor.Matrix)
        ctx.create = MagicMock()
        editor.run_command(ctx, 'I 3 4')
        ctx.create.assert_called_with([3, 4])

    def test_run_command_invalid_command(self):
        ctx = editor.Context(editor.Matrix)
        ctx.create(3, 4)
        assert editor.run_command(ctx, 'Z') is None


class ContextTest(unittest.TestCase):
    def setUp(self):
        self.context = editor.Context(editor.Matrix)

    def test_executor_create(self):
        self.context.create(4, 5)
        assert isinstance(self.context.instance, editor.Matrix)

    def test_executor_exit(self):
        self.context.exit()
        assert self.context.instance is None

    def test_get_function_create(self):
        func = self.context.get_function('I')
        assert func == self.context.create

    def test_get_function_non_initialized_matrix(self):
        with self.assertRaises(ValueError):
            self.context.get_function('C')

    def test_get_function_initialized_matrix(self):
        self.context.create(5, 6)
        func = self.context.get_function('C')
        assert func == self.context.instance.clear

    def test_get_function_invalid_command(self):
        self.context.create(5, 6)
        with self.assertRaises(ValueError):
            self.context.get_function('Z')


class MatrixTest(unittest.TestCase):
    def test_matrix_dimensions(self):
        m = editor.Matrix(4, 3)
        assert m.data == [
            ['O', 'O', 'O', 'O'],
            ['O', 'O', 'O', 'O'],
            ['O', 'O', 'O', 'O']]


if __name__ == '__main__':
    unittest.main()
