# encoding: utf-8

import unittest
import tempfile
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


class MatrixTest(unittest.TestCase):
    def test_matrix_dimensions(self):
        m = editor.Matrix(4, 3)
        assert m.data == [
            ['O', 'O', 'O', 'O'],
            ['O', 'O', 'O', 'O'],
            ['O', 'O', 'O', 'O']]


if __name__ == '__main__':
    unittest.main()
