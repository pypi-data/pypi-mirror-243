from setuptools import setup

setup(
    name='grapl-causal',
    version='1.6',
    description='GRAPL: A computational library for nonparametric structural causal modelling, analysis and inference',
    url='https://github.com/max-little/GRAPL',
    author='Max A. Little',
    author_email='maxl@mit.edu',
    license='GNU GPL-3.0',
    packages=['grapl','grapl.test','grapl.ply','grapl.tutorials'],
    package_data={'grapl': ['graphs/*.grapl', 'tutorials/*.ipynb']},
    install_requires=[],
)
