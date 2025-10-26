
# Cushion Technical Task Documentation
 ## Project Setup

This section of the guide will go over the steps required to set up this project and get the tests up and running on your system.

### Running the tests

You will want to start off with cloning this repository in your chosen location. After that, open up a terminal at that directory. Inside that terminal run the following commands:

1. `python -m venv venv` - This will create your virtual environment
2. `pip install -r requirements.txt` - This will install all the project dependencies
3. `pre-commit install` - This will set up all the git hook scripts
4. `pytest` - This will execute all the tests

### Running the tests inside a container (optional)
**Note:** The below steps for running the tests inside a container are not supported on ARM CPUs yet. I will explain in the *Known limitation* section at the bottom of this readme as to why.

These tests can also be run inside a docker container. Below are the steps to get the container up and running. You will need to have docker desktop installed beforehand for these steps.

1. Open Docker Desktop
2. `docker build -t selenium-sweet-shop-test .` - This will build the docker container
3. `docker run --rm selenium-sweet-shop-test` - This will execute the tests against chrome inside the container and teardown the container

#### Running specific tests

Here are a couple of commands to help you run a subset of the tests

- Run a single test using its name - `pytest -k  <test name>`
- Run all tests in a file - `pytest tests/<test file name>.py`

**Note:** If you want to use the commands that run specific tests in a container, you will want to preface the commands with `docker run --rm selenium-sweet-shop-test`. 

So as an example, the command to run the sweet shop login test will be:
`docker run --rm selenium-sweet-shop-test pytest -k test_login`


## Troubleshooting guide

This will outline a couple of the problems that I ran into when setting up this project and how you can resolve them.

### Pre-commit hooks failing to run

The Microsoft store version of python seemingly is known to cause path and permission issue for pip, pre-commit and virtualenv.

Fix: Unstall the microsoft store python version and install Python from the [official Python website](https://www.python.org/downloads/)

If the issue still persists then it may be that the microsoft store python.exe is still on your system and being used. To find that out open up a command line and run:

`where python`

The first python.exe listed is the one being used which in this case will be:

`C:\Users\<user>\AppData\Local\Microsoft\WindowsApps\python.exe`

If you delete that python.exe and then run:

`where python` again then the official python.exe should now the first in the list.

## Known Limitations

As mentioned earlier in the document, the set up for running the test inside a docker container is not compatible on ARM CPUs.
The reason for this is that chrome and the chrome webdriver are both required to be installed to run these tests. ARM and x86 CPUs require different binaries installed on there respective architecture.

The fix for this would be to include another docker file that installs the chrome and chrome-driver binaries compatible with ARM architecture. From what I've researched it looks like there is an image available for this `selenium/standalone-chrome:latest`. So it wouldn't be a massive change to get this to work. I do believe that is out of scope for this task though as the tests do run as expected when not running inside a container and the container steps are optional when executing the tests locally.

**Note:** It is possible to emulate x86 CPUs when running a docker image. The issue with doing that in this case is that emulation is very slow and the tests will fail with an `InvalidSessionIdException` which is commonly due to a sessions being killed/disconnected (I'm assuming due to the slow speed while emulating that the connection to the chrome session dies but that is only my theory based on experimenting with this issue)