from setuptools import find_packages, setup

package_name = 'motor_pkg'

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
    maintainer='Moritz Geissler',
    maintainer_email='moritz.geissler@tum.de',
    description='Package for controlling the motor speeds',
    license='All rights reserved',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "motor_control = motor_pkg.motor_ctrl:main",
        ],
    },
)
