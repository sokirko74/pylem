def __bootstrap__():
    global __bootstrap__, __loader__, __file__
    import sys, pkg_resources, importlib.util, os
    library_name = "pylem_binary"
    def find_compiled_library():
        f  =  os.path.dirname(__file__)
        if  len(f) == 0:
            f =  "."
        for i in os.listdir(f):
            if i.startswith(library_name) and (i.endswith('.pyd') or i.endswith('.so')):
                return i
        raise Exception ("no binary library found to load")
    compiled_lib_path = find_compiled_library()
    print ("compiled_lib_path = {}".format(compiled_lib_path))
    print(sys.modules)
    __file__ = pkg_resources.resource_filename(library_name, compiled_lib_path)
    __loader__ = None; 
    del __bootstrap__, __loader__
    spec = importlib.util.spec_from_file_location(library_name, __file__)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
__bootstrap__()

