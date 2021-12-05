#define PY_SSIZE_T_CLEAN
#ifdef _DEBUG
#undef _DEBUG
#include <python.h>
#define _DEBUG
#else
#include <python.h>
#endif

#include <iostream>
//#include "morph_dict/LemmatizerBaseLib/MorphanHolder.h"
//#include <stdio.h>

static PyObject*
pylem_test_method(PyObject* self, PyObject* args)
{
    const char* command;
    int sts;

    if (!PyArg_ParseTuple(args, "s", &command))
        return NULL;
    //printf("%s\n", command);
    std::cout << "aaa" << "\n";
    return PyLong_FromLong(0);
}


static PyMethodDef PylemMethods[] = {
    {"test_method",  pylem_test_method, METH_VARARGS,"Execute a shell command."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef pylemmodule = {
    PyModuleDef_HEAD_INIT,
    "pylem",   /* name of module */
    nullptr, /* module documentation, may be NULL */
    -1,       /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
    PylemMethods
};

/*CMorphanHolder EnglishHolder;

bool load_morphology(CMorphanHolder& holder, MorphLanguageEnum langua) {
    if (!holder.LoadLemmatizer(langua)) {
        std::cerr << "Cannot load morph_dict\n";
        return false;
    }
    Holder.m_pGramTab->m_bUseNationalConstants = false;
    Holder.m_bUsePrediction = true;
    return true;
}
*/

PyMODINIT_FUNC PyInit_pylem(void)
{
    //load_morphology(EnglishHolder, morphEnglish);
    return PyModule_Create(&pylemmodule);
}

