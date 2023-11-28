from setuptools import find_packages, setup

setup(
    name='netbox_autonames',
    version='0.2',
    description='Auto-generate names for devices in NetBox based on their role.',
    url='https://github.com/jaannnis/netbox_autonames',
    author='jannis',
    license='AGPLv3',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
