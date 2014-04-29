import os

from setuptools import setup, find_packages
import os, fnmatch

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "joerntools",
    version = "0.1",
    author = "Fabian Yamaguchi",
    author_email = "fyamagu@gwdg.de",
    description = "Tools for code analysis based on joern.",
    license = "GPLv3",
    url = "http://github.com/fabsx00/joern-tools/",
    long_description = read('README.md'),
    packages = find_packages(),
    package_data={"joerntools": ['steps/*',]},
    scripts = [f for f in os.listdir('.') if fnmatch.fnmatch(f, '*.py')],
    install_requires = ['joern >= 0.1', 'pygraphviz'],
    dependency_links = ['https://github.com/fabsx00/python-joern/tarball/master/#egg=joern-0.1'],
    zip_safe = False
)

