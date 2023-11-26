from setuptools import setup, find_packages

setup(
    name='asyncio_telnet',
    version='0.1.0',
    description='Asyncio-based Telnet library',
    author='Vladimir Penzin',
    author_email='pvenv@icloud.com',
    packages=find_packages(where='netflex'),
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
