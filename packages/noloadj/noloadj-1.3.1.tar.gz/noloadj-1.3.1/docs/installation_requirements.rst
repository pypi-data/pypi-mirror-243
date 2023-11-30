NoLOAD_Jax Installation
=======================

.. contents::
    :depth: 1
    :local:
    :backlinks: top

Installing NoLOAD_Jax
---------------------

Python 3.8.0
************
Please use Python 3.8.0 for the project interpreter:
`Python 3.8 <https://www.python.org/downloads/release/python-380/>`_


pip install noload
******************
Please install NoLOAD_Jax Lib with pip using on of the following the command prompt:

    - **If you are working on a virtual environment on Linux**::

        pip install noloadj

    - **If you want a local installation or you are not admin**::

        pip install --user noloadj

    - **If you are admin on Linux**::

        sudo pip install noloadj

Then, you can download (or clone) the NoLOAD benchmark folder (repository) at :
`NoLOAD Examples`_
Make sure that the name of the examples folder is: "noload_benchmarks_open".

Launch the examples (with Pycharm for instance) to understand how the NoLOAD_Jax Lib works.

**Enjoy your time using NoLOAD_Jax !**


Other installation requirements
-------------------------------
If the music was enough catchy, the following libraries should be
already installed.
If not, increase the volume and install the following libraries
with the help below.


    - **Jax >= 0.4.18**
    - **Jaxlib >= 0.4.18**

    Jax is a Python automatic differentiation :
    `Jax <https://github.com/google/jax>`_

    - **Matplotlib >= 3.0**

    Matplotlib is a Python 2D plotting library :
    `Matplotlib <https://matplotlib.org/>`_

    - **Scipy >= 1.2**

    Scipy is a Python-based ecosystem of open-source software for mathematics, science, and engineering :
    `Scipy <https://www.scipy.org/>`_

    - **Pandas >= 1.3.5**

    Pandas is a Python library for open source data analysis and manipulation tool :
    `Pandas <https://pandas.pydata.org/>`_

    - **Tkinter >= 0.1.0**

    The tkinter package ("Tk interface") is the standard Python interface to the Tcl/Tk GUI toolkit :
    `Tkinter <https://docs.python.org/fr/3/library/tkinter.html>`_

    - **Openpyxl >= 3.1.2**

    Openpyxl is a Python library to read/write Excel 2010 xlsx/xlsm files :
    `Openpyxl <https://openpyxl.readthedocs.io/en/stable/>`_

    - **Cyipopt >= 1.2.0**

    Cyipopt is a Python wrapper for the Ipopt optimization package :
    `Cyipopt <https://cyipopt.readthedocs.io/en/stable/index.html>`_

    ---
    **Command lover**
    --- ::

        pip install <library_name>==version

    If required, the command to upgrade the library is ::

        pip install --upgrade <library_name>

    ---
    **Pycharm lover**
    ---

    Install automatically the library using pip with Pycharm on "File", "settings...", "Project Interpreter", "+",
    and choosing the required library


GPU
---
As it uses the JAX library, NoLOAD_Jax can run on CPU (Central Processor Unit) or GPU (Graphics Processor Unit), where GPU offers better performances than CPU.
On Windows, only CPU can be used. To use GPU you may run NoLOAD on Ubuntu.
If you want to use GPU, you need to install CUDA and CuDNN on your computer then tape on Pycharm terminal (where 0.3.XX is your JAX version):
--- ::
    pip install --upgrade pip
    pip install --upgrade jax jaxlib==0.3.XX+cuda111 -f https://storage.googleapis.com/jax-releases/jax_releases.html


If you use GPU, you need to put these lines at the beginning of your "optimization" file to avoid memory issues :
--- ::
    import os
    os.environ['XLA_PYTHON_CLIENT_PREALLOCATE']='false'
    os.environ['XLA_PYTHON_CLIENT_MEM_FRACTION']='0.50'

To have more information, please have a look to :  https://jax.readthedocs.io/en/latest/installation.html

IPOPT Algorithm
---------------
NoLOAD_Jax runs with SLSQP optimization algorithm from Scipy.
To install IPOPT algorithm, please install an Anaconda environment and run this command on a terminal :
--- ::
    conda install -c conda-forge cyipopt


Install NoLOAD_Jax as a developer
---------------------------------
Installation as a developer and local branch creation
******************************************************

1. Create a new folder in the suitable path, name it as you wish for instance : NoLOAD_Jax

2. Clone the NoLOAD_Jax library repository

    ---
    **Command lover**
    --- ::

           git clone https://gricad-gitlab.univ-grenoble-alpes.fr/design_optimization/NoLoad_v2.git

    ---
    **Pycharm lover**
    ---

    | Open Pycharm
    | On the Pycharm window, click on "Check out from version control" then choose "Git".
    | A "clone repository" window open.
    | Copy the following link into the URL corresponding area:

        https://gricad-gitlab.univ-grenoble-alpes.fr/design_optimization/NoLoad_v2.git

    | Copy the path of the new folder created just before.
    | Test if the connection to the git works and if it works click on "Clone".
    | Once NoLOAD_Jax is cloned, you must be able to see the full NoLOAD library on Pycharm
      or on another development environment.

    If the connection does not work and if you are working with local protected network,
    please try again with the wifi.

3. First, choose or change your project interpreter

    ---
    **Pycharm lover**
    ---

    Click on the yellow warning link or go to "File", "settings...", "Project Interpreter"

    You can:

    - either select the "Python 3.8" project interpreter but you may change the version
      of some library that you could use for another application.

    - either create a virtual environment in order to avoid this problem (recommended).
     | Click on the star wheel near the project interpreter box.
     | Click on "add...".
     | Select "New environment" if it not selected.
     | The location is pre-filled, if not fill it with the path of the folder as folder_path/venv
     | Select "Python 3.8" as your base interpreter
     | Then click on "Ok"

4. You can install the library on developing mode using the following command in command prompt
once your are located it on the former folder.
If you are calling NoLOAD_Jax library in another project, the following command enables you to refer to the NoLOAD library you are developing:

        python setup.py develop

5. If it is not already done, install the library requirements.

    ---
    **Command lover**
    --- ::

            pip install <library_name>

    If required, the command to upgrade the library is ::

            pip install --upgrade <library_name>

    ---
    **Pycharm lover**
    ---

    You should still have a yellow warning.
    You can:

    - install automatically the libraries clicking on the yellow bar.

    - install automatically the library using pip with Pycharm on "File", "settings...", "Project Interpreter", "+",
      and choose the required library as indicated in the Library Installation Requirements
      part.

6. Finally, you can create your own local development branch.

    ---
    **Command lover**
    --- ::

        git branch <branch_name>

    ---
    **Pycharm lover**
    ---

    | By default you are on a local branch named master.
    | Click on "Git: master" located on the bottom write of Pycharm
    | Select "+ New Branch"
    | Name the branch as you convenience for instance "dev_your_name"

7. Do not forget to "rebase" regularly to update your version of the library.

    ---
    **Command lover**
    --- ::

        git rebase origin

    ---
    **Pycharm lover**
    ---

    To do so, click on your branch name on the bottom write of the Pycharm window
    select "Origin/master" and click on "Rebase current onto selected"

If you want to have access to examples and study cases,
download (or clone) the NoLOAD Examples folder (repository) from :
`NoLOAD Examples`_ .    \
Make sure that the name of the examples folder is: "noload_benchmarks_open".


**Enjoy your time developing NoLOAD_Jax!**


.. _NoLOAD Gitlab: https://gricad-gitlab.univ-grenoble-alpes.fr/design_optimization/NoLoad_v2
.. _NoLOAD Examples: https://gricad-gitlab.univ-grenoble-alpes.fr/design_optimization/noload_benchmarks_open/-/tree/noload_version2
