# -*- coding: utf-8 -*-
import setuptools

setuptools.setup(
    name='python-cuit',
    version='1.0.1',
    # py_modules = ['cuit'],
    author='Agustin Bouillet',
    author_email='agustin.bouillet@gmail.com',
    url='https://github.com/agustinbouillet/python-cuit',
    long_description_content_type="text/markdown",
    description='Validador de CUIT',
    long_description='Validador de Código Único de Identificación Titubaria (CUIT)',
    keywords = ['cuil', 'cuit', 'Argentina', 'AFIP', 'ANSES'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.8",
)