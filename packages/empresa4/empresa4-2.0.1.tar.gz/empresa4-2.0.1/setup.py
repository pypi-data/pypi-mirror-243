from setuptools import find_packages, setup

setup(
    name='empresa4',
    packages=find_packages(include=['empresa4', 'empresa4.*']),
    version='2.0.1',
    description='Empresa 4 Library for Laboratorio de Implementación 3',
    author='Gero',
    author_email='geropellicer@gmail.com',  # Type in your E-Mail
    install_requires=['pandas', 'numpy', 'scipy', 'pytest'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==7.4.2'],
    test_suite='tests',
    package_data={
        'empresa4': ['datasets/*'],
    },
)
