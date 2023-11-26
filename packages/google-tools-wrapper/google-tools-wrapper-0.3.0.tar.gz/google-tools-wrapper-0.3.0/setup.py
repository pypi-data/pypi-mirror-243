from setuptools import setup

with open("README.md", "r") as file:
    readme = file.read()

setup(
    name='google-tools-wrapper',
    version='0.3.0',
    license='MIT License',
    author='João Zacchello',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='xongsdartx@gmail.com',
    keywords=['google tools', 'google finance', 'google api', 'currency conversion', 'google translater', 'google tradutor'],
    description=u'An unofficial Google Tools wrapper',
    packages=['google_tools'],
    install_requires=['selenium', 'requests', 'bs4'],
)

#comandos:
# criar empacotamento: python.exe setup.py sdist
# enviar para pypi: twine upload dist/*
#pegue uma api key pro projeto no pypi: 
