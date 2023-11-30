from setuptools import find_packages, setup
setup(
    name='rasteric',
    packages=find_packages(include=['rasteric']),
    version='0.0.2beta',
    description='Python Geospatial Library',
    author='Thai Tran',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)