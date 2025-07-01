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
        'textblob',
        # Adicionando o modelo spaCy:
        'pt_core_news_sm @ https://github.com/explosion/spacy-models/releases/download/pt_core_news_sm-3.8.0/pt_core_news_sm-3.8.0-py3-none-any.whl'
    ],
    entry_points={
        'console_scripts': [
            'sata = src.main:main'
        ]
    },
)
