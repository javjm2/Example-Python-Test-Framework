
# Cushion Technical Task Documentation
 ## Project Setup

This section of the guide will go over the steps required to set up this project and get the tests up and running on your system.

### Running the tests

You will want to start off with cloning this repository in your chosen location. After that, open up a terminal at that directory. Inside that terminal run the following commands:

1. `python -m venv venv` - This will create your virtual environment
2. `pip install -r requirements.txt` - This will install all the project dependencies
3. `pre-commit install` - This will set up all the git hook scripts
4`pytest` - This will execute all the tests


### Running the tests inside a container (optional)
`Note: The below steps for running the tests inside a container is not supported on ARM CPUs yet. I will explain further down as to why.`

These tests can also be run inside a docker container. Below are the steps to get the container up and running. You will need to have docker desktop installed beforehand for these steps.

1. Open Docker Desktop
2. `docker build -t selenium-sweet-shop-test .` - This will build the docker container
3. `docker run --rm selenium-sweet-shop-test` - This will execute the tests against chrome inside the container and teardown the container

issue with Microsoft python

## Troubleshooting guide

This will outline a couple of the problems that I ran into when setting up this project and how you can resolve them.

### Pre-commit hooks failing to run

The Microsoft store version of python seemingly is known to cause path and permission issue for pip, pre-commit and virtualenv.

Fix: Unstall the microsoft store python version and install Python from the official Python site

If the issue still persists then it may be that the microsoft store python.exe is still on your system and being used. To find that out open up a command line and run:

`where python`

The first python.exe listed is the one being used which in this case will be:

`C:\Users\<user>\AppData\Local\Microsoft\WindowsApps\python.exe`

If you delete that python.exe and then run:

`where python` again then the official python.exe should now the first in the list.

## Known Limitations