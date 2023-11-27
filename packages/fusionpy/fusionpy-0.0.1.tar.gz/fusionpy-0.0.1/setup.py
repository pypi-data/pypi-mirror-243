from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='fusionpy',
    packages=['fusionpy'],
    
    version='0.0.1',

    license='MIT',

    install_requires=['numpy'],
    author='astroysmr',
    author_email='astro.yoshimura@gmail.com',

    url='https://github.com/exfusion-dev',

    description='Python libralies for laser fusion development',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='laser fusion',

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.11',
    ],
)