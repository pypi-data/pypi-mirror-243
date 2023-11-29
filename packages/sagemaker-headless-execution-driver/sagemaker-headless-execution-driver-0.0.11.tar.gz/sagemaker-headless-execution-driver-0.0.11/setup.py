import setuptools

from setuptools import find_packages


setuptools.setup(
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "amazon_sagemaker_scheduler=sagemaker_headless_execution_driver.headless_execution:main",
        ]
    },
)
