import setuptools
from setuptools import setup, find_packages

setuptools.setup(name='ipa_rhyming',
                 version='1.0.5',
                 packages=find_packages(),
                 package_data={'ipa_rhyming': ['static']},
                 classifiers=[
                     'Programming Language :: Python :: 3',
                     'Operating System :: OS Independent',
                     'Topic :: Scientific/Engineering'
                 ],
                 python_requires='>=3',
                 author_email='neminova2.0@gmail.com'
                 )
