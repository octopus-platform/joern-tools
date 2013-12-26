import os

from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "joern-tools",
    version = "0.1",
    author = "Fabian Yamaguchi",
    author_email = "fyamagu@gwdg.de",
    description = "Tools for code analysis based on joern.",
    license = "GPLv3",
    url = "http://github.com/fabsx00/joern-tools/",
    long_description = read('README.md'),
    packages = find_packages(),
    scripts = ['.']
    install_requires = ['joern >= 0.1'],
    dependency_links = ['https://github.com/fabsx00/python-joern/tarball/master/#egg=joern-0.1']
)
