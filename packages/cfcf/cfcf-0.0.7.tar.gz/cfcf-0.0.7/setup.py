from setuptools import find_packages
from setuptools import setup
import cfcf


def load_description():
    with open('README.md', 'r') as file:
        line = file.readline()
        prev = ''
        while line:
            if prev == '# cfcf\n':
                return line.rstrip()
            prev = line
            line = file.readline()
    return ''


def load_long_description():
    with open('README.md', 'r') as file:
        return file.read().rstrip()


setup(
    name='cfcf',
    version=cfcf.__version__,
    description=load_description(),
    long_description=load_long_description(),
    long_description_content_type="text/markdown",
    author='tkms',
    author_email='tkmnet.dev@gmail.com',
    url='https://github.com/tkmnet/cfcf',
    packages=find_packages(),
    install_requires=['ulid-py'],
)
