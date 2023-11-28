
from setuptools import setup, find_packages

setup(
    name='pyx-react',
    version='0.0.3-alpha.1',
    description='A framework that enables Python objects to be easily rendered on a web server',
    author='Kim Changyeon',
    author_email='cykim8811@snu.ac.kr',
    url='https://github.com/cykim8811/pyx',
    python_requires='>=3.7',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    package_data={'': ['assets/*']},
    include_package_data=True,
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    zip_safe=False,
    license='MIT'
)

