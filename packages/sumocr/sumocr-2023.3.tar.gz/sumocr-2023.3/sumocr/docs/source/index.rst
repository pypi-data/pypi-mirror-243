.. sumo_interface documentation master file, created by
   sphinx-quickstart on Mon May 27 10:09:34 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

===========================================
CommonRoad-SUMO interface documentation
===========================================

Testing motion planning algorithms for automated vehicles in realistic simulation environments accelerates their development compared to performing real-world test drives only.
In this work, we combine the open-source microscopic traffic simulator SUMO with our software framework CommonRoad to test motion planning of automated vehicles.
Since SUMO is not originally designed for simulating automated vehicles, this interface is designed for exchanging the trajectories of vehicles controlled by a motion planner
and the trajectories of other traffic participants between SUMO and CommonRoad.

To run interactive scenarios fr the CommonRoad database, please use the scripts provided in this repository https://gitlab.lrz.de/tum-cps/commonroad-interactive-scenarios.

More about the interface can be found in our `paper <http://mediatum.ub.tum.de/doc/1486856/344641.pdf>`_:

Moritz Klischat, Octav Dragoi, Mostafa Eissa, and Matthias Althoff, *Coupling SUMO with a Motion Planning Framework for Automated Vehicles*, SUMO 2019: Simulating Connected Urban Mobility



User manual
=============================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   install/install.rst
   install/example.rst
   api/index.rst


Changelog
=============================================

Changes compared to version 2021.4:

- improved speed of the SUMO co-simulation
- removed map conversion function that are now available in the commonroad scenario designer



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Contact information
=====================

:Website: `http://commonroad.in.tum.de <https://commonroad.in.tum.de/>`_
:Email: `commonroad@lists.lrz.de <commonroad@lists.lrz.de>`_
