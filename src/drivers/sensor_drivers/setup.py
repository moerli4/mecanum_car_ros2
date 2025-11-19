from setuptools import find_packages, setup

package_name = "sensor_drivers"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Moritz Geissler",
    maintainer_email="moritz.geissler@tum.de",
    description="Provides drivers for sensors",
    license="All rights reserved",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "infrared_track_sensor_driver = sensor_drivers.infrared_track_sensor_driver:main",
            "ultrasound_sensor_driver = sensor_drivers.ultrasound_sensor_driver:main",
        ],
    },
)
