from setuptools import find_packages, setup

package_name = "testing"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Moritz Geissler",
    maintainer_email="moritz.geissler@tum.de",
    description="Package for tests and experiments",
    license="All rights reserved",
    extras_require={},
    entry_points={
        "console_scripts": [
            "test_raspbot_class = testing.test_raspbot_class:main",
        ],
    },
)
