﻿import os
import json
from .pylem_binary import *

class MorphLanguage:
    Russian = 1
    English = 2
    German = 3
    def check_language(l):
        return l == MorphLanguage.Russian  or l == MorphLanguage.English or l == MorphLanguage.German

    def GetStrByLanguage(l):
        if l == MorphLanguage.Russian:
            return "Russian"
        elif l == MorphLanguage.English:
            return "English"
        elif l == MorphLanguage.German:
            return "German"
        else:
            return "unknown"

class MorphanHolder:
    
    def __init__(self, language):
        assert MorphLanguage.check_language(language)
        self.language = language
        path = os.path.join(os.path.dirname(__file__), 'Dicts/Morph', MorphLanguage.GetStrByLanguage(language))
        ret = load_morphology(int(language), path)

    def lemmatize_json(self, word, all_forms=False):
        r = lemmatize_json(self.language, word, all_forms)
        return json.loads(r)

    def is_in_dictionary(self, word):
        r = is_in_dictionary(self.language, word)
        return r

    def synthesize(self, word, all_forms=False):
        r = synthesize(self.language, word, all_forms)
        return json.loads(r)

