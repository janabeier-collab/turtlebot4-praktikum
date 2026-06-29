import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'praktikum_py'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Launch- und Config-Dateien mit installieren:
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Praktikum Mobile Systeme',
    maintainer_email='mobile-robotik@th-luebeck.de',
    description='Python-Paket für das Mobile Robotik Praktikum (TurtleBot 4, ROS 2 Jazzy)',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            # Versuch 1 – Grundlagen
            'hello_node       = praktikum_py.hello_node:main',
            'square_driver    = praktikum_py.square_driver:main',
            'battery_listener = praktikum_py.battery_listener:main',
            # Versuch 3 – Navigation
            'goto_goal        = praktikum_py.goto_goal:main',
        ],
    },
)
