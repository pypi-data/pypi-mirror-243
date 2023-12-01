from setuptools import setup, find_packages

DESCRIPTION = 'Train a RKM'
LONG_DESCRIPTION = 'A Python package to simulate and train a RKM model'

# Setting up
setup(
    name='pyrkm',
    version='0.0.2',
    author='Simone Ciarella',
    author_email='<simoneciarella@gmail.com>',
    url='https://github.com/SCiarella/circuit-rbm',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib',
        'torch',
        'torchvision',
        'scipy',
    ],
    keywords=['python', 'statistical physics', 'machine learning', 'rbm'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Education',
        'Programming Language :: Python :: 3',
        'Operating System :: Unix',
    ],
)
