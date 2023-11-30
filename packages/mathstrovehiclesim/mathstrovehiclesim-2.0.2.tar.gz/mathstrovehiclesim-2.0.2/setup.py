from setuptools import find_packages, setup

setup(
    name='mathstrovehiclesim',
    version='2.0.2',
    description='A short description of your package',
    author='Richard Hamilton',
    author_email='r.hamilton@mathstronauts.ca',
    url='https://github.com/your_username/your_package_name',
    include_package_data=True,
    package_data={'': ['images/*',
                       'images/traffic_signs/headlights-off/*',
                       'images/traffic_signs/headlights-on/*',
                       'images/traffic_signs/keep-left/*',
                       'images/traffic_signs/keep-right/*',
                       'images/traffic_signs/school-zone/*',
                       'images/traffic_signs/speed-limit/*',
                       'images/traffic_signs/stop/*',
                       'simulation_cfg.json']},
    packages=find_packages(),
    install_requires=[
        "pygame",
        "easydict",
        "opencv-python"
    ],
    extras_require={
        "dev": [
            "black>=23.1a1",
            "flake8>=3.8.4",
            "pytest>=6.2.5",
            "pytest-cov>=2.11.1",
            "isort>=5.7.0",
            "pre-commit>=2.9.3",
            "ipython>=8.8.0",
            "ipykernel>=6.20.2",
            "ipywidgets>=7.6.3",
            "build",
            "twine",
            "pandas==1.3.5"
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
