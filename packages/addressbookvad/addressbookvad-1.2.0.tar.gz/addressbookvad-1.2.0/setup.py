from setuptools import setup, find_namespace_packages

setup(
    name='addressbookvad',
    version='1.2.0',
    description='THIS IS A USEFUL CONTACT BOOK, NOTES BOOK AND CALCULATOR IN ONE APPLICATION',
    url='https://github.com/VadimTrubay/Vad_address_book',
    author='TrubayVadim',
    author_email='vadnetvadnet@ukr.net',
    license='MIT',
    include_package_data=True,
    packages=find_namespace_packages(),
    install_requires=['colorama', 'numexpr'],
    entry_points={'console_scripts': ['addressbookvad=addressbookvad.main:main']}
)