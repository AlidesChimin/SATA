from setuptools import setup, find_packages

setup(
    name='SATA',
    version='1.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'nltk',
        'pdfminer.six',
        'docx',
        'ttkbootstrap',
        'spacy',
        'gender-guesser',
        'Pillow',
        'wordcloud',
        'textblob'
    ],
    entry_points={
        'console_scripts': [
            'sata = src.main:main'
        ]
    },
)
