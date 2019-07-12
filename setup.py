from setuptools import setup, find_packages

setup(
    name='qintervals',
    version='0.1',
    description=(
        'An interval training program written in python with a Qt GUI.'
        ),
    author='Jim Madge',
    author_email='jmmadge@gmail.com',
    url='https://github.com/jimmadge/qintervals',
    license='GPLv3',
    packages=find_packages(),
    install_requires=['pyyaml', 'PyQt5'],
    include_package_data=True,
    scripts=['bin/qintervals']
)
