from setuptools import setup, find_packages

setup(
    name='tree_control',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    description='A reusable Django tree app.',
    long_description=open('README.md').read(),
    url='http://example.com/myapp',
    author='Neo Jabin',
    author_email='neo.j.jabin@gmail.com',
    license='MIT',
    install_requires=[
        'Django>=3.0',
        # other dependencies...
    ],
)
