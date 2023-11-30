.. _install-index:

==============================
Installation
==============================

This interface couples the framework for motion planning of automated vehicles based on CommonRoad_io_ and the traffic simulator SUMO_.

.. _CommonRoad_io: https://pypi.org/project/commonroad-io

.. _SUMO: https://sumo.dlr.de

Prerequisites
=============

The package is written in Python 3.8 and tested on Ubuntu. Install either via

.. code-block:: console

  pip install sumocr

or clone from our gitlab

.. code-block:: console

  git clone https://gitlab.lrz.de/tum-cps/commonroad-sumo-interface.git
  pip install .

.. _installation:

Install SUMO or use dockerized SUMO interface
=============================================

There are two options for interfacing with Sumo:

1) Install Sumo locally as described here: https://sumo.dlr.de/docs/Installing/index.html
2) Use the integrated dockerized version of Sumo. To use dockerized sumo simulation, you have to install `docker <https://docs.docker.com/engine/install/ubuntu/>`_ and follow the `postinstall instructions <https://docs.docker.com/engine/install/linux-postinstall/>`_ as well, to ensure that **you can use the Docker without root privileges**.
   For using this option, simply call the simulation functions with the option :code:`use_docker=True` in the simulation scripts of https://gitlab.lrz.de/tum-cps/commonroad-interactive-scenarios.
