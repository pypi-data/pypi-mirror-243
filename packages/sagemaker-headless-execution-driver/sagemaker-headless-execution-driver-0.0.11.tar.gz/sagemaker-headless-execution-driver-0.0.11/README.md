# SageMaker  Headless Notebook Execution Driver
This package is used to host headless execution manager/driver logic and its dependent scripts for notebook execution. Other types of headless execution like python script, java jar based job types could be supported later by adding new types of manager/driver.

## Description

The sagemaker_headless_execution_driver facilitates running SageMaker notebook jobs in a headless mode. It integrates seamlessly with the Amazon SageMaker Jupyter Scheduler and provides the necessary mechanisms to execute Jupyter notebooks as automated jobs.

## Features
* Executes Jupyter notebooks as SageMaker Training Jobs.
* Compatible with custom SageMaker images.
* Extensible and easily integrable with other SageMaker tooling

## Installation
To install the package:

```
pip install sagemaker-headless-execution-driver

```
For Conda users: 
```
conda install -c conda-forge sagemaker-headless-execution-driver

```

## Dependecies
* IPython
* Papermill

## License
This project is licensed under the terms of the Apache 2.0 license. See LICENSE for more details.
