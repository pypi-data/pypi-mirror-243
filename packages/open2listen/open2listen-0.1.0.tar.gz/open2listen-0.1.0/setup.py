from setuptools import setup, find_packages

setup(
    name='open2listen',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'nougat-ocr',
        'gTTS',
        'idisplay',
    ],
)
