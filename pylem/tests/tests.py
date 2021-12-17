from pylem import MorphanHolder, MorphLanguage
import unittest

class TestBasicAnalyze(unittest.TestCase):

    def test_mama(self):
       holder = MorphanHolder(MorphLanguage.Russian)
       res = holder.is_in_dictionary("мама")
       self.assertTrue(res)

    def test_asokirko(self):
       holder = MorphanHolder(MorphLanguage.Russian)
       res = holder.is_in_dictionary("этогослованнет")
       self.assertFalse(res)

    def test_mother(self):
       holder = MorphanHolder(MorphLanguage.English)
       res = holder.is_in_dictionary("mother")
       self.assertTrue(res)

    def test_mutter(self):
       holder = MorphanHolder(MorphLanguage.German)
       res = holder.is_in_dictionary("mutter")
       self.assertTrue(res)



class TestMorphInfoJson(unittest.TestCase):
    def test_papa(self):
        holder = MorphanHolder(MorphLanguage.Russian)
        canon = [{'commonGrammems': 'anim', 'found': True, 'morphInfo': 'N mas,nom,sg', 'wordForm': 'ПАПА'}]
        res = holder.lemmatize_json("папа")
        self.assertEqual(len(canon), len(res))
        self.assertDictEqual(canon[0], res[0])


class TestSynthesis(unittest.TestCase):
    def test_stul(self):
        holder = MorphanHolder(MorphLanguage.Russian)
        answer = holder.synthesize("мама", "N fem,sg,gen")
        self.assertEqual(len(answer['forms']), 1)
        self.assertEqual("МАМЫ", answer['forms'][0])


if __name__ == '__main__':
    unittest.main()
