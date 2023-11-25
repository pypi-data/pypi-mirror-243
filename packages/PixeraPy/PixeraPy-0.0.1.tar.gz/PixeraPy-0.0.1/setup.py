#WRITTEN BY: Ted Charles Brown
#ONLY FOR USE WITH PYPI

from setuptools import setup, find_packages

setup(
    name='PixeraPy',
    version='0.0.1',
    packages=find_packages(),
    description='Python package for AVStumpfl, Pixera API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='http://github.com/yourusername/mypackage',
    author='Ted Charles Brown',
    author_email='tedcharlesbrown@gmail.com',
    license='MIT',
    install_requires=[
        "requests"
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)