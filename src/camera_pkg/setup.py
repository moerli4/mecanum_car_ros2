from setuptools import find_packages, setup

package_name = 'camera_pkg'

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
    description='Package for camera control',
    license='All rights reserved',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "camera = camera_pkg.camera:main",
            "servo_control = camera_pkg.servo_ctrl:main",
        ],
    },
)
