from setuptools import setup, find_packages

setup(
    name='AZConversion',
    description='一个快捷转换文件格式的库 | A library for quickly converting file formats',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'python-docx',
        'moviepy',
        'Pillow',
        'soundfile'
    ],
)
