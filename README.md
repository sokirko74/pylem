# Morphological analyzer for Russian, English and German languages. 
This is a python wrapper for C++ morphology library that was created in 2000 (many years ago) 
for website [aot.ru](http://aot.ru).  The original library was written in C++, so we have to
compile it and integrate with python using [pybind11](https://github.com/pybind/pybind11).
The dictionaries are rather outdated, but I use them for some modern projects,
that's why I decided to share the project with other people.

License is MIT.

The project is distributed in (sources)[https://github.com/sokirko74/pylem], you have to install cmake and modern C++ (17)
compiler to your workstation. 


## Install
Normally you could install the project with 
`python -m pip install pylem`
but if it does not work install it using the following steps:
1. download and unpack sources
2. run python setup.py install

## Using the library

To search word `mother` in the English dictionary one should 
write the following code:

```python
from pylem import MorphanHolder, MorphLanguage

h = MorphanHolder(MorphLanguage.English) #load dicts from disk

print(h.is_in_dictionary("mother"))
```

Other usages are covered by [unittests](https://github.com/sokirko74/pylem/blob/main/pylem/tests/tests.py) 
