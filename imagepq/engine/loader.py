 
def load(module_name) :
    """
    手功加载模块：
    插件写成自加载形式，调用本模块，把插件加载到插件指定的位置上
    """
    import importlib 
    spec = importlib.util.find_spec(module_name)
    if spec is None :
        print("cant find the {} module".format(module_name))
    else:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        sys.modules[name] = module