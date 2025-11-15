case = 2
if case==1:
    print('='*10)
    import testMod #a module in the form of a directory
    print(*zip(globals().keys(), globals().values()), sep='\n')
    try:
        print(testMod.testImportHeader)
    except AttributeError:
        print("testMod.testImportHeader failed ❌")
    else:
        print("testMod.testImportHeader succeeded ✅")
    print('='*10)

    #from testMod import *
    import testMod.testImportHeader #a module in the form of a file in the directory above; this is adding `testImportHeader` to the `testMod` namespace
    print(*zip(globals().keys(), globals().values()), sep='\n')
    try:
        print(testMod.testImportHeader)
    except AttributeError:
        print("testMod.testImportHeader failed ❌")
    else:
        print("testMod.testImportHeader succeeded ✅")
    print('='*10)
    #print(testMod, testImportHeader, sep='\n')
    print("Done!")

if case == 2:
    import pkgutil
    import importlib
    def import_submodules(package):
        """Import all submodules of a module, recursively."""
        if isinstance(package, str):
            package_str = package
            package = importlib.import_module(package)
        
        results = {}
        
        for _, name, is_pkg in pkgutil.iter_modules(package.__path__, package.__name__ + '.'):
            full_name = name
            results[full_name] = importlib.import_module(full_name)
            
            if is_pkg:
                results.update(import_submodules(full_name))
             
#        exec(f'import {package_str}')
#        print("exec done")
        return results
    
    import_submodules("testMod")
    import testMod
    print(testMod.testImportHeader)
    print(testMod.testImportHeader2)
    print(testMod)
    print("Done.")
