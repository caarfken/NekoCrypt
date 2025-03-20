from setuptools import setup, find_packages

setup(
    name='nekocrypt',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    description='A simple encryption package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/caarfken/NekoCrypt',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache-2.0 License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
