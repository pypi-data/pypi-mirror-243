

sumo_docker
-----------

This module provides an interface to a dockerized Sumo simulation
and handles all docker-related operations. The communication with the Sumo simulation
works via an RPC interface that is implemented in :py:class:`sumocr.sumo_docker.rpc.sumo_client.SumoRPCClient`.

.. automodule:: sumocr.sumo_docker.interface.docker_interface

``SumoInterface`` class
^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: SumoInterface
   :members:
   :member-order: bysource

.. automodule:: sumocr.sumo_docker.rpc.sumo_client

``SumoRPCClient`` class
^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: SumoRPCClient
   :members:
   :member-order: bysource