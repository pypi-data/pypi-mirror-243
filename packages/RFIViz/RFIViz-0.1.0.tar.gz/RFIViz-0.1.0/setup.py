from setuptools import setup, find_packages

setup(
    name='RFIViz',
    version='0.1.0',
    author='Timothy H Bell',
    author_email='timothy.bell@etu.unice.fr',
    description='A visualisation tool for Random Forests',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)