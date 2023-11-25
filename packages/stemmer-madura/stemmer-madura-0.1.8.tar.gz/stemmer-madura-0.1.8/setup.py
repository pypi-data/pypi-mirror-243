from setuptools import setup

setup(
  name='stemmer-madura',
  version='0.1.8',
  description='Stemmer untuk bahasa Madura menggunakan rule based',
  author='Mohammad Nazir Arifin',
  author_email='ceylon.rizan@gmail.com',
  packages=['stemmer_madura', 'stemmer_madura.lib'],
  package_data={'stemmer_madura': ['data/*.txt']},
  license='MIT',
  install_requires=[],
  keywords=['stemmer', 'madura', 'bahasa madura', 'nlp'],
  classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Education',
    'Programming Language :: Python :: 3.10',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
  ],
)