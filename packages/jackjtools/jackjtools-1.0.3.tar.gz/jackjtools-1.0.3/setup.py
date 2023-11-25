from setuptools import setup

setup(
    name='jackjtools',
    version='1.0.3',
    author='tomzmagic',
    author_email='pi_sender@163.com',
    description='jackjtools',
    packages=['jackjtools'],
    package_data={"jackjtools":["*.pyd"]},
    install_requires=[
        'requests'
    ],
)