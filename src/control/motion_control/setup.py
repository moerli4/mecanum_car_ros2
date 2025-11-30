from setuptools import find_packages, setup

package_name = "motion_control"

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
    maintainer="mo",
    maintainer_email="moritzgeissler04@gmail.com",
    description="Package for basic motion control",
    license="All rights reserved",
    extras_require={
        "test": [
            "pytest",
        ],
    },
    entry_points={
        "console_scripts": [
            "motion_control = motion_control.motion_control:main",
        ],
    },
)
