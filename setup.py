from setuptools import setup, find_packages
from html5audio import __version__

setup(
    name='html5audio-sandbox',
    version=__version__,
    author='Michel Albert',
    author_email='michel@albert.lu',
    packages = find_packages(),
    include_package_data = True,
    zip_safe = False,
    install_requires = ['flask'],
    license='BSD',
    long_description=open('README.rst').read(),
    entry_points = {
        'console_scripts': [
            'webui = html5audio.webui:main'
            ]
        }
)
