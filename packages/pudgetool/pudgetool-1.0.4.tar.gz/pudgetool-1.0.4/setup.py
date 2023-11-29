#!/usr/bin/python3 
# -*- coding: utf-8 -*- 

from setuptools import setup, find_packages, Extension
from setuptools.command.install import install
from Cython.Build import cythonize
from distutils.sysconfig import get_python_lib
import os

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION
        install.run(self)
 
        pkg_path = get_python_lib()
        pg_path = os.path.join(pkg_path, 'pudge')

with open('requirements.txt') as f:
    required = f.read().splitlines()

package_dir = 'src'
try:
    from Cython.Distutils import build_ext

    source_file = os.path.join(package_dir, "numa/numa.pyx")
    cython_available = True
except ImportError:
    source_file = "numa.c"
    cython_available = False

options = {'ext_modules': [
        Extension("numa",
                [source_file],
                libraries=["numa"],
                define_macros=[('NUMA_VERSION1_COMPATIBILITY', 1)],
                )
    ]
}

if cython_available:
    options['cmdclass'] = {"build_ext": build_ext}

setup(
    name = "pudgetool", 
    version = "1.0.4", 
    keywords = ("pudge tools", "CLI tools"),
    description = "pudge tools is automatic coding tools",  
    long_description = "convenient python cli tools, like s3, jumpserver url switches...",  
    license = "MIT Licence",  
    url = "https://github.com/ThierryZhou/pudgetool.git",
    author = "thierry.zhou",  
    author_email = "zhouhui295@163.com",
    platforms = "any",  
    install_requires = required,
    packages=['pudgetool', 'pudge', 'numa'],
    package_dir={
        'pudgetool': 'src',
        'pudge': 'src',
        'numa': 'src',
    },
    scripts = [],  
    entry_points = {  
        'console_scripts': [  
            'pg = pudgetool.entry_point:entry_point' 
        ]
    },
    **options
)

# package_dir = 'src/pudge'
# setup(
#     name = "pudge", 
#     version = "1.0.4", 
#     keywords = ("pudge develop package", "Dev tools"),
#     description = "pudge dev tools is automatic coding package",  
#     long_description = "convenient python dev package, like numa, benchmark...",  
#     license = "MIT Licence",
#     url = "https://github.com/ThierryZhou/pudgetool.git",
#     author = "thierry.zhou",
#     author_email = "zhouhui295@163.com",
#     platforms = "any",
#     install_requires = required,
#     packages=find_packages(package_dir),
#     package_dir={'': 'src'},
#     **options
# )

from setuptools.command.sdist import sdist as _sdist  
from setuptools.command.upload import upload as _upload  
  
class sdist(_sdist):  
    def run(self):  
        # generate manifest file which includes all files listed in MANIFEST.in file in top-level directory.  
        self.distribution.run_command('manifest')  
        # create source distribution package with generated manifest file.  
        _sdist.run(self)  
        self.distribution.run_command('build')  # build source distribution package into binary distribution package.  
        self.distribution.run_command('upload')  # upload source/binary distribution package to PyPI.
