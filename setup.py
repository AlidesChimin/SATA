from setuptools import setup, find_packages

setup(
    name='sata',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'nltk',
        'pdfminer.six',
        'docx',
        'ttkbootstrap',  # Adicionado
        'tkinter',        # Adicionado (não necessário no pip, mas incluído por clareza)
        'spacy',          # Adicionado
        'gender-guesser', # Adicionado
        'csv'             # OBS: O `csv` já faz parte do Python padrão, não precisa ser instalado
    ],
    entry_points={
        'console_scripts': [
            'sata = src.main:main'
        ]
    },
)
