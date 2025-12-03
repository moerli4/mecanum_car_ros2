from setuptools import find_packages, setup

package_name = "camera_control_pkg"

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
    description="Package for basic camera control, such as mediapipe face detection etc",
    license="All rights reserved",
    extras_require={
        "test": [
            "pytest",
        ],
    },
    entry_points={
        "console_scripts": [
            "mediapipe_detection = camera_control_pkg.mediapipe_detection:main",
            "image_handler = camera_control_pkg.image_handler:main",
        ],
    },
)
