import setuptools
from setuptools import setup
from numpy.distutils.core import setup
from numpy.distutils.misc_util import Configuration
from os.path import join

str_version = '1.3.3'

def configuration(parent_package='', top_path=''):
    # this will automatically build the scattering extensions, using the
    # setup.py files located in their subdirectories
    config = Configuration(None, parent_package, top_path)

    pkglist = setuptools.find_packages()
    for i in pkglist:
        config.add_subpackage(i)
    # config.add_data_files(join('assets', '*.png'))
    # config.add_data_files(join('README.md'))

    return config


if __name__ == '__main__':
    pass
    setup(
        configuration=configuration,  # uncomment this to attach files other than *.py
        name='cellink',
        version=str_version,
        description='An easy-to-use engine that allows python programmers to code with Chain of Responsibility Pattern',
        # url='-_-',
        author='Zhai Menghua',
        author_email='viibridges@gmail.com',
        license='Apache License Version 2.0',
        packages=['cellink'],
        zip_safe=False,
        install_requires= ['graphviz'],
        python_requires='>=3')
