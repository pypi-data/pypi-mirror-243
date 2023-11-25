from setuptools import setup

setup(
    name='jackjtools',
    version='1.0.2',
    author='tomzmagic',
    author_email='pi_sender@163.com',
    description='jackjtools',
    packages=['upload'],
    package_data={"upload":["*.pyd"]},
    install_requires=[
        'requests'
    ],
)