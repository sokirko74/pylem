from pylem import MorphSourceDictHolder
import unittest
import os


class TestLemPredict(unittest.TestCase):

    def test_surname_predict(self):
        mwz_path = os.path.join(os.path.dirname(__file__), '../morph_dict/data/Russian/project.mwz')
        holder = MorphSourceDictHolder(mwz_path)
        r = holder.predict_lemm("асокирко", 3, 2)
        self.assertGreater(len(r), 0)

if __name__ == '__main__':
    unittest.main()
