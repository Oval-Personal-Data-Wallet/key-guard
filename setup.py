from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()
setup(
    name='key_guard',
    version='0.1',
    author='Jerry Buaba',
    author_email='buabajerry@gmail.com',
    license='MIT',
    description='A CLI tool to help you guard your sensitive information from being pushed to a remote repository',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/buabaj/key-guard',
    py_modules=['key_guard'],
    packages=find_packages(),
    install_requires=[requirements],
    python_requires='>=3.8',
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    entry_points='''
        [console_scripts]
        key-guard=key_guard:cli
    '''
)
