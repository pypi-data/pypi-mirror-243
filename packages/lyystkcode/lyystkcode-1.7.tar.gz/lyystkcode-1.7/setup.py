from setuptools import setup

setup(
    name='lyystkcode',
    version='1.7',
    author='lyy',
    author_email='',
    description='userfull application for  lyy',
    #packages=find_packages(),
    license="MIT",
    install_requires=[
        "pandas",
        "baostock",
        "tushare",
        "sqlalchemy",


    ],
)