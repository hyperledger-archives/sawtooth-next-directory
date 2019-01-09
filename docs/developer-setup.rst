===============
Developer Setup
===============

The purpose of this document is to get all developers on the same page for development when beginning so all
dependencies install properly in a virtual environment and all IDE interpreters run off the same environment.

Windows users: The files in this repo use unix-style line wraps. Ensure you have git configured such that it checks
out/commits with newlines as-is:

 ::

   git config core.autocrlf

Prerequisites
=============
Python 3.7 and pip are installed: https://www.python.org/downloads/

Docker and docker-compose are installed: https://docs.docker.com/docker-for-windows/install/



Operating System Setups
=======================

- Windows
- Mac/OSX
- Linux



-------
Windows
-------

Docker:
    Ensure all required drives are shared with Docker

        A. Right click Docker on Task Tray
        B. Select "Settings"
        C. Select "Shared Drives"
        D. Check "D" (as well as any others that show up)
        E. Click "Apply"

Other Tools:
    1. Git-bash must be installed: https://git-scm.com/downloads
    2. Git-bash will conflict with the 64-bit version of Cyqwin. Windows users must uninstall if present and instead install the 32-bit version of Cygwin: https://cygwin.com/install.html
    3. Run the Cygwin installer again and install the 64-bit versions of libtool, automake, and pkgconfig.
    4. Run ``echo 'export PATH="$PATH:/c/cygwin/bin"' > ~/.bashrc`` in git-bash to access those tools from git-bash. 
    5. Add ``C:\cygwin\bin`` to your Windows PATH variable as well.
    6. Add ``COMPOSE_CONVERT_WINDOWS_PATHS=1`` to .env to allow docker-compose to run as per: https://github.com/docker/for-win/issues/1829
    7. Run ``echo 'export PATH="$PATH:/c/Python37"' > ~/.bashrc`` in git-bash to run Python3.7 and pip3 from git-bash.
    8. Restart git-bash to allow the changes to take effect.


Set-up your virtual env:
    1. Navigate to the top level of the project (sawtooth-next-directory)
    2. Run the following:

        ``python -m venv ENV``
    3. To Activate your virtual environment, run:

        ``source ./ENV/scripts/activate``
    
    You should now see '(ENV)' at the beginning of your terminal command line. This indicates you are in your ENV.
    To Deactivate, run the following:
    ``deactivate``


Tar File Dependencies:
    1. Navigate to the "windows-dependencies" folder from the home folder.
    2. Untar "secp256k1-0.13.2-py3.7.egg-info.tar" and "secp256k1.tar"
    3. Move both untarred folders into "\sawtooth-next-directory\ENV\Lib\site-packages"


Setting up Dependencies:
    Prior to setting up dependencies you should activate your virtual env and have automake installed. Automake is to
    help with the installation of secp256k1 as it will error without during installation.

    1. Follow this `solution <https://stackoverflow.com/questions/29846087/microsoft-visual-c-14-0-is-required-unable-to-find-vcvarsall-bat>`_
    to get a C++ support for a couple of dependencies.
    2. Run the following:

        ``pip3 install -r requirements.txt``

    You should now have all dependencies installed within your virtualenv. You can tell by running:

        ``pip freeze -l``

    This will list all of your installed dependencies. You can then deactivate your env, run the same command, and see
    the difference.




-------
Mac/OSX 
-------

Prerequisites:
    Ensure brew is up to date
    Ensure XCode is installed and up to date

Getting Tools:
    1. Run in home directory:
        
        A. ``brew install automake``
        B. ``brew install libtool``
        C. ``brew install pkg-config``
        D. ``python3.7 -m venv ENV``

    2. Activate virtual env

        ``source ENV/bin/activate``

    You should now see '(ENV)' at the beginning of your terminal command line. This indicates you are in your ENV.
    To Deactivate, run the following:
    ``deactivate``

    3. Run the following:

        ``pip3 install -r requirements.txt``

    If you receive errors with a permission denied error with directory creation run with sudo:

        ``sudo pip install -r requirements.txt``
    
    You should now have all dependencies installed within your virtualenv. You can tell by running

        ``pip freeze -l``
    
    This will list all of your installed dependencies. You can then deactivate your env, run the same command, and see
    the difference.


-----
Linux
-----

Getting Tools:
    1. Run in home directory:
        
        A. ``apt-get install automake``
        B. ``apt-get install libtool``
        C. ``apt-get install pkg-config``
        D. ``python3.7 -m venv ENV``

    2. Activate virtual env

        ``source ENV/bin/activate``

    You should now see '(ENV)' at the beginning of your terminal command line. This indicates you are in your ENV.
    To Deactivate, run the following:
    ``deactivate``

    3. Run the following:

        ``pip3 install -r requirements.txt``

    If you receive errors with a permission denied error with directory creation run with sudo:

        ``sudo pip install -r requirements.txt``
    
    You should now have all dependencies installed within your virtualenv. You can tell by running

        ``pip freeze -l``
    
    This will list all of your installed dependencies. You can then deactivate your env, run the same command, and see
    the difference.


IDE Interpreter setup
=====================
This will of course change between each IDE for the example process I will be using PyCharm.  You need to set your
Interpreter path to point at the python in the ENV folder in the top level directory. If you are using PyCharm the
following steps will work for you; if not please adapt to your IDE.  Go to
http://pylint.pycqa.org/en/latest/user_guide/ide-integration.html#pylint-in-pycharm for easy integration with different interpreters.

 1. Select Preferences > Project: saw-tooth-next-directory > Project Interpreter
 2. Click the 'gear' image in the top corner and click 'Add..'
 3. Select 'Existing Environment' and in 'Interpreter:' from the drop down select the path that leads to your 'ENV'. This will automatically be detected and be in the dropdown.
 4. Select 'OK'
 5.  You will see your new interpreter with all the dependencies listed. 

IDE pylint setup
================
Once again this will be using PyCharm as an example.  This is to unite all pep8 pylint errors under the same standards
across IDEs.  Our common standards and what to ignore and pass is defined in setup.cfg.  That means that when running
pylint you need to add the argument '--rcfile=setup.cfg'.  Lets set this up now.

 1. In PyCharm go to Preferences > Plugins  and search for Pylint
 2. Click on the plugin named Pylint, select Download and Install and click on restart PyCharm when prompted (You may have to click ok afterward and leave before it will restart)
 3. Select Preferences > Pylint
 4. For path to executable put the path to you virtual env's pylint (i.e. ENV/bin/pylint)
 5. For Arguments put --rcfile=setup.cfg

You are now done.  If you want it easily available for selection under External tools go to
http://pylint.pycqa.org/en/latest/user_guide/ide-integration.html#pylint-in-pycharm and follow the section
'Using External Tools'

Client Setup
================
 1. Run the following:
 ::
   # Install Yarn and Gulp globally
   npm install -g yarn gulp

 2. Install NPM packages:
 ::
   # Install NPM packages and create yarn.lock
   cd client && yarn

 3. Build Semantic UI (https://react.semantic-ui.com/usage/):
 ::
   # Build Semantic UI
   yarn build:semantic

Client Development
   # Watch for changes to Semantic source
   yarn watch:semantic

