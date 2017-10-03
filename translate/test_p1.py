import math
import unittest

from translate import translate, SEPARATOR


class TestTranslate(unittest.TestCase):

    def test_positive_numbers(self):
        n = 0
        for i in range(1, 1000):
            n = n*10 + i
            t = translate(n)

            digits = int(math.log10(n))+1
            number_sep = digits // 3
            if (digits % 3) == 0:
                number_sep -= 1

            # Check the langth of the result: digits + number of separators (commas)
            self.assertEqual(len(t), digits + number_sep)

            # Chck the number of commas
            self.assertEqual(t.count(SEPARATOR), number_sep)


if __name__ == '__main__':
    unittest.main()
