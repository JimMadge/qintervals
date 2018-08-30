from setuptools import setup

setup(
    name='qintervals',
    version='0.1',
    description='An interval training program written in python with a Qt GUI.',
    author='Jim Madge',
    author_email='jmmadge@gmail.com',
    url='https://github.com/jimmadge/qintervals',
    license='GPLv3',
    packages=['qintervals'],
    install_requires=['PyQt5'],
    include_package_data=True,
    scripts=['bin/qintervals']
)

