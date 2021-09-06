from setuptools import setup

setup(
	name='scrython',
	packages=['scrython', 'scrython.cards', 'scrython.rulings', 'scrython.catalog', 'scrython.sets', 'scrython.symbology', 'scrython.bulk_data'],
	version='1.10.1',
	description='A wrapper for using the Scryfall API.',
	long_description='https://github.com/NandaScott/Scrython/blob/master/README.md',
	url='https://github.com/NandaScott/Scrython',
	download_url='https://github.com/NandaScott/Scrython/archive/0.1.0.tar.gz',
	author='Nanda Scott',
	author_email='nanda1123@gmail.com',
	license='MIT',
	keywords=['Scryfall', 'magic', 'the gathering', 'scrython', 'wrapper'],
	install_requires=['aiohttp', 'asyncio']
	)
