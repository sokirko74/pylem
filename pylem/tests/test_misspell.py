from pylem import MorphanHolder, MorphLanguage
import unittest


class TestMisspell(unittest.TestCase):
    def test_sokirko(self):
        holder = MorphanHolder(MorphLanguage.Russian)
        res = holder.correct_misspell("сакирко")
        self.assertGreater(len(res), 0)
        self.assertTrue(res[0], "СОКИРКО")


if __name__ == '__main__':
    unittest.main()
