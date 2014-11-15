

from distutils.core import setup
import os


def read(fname):
    # noinspection PyBroadException
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except:
        return ""


setup(
    name='clocked',
    packages=['clocked'],
    version='0.2',
    description='python library for high level profiling',
    author='Jesse Buesking',
    author_email='jessebuesking+pypi@gmail.com',
    url='https://github.com/JesseBuesking/clocked',
    download_url='https://github.com/JesseBuesking/clocked/tarball/0.2',
    keywords=['benchmark', 'benchmarking', 'profiler', 'profiling'],
    long_description=read('readme.md'),
    classifiers=[]
)
