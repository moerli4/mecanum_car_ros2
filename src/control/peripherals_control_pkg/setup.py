from setuptools import find_packages, setup

package_name = 'peripherals_control_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='mo',
    maintainer_email='moritzgeissler04@gmail.com',
    description='Package for any peripheral stuff like remotes and controllers etc',
    license='All rights reserved',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'controller_to_twist = peripherals_control_pkg.controller_to_twist:main',
        ],
    },
)
