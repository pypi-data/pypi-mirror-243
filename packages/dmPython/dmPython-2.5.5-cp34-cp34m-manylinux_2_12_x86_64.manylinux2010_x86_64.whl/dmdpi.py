import os
import sys
import pip
import inspect
dpi_path = os.path.dirname(__file__) + '/dpi'
if 'SETUPTOOLS_USE_DISTUTILS' not in os.environ:
    os.environ['SETUPTOOLS_USE_DISTUTILS'] = 'stdlib'
else:
    if 'stdlib' not in os.environ['SETUPTOOLS_USE_DISTUTILS']:
        os.environ['SETUPTOOLS_USE_DISTUTILS'] = 'stdlib' +':' + os.environ['SETUPTOOLS_USE_DISTUTILS']
if 'LD_LIBRARY_PATH' not in os.environ:
    os.environ['LD_LIBRARY_PATH'] = dpi_path
    if sys.version_info[:2]<(3,5) and sys.version_info[:2]>(3,7):
        if sys.argv[0] == '':
            lenth_site_packages = len(inspect.getfile(pip)) - len(inspect.getfile(pip).split('/')[-1]) - len(inspect.getfile(pip).split('/')[-2]) - 1
            path_str_site = inspect.getfile(pip)[0:lenth_site_packages]
            os.execve(sys.executable, [sys.executable, path_str_site + "dm_remake_python_env.py"], os.environ)
        else:
            os.execve(sys.executable, [sys.executable] + sys.argv, os.environ)
else:
    if dpi_path not in os.environ['LD_LIBRARY_PATH']:
        os.environ['LD_LIBRARY_PATH'] = dpi_path + ':' + os.environ['LD_LIBRARY_PATH']
        if sys.version_info[:2]<(3,5) and sys.version_info[:2]>(3,7):
            if sys.argv[0] == '':
                lenth_site_packages = len(inspect.getfile(pip)) - len(inspect.getfile(pip).split('/')[-1]) - len(inspect.getfile(pip).split('/')[-2]) - 1
                path_str_site = inspect.getfile(pip)[0:lenth_site_packages]
                os.execve(sys.executable, [sys.executable, path_str_site + "dm_remake_python_env.py"], os.environ)
            else:
                os.execve(sys.executable, [sys.executable] + sys.argv, os.environ)
