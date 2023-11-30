interface
==========

This module provides an interface between a local Sumo
installation and an ego vehicle steered by a motion planner.


.. automodule:: sumocr.interface.sumo_simulation

Sumo Simulation
----------------


``SumoSimulation`` class
^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: SumoSimulation
   :members:
   :member-order: bysource


.. automodule:: sumocr.interface.ego_vehicle

Ego Vehicle
----------------


``EgoVehicle`` class
^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: EgoVehicle
   :members:
   :member-order: bysource


Helper Functions
------------------

.. automodule:: sumocr.interface.util

.. autofunction:: get_route_files
.. autofunction:: initialize_id_dicts
.. autofunction:: generate_cr_id
.. autofunction:: cr2sumo
.. autofunction:: sumo2cr
