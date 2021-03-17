from setuptools import setup

setup(
    name='inventory_app',
    packages=['inventory_api'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)