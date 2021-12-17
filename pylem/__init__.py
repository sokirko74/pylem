import os
import json
from .pylem_binary import *


class MorphLanguage:
    Russian = 1
    English = 2
    German = 3

    @staticmethod
    def check_language(langua):
        return langua == MorphLanguage.Russian or langua == MorphLanguage.English or langua == MorphLanguage.German

    @staticmethod
    def GetStrByLanguage(langua):
        if langua == MorphLanguage.Russian:
            return "Russian"
        elif langua == MorphLanguage.English:
            return "English"
        elif langua == MorphLanguage.German:
            return "German"
        else:
            return "unknown"


class LemmaInfo:
    def __init__(self, predicted, lemma = None, part_of_speech = None, morph_features=None, predicted_by=None):
        self.predicted = predicted
        self.lemma = lemma
        self.part_of_speech = part_of_speech
        self.morph_features = morph_features
        self.predicted_by = predicted_by


class MorphanHolder:

    def __init__(self, langua):
        assert MorphLanguage.check_language(langua)
        self.language = langua
        path = os.path.join(os.path.dirname(__file__), 'Dicts/Morph', MorphLanguage.GetStrByLanguage(langua))
        ret = load_morphology(int(langua), path)

    def lemmatize_json(self, word, all_forms=False):
        r = lemmatize_json(self.language, word, all_forms)
        return json.loads(r)

    def lemmatize(self, word):
        lemm_infos_in_json = self.lemmatize_json(word, False)
        for l in lemm_infos_in_json:
            #{'commonGrammems': 'inanim', 'found': False, 'morphInfo': 'N neu,fem,mas,prp,ins,acc,dat,gen,nom,sg,pl', 'srcNorm': 'НЕУБИВАЙМЕНЯ', 'wordForm': 'ААБ'}
            grammems =  set(l.get('commonGrammems', '').split(','))
            i = l['morphInfo'].find(' ')
            if i == -1:
                pos = l['morphInfo']
            else:
                pos = l['morphInfo'][0:i]
                grammems.update((l['morphInfo'][i+1:].split(',')))
            lemm_info = LemmaInfo(predicted=not l['found'],
                                  lemma=l['wordForm'],
                                  part_of_speech=pos,
                                  morph_features=grammems,
                                  predicted_by=l.get('srcNorm'))
            yield lemm_info

    def is_in_dictionary(self, word):
        r = is_in_dictionary(self.language, word)
        return r

    def synthesize(self, word, all_forms=False):
        r = synthesize(self.language, word, all_forms)
        return json.loads(r)


class MorphSourceDictHolder:
    def __init__(self, mwz_path):
        self.mwz_path = mwz_path
        if not os.path.exists(mwz_path):
            raise OSError("cannot find mwz project {}".format(mwz_path))
        load_mwz_project(self.mwz_path)

    def predict_lemm(self, word, suf_len: int, minimal_frequence: int):
        predicted = predict_lemm(self.mwz_path, word, suf_len, minimal_frequence)
        return predicted
