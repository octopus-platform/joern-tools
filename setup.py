import os

from setuptools import setup, find_packages
import os, fnmatch

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def getScripts():
    x = []
    for (dirpath, dirnames, filenames) in os.walk('tools'):
        x.extend(os.path.join(dirpath,f) for f in filenames)
    return x

setup(
    name = "joern",
    version = "0.2",
    author = "Fabian Yamaguchi",
    author_email = "f.yamaguchi@tu-braunschweig.de",
    description = "Tools for code analysis based on joern.",
    license = "GPLv3",
    url = "http://github.com/octopus-tools/joern-tools/",
    long_description = read('README.md'),
    packages = find_packages(),
    package_data={"joern": ['steps/*',]},
    scripts = getScripts(),
    install_requires = ['pyorient', 'pygraphviz', 'chardet'],
    dependency_links = ['https://github.com/octopus-platform/pyorient/tarball/master/#egg=pyorient'],
    zip_safe = False
)
