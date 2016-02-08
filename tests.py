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
        mock_matrix.clear.assert_called_with()

    def test_run_command_create_matrix(self):
        ctx = editor.Context(editor.Matrix)
        ctx.create = MagicMock()
        editor.run_command(ctx, 'I 3 4')
        ctx.create.assert_called_with(3, 4)

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
    def setUp(self):
        self.matrix = editor.Matrix(4, 3)

    def test_matrix_created(self):
        assert self.matrix == [
            ['O', 'O', 'O', 'O'],
            ['O', 'O', 'O', 'O'],
            ['O', 'O', 'O', 'O']]

    def test_get_value(self):
        self.matrix.set_at(2, 1, 'C')
        assert self.matrix.get_at(2, 1) == 'C'

    def test_get_value_invalid_cell(self):
        assert self.matrix.get_at(20, 10) is None

    def test_draw_pixel(self):
        self.matrix.draw_pixel(2, 1, 'C')
        assert self.matrix == [
            ['O', 'C', 'O', 'O'],
            ['O', 'O', 'O', 'O'],
            ['O', 'O', 'O', 'O']]

    def test_draw_pixel_max_values(self):
        self.matrix.draw_pixel(4, 3, 'C')
        assert self.matrix == [
            ['O', 'O', 'O', 'O'],
            ['O', 'O', 'O', 'O'],
            ['O', 'O', 'O', 'C']]

    def test_draw_pixel_incorrect_cell(self):
        self.matrix.draw_pixel(20, 11, 'C')
        assert self.matrix == [
            ['O', 'O', 'O', 'O'],
            ['O', 'O', 'O', 'O'],
            ['O', 'O', 'O', 'O']]

    def test_draw_rectangle_3_2(self):
        self.matrix.draw_rectangle(1, 1, 3, 2, 'C')
        assert self.matrix == [
            ['C', 'C', 'C', 'O'],
            ['C', 'C', 'C', 'O'],
            ['O', 'O', 'O', 'O']]

    def test_draw_rectangle_size_one(self):
        self.matrix.draw_rectangle(1, 1, 1, 1, 'C')
        assert self.matrix == [
            ['C', 'O', 'O', 'O'],
            ['O', 'O', 'O', 'O'],
            ['O', 'O', 'O', 'O']]

    def test_draw_rectangle_wrong_values(self):
        self.matrix.draw_rectangle(3, 4, 1, 1, 'C')
        assert self.matrix == [
            ['O', 'O', 'O', 'O'],
            ['O', 'O', 'O', 'O'],
            ['O', 'O', 'O', 'O']]

    def test_draw_rectangle_exceed_limit(self):
        self.matrix.draw_rectangle(1, 1, 10, 10, 'C')
        assert self.matrix == [
            ['C', 'C', 'C', 'C'],
            ['C', 'C', 'C', 'C'],
            ['C', 'C', 'C', 'C']]

    def test_clear(self):
        self.matrix.draw_rectangle(1, 1, 3, 2, 'C')
        self.matrix.clear()
        assert self.matrix == [
            ['O', 'O', 'O', 'O'],
            ['O', 'O', 'O', 'O'],
            ['O', 'O', 'O', 'O']]

    def test_draw_vertical_line(self):
        self.matrix.draw_vertical_line(1, 1, 2, 'C')
        assert self.matrix == [
            ['C', 'O', 'O', 'O'],
            ['C', 'O', 'O', 'O'],
            ['O', 'O', 'O', 'O']]

    def test_draw_vertical_line_wrong_range(self):
        self.matrix.draw_vertical_line(1, 3, 2, 'C')
        assert self.matrix == [
            ['O', 'O', 'O', 'O'],
            ['O', 'O', 'O', 'O'],
            ['O', 'O', 'O', 'O']]

    def test_draw_horizontal_line(self):
        self.matrix.draw_horizontal_line(1, 4, 2, 'C')
        assert self.matrix == [
            ['O', 'O', 'O', 'O'],
            ['C', 'C', 'C', 'C'],
            ['O', 'O', 'O', 'O']]

    def test_draw_horizontal_line_off_limits(self):
        self.matrix.draw_horizontal_line(1, 40, 2, 'C')
        assert self.matrix == [
            ['O', 'O', 'O', 'O'],
            ['C', 'C', 'C', 'C'],
            ['O', 'O', 'O', 'O']]

    def test_fill_region(self):
        self.matrix.draw_horizontal_line(1, 4, 2, 'C')
        self.matrix.fill_region(1, 1, 'A')
        assert self.matrix == [
            ['A', 'A', 'A', 'A'],
            ['C', 'C', 'C', 'C'],
            ['O', 'O', 'O', 'O']]

    def test_fill_region_with_half_segment(self):
        self.matrix.draw_horizontal_line(1, 2, 2, 'C')
        self.matrix.fill_region(1, 1, 'A')
        assert self.matrix == [
            ['A', 'A', 'A', 'A'],
            ['C', 'C', 'A', 'A'],
            ['A', 'A', 'A', 'A']]

    def test_fill_region_different_colors(self):
        self.matrix.draw_horizontal_line(1, 2, 2, 'C')
        self.matrix.draw_vertical_line(4, 1, 3, 'E')
        self.matrix.fill_region(3, 1, 'Z')
        assert self.matrix == [
            ['Z', 'Z', 'Z', 'E'],
            ['C', 'C', 'Z', 'E'],
            ['Z', 'Z', 'Z', 'E']]

    def test_fill_region_single_cell_area(self):
        self.matrix.draw_horizontal_line(1, 4, 2, 'C')
        self.matrix.draw_vertical_line(2, 1, 1, 'E')
        self.matrix.fill_region(1, 1, 'Z')
        assert self.matrix == [
            ['Z', 'E', 'O', 'O'],
            ['C', 'C', 'C', 'C'],
            ['O', 'O', 'O', 'O']]

    def test_save_image(self):
        fp = tempfile.NamedTemporaryFile(mode='w+t')
        self.matrix.save_image(fp.name)
        file_content = fp.read()
        assert file_content == 'OOOO\nOOOO\nOOOO'
        fp.close()


if __name__ == '__main__':
    unittest.main()
