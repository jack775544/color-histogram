from setuptools import setup, find_packages

requires = [
    'tropofy',
    'requests',
    'simplekml',
    'pillow',
]

setup(
    name='color-histogram',
    version='1.0',
    description='A tropofy app that generates a colour histogram from a web hosted image',
    author='Jack Kerr',
    url='https://j754.xyz',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
)
