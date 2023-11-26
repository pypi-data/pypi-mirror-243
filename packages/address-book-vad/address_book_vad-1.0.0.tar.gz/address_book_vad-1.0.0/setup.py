from setuptools import setup, find_namespace_packages

setup(
    name='address_book_vad',
    version='1.0.0',
    description='address book + note book + calculator',
    url='https://github.com/VadimTrubay/address_book_vad',
    author='TrubayVadim',
    author_email='vadnetvadnet@ukr.net',
    license='MIT',
    include_package_data=True,
    packages=find_namespace_packages(),
    install_requires=['colorama', 'numexpr'],
    entry_points={'console_scripts': ['address_book_vad=address_book_vad.main:main']}
)