from setuptools import setup

requirements = []
with open('requirements.txt') as f:
	requirements = f.read().splitlines()

readme = ''
with open('README.md') as f:
	readme = f.read()

setup(
	name='scrython',
	packages=['scrython'],
	version='0.1.0',
	description='A wrapper for using the Scryfall API.',
	long_description=readme
	url='https://github.com/NandaScott/Scrython',
	download_url='https://github.com/NandaScott/Scrython/archive/0.1.0.tar.gz',
	author='Nanda Scott',
	author_email='nanda1123@gmail.com',
	license='MIT',
	keywords=['Scryfall', 'magic', 'the gathering', 'scrython', 'wrapper'],
	install_requires=requirements
	)
