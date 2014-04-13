from setuptools import setup, find_packages

setup(
    name = 'cratools',
    version = '0.0.1',
    packages = find_packages(),
    install_requires = [
        'datautil',
        'xlrd'
    ],
    entry_points = {
        'console_scripts': [
            'cratools = cratools.command:main',
        ],
    },
    zip_safe = False
)
