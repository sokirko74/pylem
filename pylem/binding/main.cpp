#include <pybind11/pybind11.h>
#include <iostream>
#include "morph_dict/LemmatizerBaseLib/MorphanHolder.h"
#include <stdio.h>
#include <exception>

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

namespace py = pybind11;

CMorphanHolder EnglishHolder;
CMorphanHolder RussianHolder;
CMorphanHolder GermanHolder;

CMorphanHolder& GetHolder(int langua) {
    switch (langua) {
        case morphEnglish: return EnglishHolder;
        case morphRussian: return RussianHolder;
        case morphGerman: return GermanHolder;
    }
    throw std::runtime_error("unknown language");
}

int load_morphology(int langua, std::string folder) {
    try {
        GetHolder(langua).LoadLemmatizer((MorphLanguageEnum)langua, folder);
        GetHolder(langua).m_pGramTab->m_bUseNationalConstants = false;
    }
    catch (CExpc e) {
        throw std::runtime_error(e.m_strCause);
    }
    return 1;
}

std::string lemmatize_json(int langua, std::string word_form, bool allForms) {
    word_form = convert_from_utf8(word_form.c_str(), GetHolder(langua).m_CurrentLanguage);
    return GetHolder(langua).LemmatizeJson(word_form.c_str(), allForms, true, true);
}

bool is_in_dictionary(int langua, std::string word_form) {
    word_form = convert_from_utf8(word_form.c_str(), (MorphLanguageEnum)langua);
    return GetHolder(langua).IsInDictionary(word_form);
}

std::string synthesize(int langua, std::string word_form, std::string part_of_speech_and_grammems) {
    CMorphanHolder& holder = GetHolder(langua);
    MorphLanguageEnum lang = (MorphLanguageEnum)langua;
    word_form = convert_from_utf8(word_form.c_str(), lang);
    part_of_speech_and_grammems = convert_from_utf8(part_of_speech_and_grammems.c_str(), lang);
    part_of_speech_t partOfSpeech;
    grammems_mask_t grammems;
    if (!holder.m_pGramTab->ProcessPOSAndGrammemsIfCan(part_of_speech_and_grammems.c_str(), &partOfSpeech, &grammems)) {
        return "{\"forms\":[], \"error\": \"cannot process part_of_speech_and_grammems\"}";
    }
    std::vector<CFormInfo>	paradigms;
    holder.m_pLemmatizer->CreateParadigmCollection(false,
        word_form,
        is_upper_alpha((unsigned char)word_form[0], lang), true, paradigms);
    if (paradigms.empty()) {
        return "{\"forms\":[], \"error\": \"word form not found\"}";
    };
    std::vector<std::string> found_forms;
    for (auto& p : paradigms) {
        if (holder.m_pGramTab->GetPartOfSpeech(p.GetAncode(0).c_str()) != partOfSpeech) {
            continue;
        }
        for (size_t i = 0; i < p.GetCount(); i++) {

            std::string gramCodes = p.GetAncode(i) + p.GetCommonAncode();
            grammems_mask_t form_mask = holder.m_pGramTab->GetAllGrammems(gramCodes.c_str());
            if ((form_mask & grammems) == grammems) {
                found_forms.push_back(std::string("\"") + convert_to_utf8(p.GetWordForm(i), lang) + std::string("\""));
            }
        }
    }
    return std::string("{\"forms\": [") + join_string(found_forms, ",") + std::string("]}");

}


map<string, MorphoWizard*> WizardsByPath;

bool load_mwz_project(std::string mwz_project_path) {
    MorphoWizard* wizard = new MorphoWizard(); // I do not delete wizards in this project, it is not important
    wizard.load_wizard(mwz_project_path, "guest", false);
    WizardsByPath[mwz_project_path] = wizard;
    return true;
}
/*
void predict_lemm(std::string mwz_project_path, const std::string& lemm, const int preffer_suf_len, const int minimal_frequence)
{
    WizardsByPath[mwz_project_path]->predict_lemm(lemm,  preffer_suf_len, minimal_frequence, true);
    for
    			const CPredictSuffix& S = *GetWizard()->m_CurrentPredictedParadigms[ind];
			const CFlexiaModel& P = GetWizard()->m_FlexiaModels[S.m_FlexiaModelNo];

}
*/

PYBIND11_MODULE(pylem_binary, m) {
    m.doc() = R"pbdoc()pbdoc";
    m.def("load_morphology", &load_morphology, R"pbdoc()pbdoc");
    m.def("lemmatize_json", &lemmatize_json, R"pbdoc()pbdoc");
    m.def("is_in_dictionary", &is_in_dictionary, R"pbdoc()pbdoc");
    m.def("synthesize", &synthesize, R"pbdoc()pbdoc");
    m.def("load_mwz_project", &load_mwz_project, R"pbdoc()pbdoc");

  
#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
