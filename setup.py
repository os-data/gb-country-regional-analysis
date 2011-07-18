from setuptools import setup, find_packages

setup(
    name = 'cratools',
    version = '0.0.1',
    packages = find_packages(),
    install_requires = [
        'datautil==0.4',
        'xlrd==0.7.1'
    ],
    entry_points = {
        'console_scripts': [
            'cratools = cratools.command:main',
        ],
    },
    zip_safe = False
)
