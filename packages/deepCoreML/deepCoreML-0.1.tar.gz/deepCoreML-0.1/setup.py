from distutils.core import setup
from setuptools import find_packages

DESCRIPTION = 'A collection of Machine Learning techniques for data management and augmentation.'
LONG_DESCRIPTION = 'DeepCoreML is a collection of Machine Learning techniques for data management and augmentation. '\
    'More specifically, DeepCoreML includes modules for: '\
    ' * Dataset handling' \
    ' * Text data preprocessing' \
    ' * Text vectorization' \
    ' * Dimensionality Reduction' \
    ' * Handling imbalanced datasets' \
    'DeepCoreML has dependencies with on scikit-learn, imbalanced-learn, pytorch, numpy, pandas.\n\n'\
    'GitHub repository: [https://github.com/lakritidis/DeepCoreML](https://github.com/lakritidis/DeepCoreML)\n\n'

setup(
    name='deepCoreML',
    version='0.1',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author="Leonidas Akritidis",
    author_email="lakritidis@ihu.gr",
    maintainer="Leonidas Akritidis",
    maintainer_email="lakritidis@ihu.gr",
    packages=find_packages(),
    url='https://github.com/lakritidis/DeepCoreML',
    install_requires=["numpy", "pandas", "nltk", "matplotlib", "seaborn", "gensim", "bs4",
                      "torch>=2.0.0+cu117",
                      "transformers>=4.28.1",
                      "scikit-learn>=1.0.0",
                      "imblearn>=0.0"],
    license="Apache",
    keywords=[
        "data engineering", "data management", "text vectorization", "text processing", "dimensionality reduction",
        "imbalanced data", "machine learning", "deep learning"]
)
