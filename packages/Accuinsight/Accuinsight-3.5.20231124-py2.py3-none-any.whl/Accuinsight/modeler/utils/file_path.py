from Accuinsight.modeler.utils.dependency.dependencies import gather_sources_and_dependencies
from Accuinsight.modeler.core.LcConst import LcConst

def get_file_path(_caller_globals):
    print("Excuting environment", _caller_globals.get("get_ipython"))
    # print(_caller_globals)
    filepath = _caller_globals.get("__session__") or _caller_globals.get("__file__")
    print("call stack filename:", filepath)
    sources, dependencies = gather_sources_and_dependencies(globs=_caller_globals, save_git_info=False)

    if filepath.startswith(LcConst.ENV_JUPYTER_HOME_DIR+'/'):
        filepath_in_Jupyter = filepath[len(LcConst.ENV_JUPYTER_HOME_DIR+'/'):]
    return filepath_in_Jupyter, sources, dependencies