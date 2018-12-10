from setuptools import setup

setup(
    name="api_challenge",
    version='0.1',
    url='www.github.com/sthomasp',
    author='Steffan Padel',
    author_email='steffanpadel@gmail.com',
    packages=['api_challenge'],
    install_requires=[
        'flask',
        'pymongo',
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest']
)
