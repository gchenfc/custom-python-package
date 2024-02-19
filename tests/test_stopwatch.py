import unittest
import time
from gerry import Stopwatch
from io import StringIO
from unittest.mock import patch


class TestStopwatch(unittest.TestCase):
    def checktime(self, act, exp, delta=0.01):
        self.assertAlmostEqual(
            act,
            exp,
            delta=delta,
            msg=f'Time was not accurate (expected {exp}, got {act})')

    def test_stopwatch_basic(self):
        # Basic usage
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with Stopwatch(print=False) as sw:
                time.sleep(0.3)
        self.checktime(float(sw), 0.3)
        self.assertEqual(fake_out.getvalue(), '',
                         'Stopwatch printed when it should not have')

        # Check that external statements do not affect timing
        with patch('sys.stdout', new=StringIO()) as fake_out:
            time.sleep(0.10)
            with Stopwatch(print=False) as sw:
                time.sleep(0.23)
            time.sleep(0.15)
        self.checktime(float(sw), 0.23)
        self.assertEqual(fake_out.getvalue(), '',
                         'Stopwatch printed when it should not have')

    def test_stopwatch_printing(self):
        # Default to no printing
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with Stopwatch() as sw:
                time.sleep(0.05)
            t = float(sw)
            self.checktime(t, 0.05)
            self.assertEqual(fake_out.getvalue(), '',
                             'Stopwatch printed when it should not have')

        # Test with name only
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with Stopwatch('Test') as sw:
                time.sleep(0.05)
            t = float(sw)
            self.checktime(t, 0.05)
            self.assertEqual(fake_out.getvalue(), f'Test took {t:.3f}s\n',
                             'Stopwatch did not print correctly')

        # Test with message only
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with Stopwatch(msg='thingy {:.6f} s') as sw:
                time.sleep(0.05)
            t = float(sw)
            self.checktime(t, 0.05)
            self.assertEqual(fake_out.getvalue(), f'thingy {t:.6f} s\n',
                             'Stopwatch did not print correctly')

        # Test with both name and message
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with Stopwatch(name='Test', msg='{name} and {:.2f} s') as sw:
                time.sleep(0.05)
            t = float(sw)
            self.checktime(t, 0.05)
            self.assertEqual(fake_out.getvalue(), f'Test and {t:.2f} s\n',
                             'Stopwatch did not print correctly')

        # Test with print=False
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with Stopwatch(name='MyTest', print=False) as sw:
                time.sleep(0.05)
            t = float(sw)
            self.checktime(t, 0.05)
            self.assertEqual(fake_out.getvalue(), '',
                             'Stopwatch printed when it should not have')
            self.assertEqual(str(sw), f'MyTest took {t:.3f}s',
                             'Stopwatch did not print correctly')

    def test_print_start_and_end(self):
        # Test with print_start_and_end
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with Stopwatch(name='Test', print_start_and_end=True) as sw:
                time.sleep(0.05)
                self.assertEqual(fake_out.getvalue(), f'Starting Test... ⏳ ',
                                 'Stopwatch did not print correctly')
            t = float(sw)
            self.checktime(t, 0.05)
            self.assertEqual(
                fake_out.getvalue(),
                f'Starting Test... ⏳ Finished Test in {t:.3f}s\n',
                'Stopwatch did not print correctly')


if __name__ == '__main__':
    unittest.main()
