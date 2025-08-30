from setuptools import setup, find_packages

setup(
    name='rag_components',
    version='0.1',
    package_dir={'': 'src'},  # Tells setuptools to look in `src/`
    packages=find_packages(where='src')
)
