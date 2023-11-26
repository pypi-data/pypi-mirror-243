import codecs
from setuptools import setup

INFO = {}

with codecs.open('README.md', mode='r', encoding='utf-8') as f:
    INFO['long_description'] = f.read()

setup(
    name='asyncio_telnet',
    version='0.1.4',
    description='Asyncio-based Telnet library',
    long_description=INFO['long_description'],
    author='Vladimir Penzin',
    author_email='pvenv@icloud.com',
    py_modules=['asyncio_telnet'],  # добавлено здесь
    url='https://github.com/ForceFledgling/asyncio_telnet',
    platforms='any',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    install_requires=[
        'asyncio',
    ],
)
