from distutils.core import setup

setup(
    name='RobotD',
    version='0.1.0',
    author='Siddharth Nandagopal',
    author_email='sid.nandhan@gmail.com',
    packages=['utils', 'tests'],
    scripts=['bin/manager.py'],
    description='Automation deployment script',
    long_description=open('README.md').read(),
    install_requires=[
        "Python >= 2.7.5",
        "Fabric >= 1.9.0",
    ],
)
