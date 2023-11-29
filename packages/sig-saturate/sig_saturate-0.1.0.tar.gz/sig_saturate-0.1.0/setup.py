from setuptools import setup, find_packages

# Read the contents of requirements.txt from package root
# with open('requirements.txt') as f:
#     install_requires = f.read().splitlines()

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='sig_saturate',
    version='0.1.0',
    author='Sudhir Arvind Deshmukh',
    description='Second-Order Lag System with Saturation',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/bokey007/sig_saturate',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'matplotlib',
        'streamlit',
    ],
    entry_points={
        'console_scripts': [
            'sig_saturate.run=sig_saturate.run:run',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)

#how to build test and bublish this pkg

# pip uninstall sig_saturate
# python setup.py sdist bdist_wheel
# pip install ./dist/sig_saturate-0.1.0.tar.gz
# sig_saturate.run
# twine upload dist/*