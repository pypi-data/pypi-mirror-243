.. _example-index:

========================================
Examples for using the interface
========================================

Run interactive CommonRoad scenarios
========================================

To run a motion planner on interactive
scenarios from the CommonRoad database, denoted by the suffix :code:`I`,
please use the scripts provided in the `commonroad-interactive-scenarios
repository <https://gitlab.lrz.de/tum-cps/commonroad-interactive-scenarios>`_ and have a look at the tutorials
`tutorials <https://commonroad.in.tum.de/sumo-interface>`_.


Run with custom scenarios
==========================

Further options for the interface can be found in the sumo-interface config file `sumocr/sumo_config/default.py`.
When creating configuration files for simulations, they need to be derived from this class.
However, creating your own scenarios for simulation is currently not recommended.
In the future, we will provide additional tools for the convenient creation of scenarios.

.. _howto_local_sumo:

Run Simulation
--------------

This option requires the additional installation of SUMO as described in :ref:`installation`.

The following example shows how the interface can be integrated into an existing trajectory planner.
Make sure the folder `example_scenarios`, which can be found in the repository, was added to the python path.
Plug in a trajectory planner and run:

.. code-block:: python

    import copy
    import os
    from typing import List
    import inspect

    from commonroad.scenario.trajectory import State
    from commonroad.common.file_reader import CommonRoadFileReader
    from commonroad.common.file_writer import CommonRoadFileWriter

    from sumocr.interface.sumo_simulation import SumoSimulation
    from sumocr.maps.sumo_scenario import ScenarioWrapper

    from example_scenarios.a9.scenario_config import Conf

    config = Conf()
    scenario_path = os.path.dirname(inspect.getfile(Conf))

    cr_file = os.path.abspath(
        os.path.join(scenario_path,
                     config.scenario_name + '.cr.xml'))

    # Change this as you see fit
    output_folder = os.path.dirname(cr_file)
    print("Reading file:", cr_file, " Outputing to folder:", output_folder)

    scenario, _ = CommonRoadFileReader(cr_file).open()
    wrapper = ScenarioWrapper.init_from_scenario(config, scenario_path, cr_map_file=cr_file)

    sumo_sim = SumoSimulation()
    sumo_sim.initialize(config, wrapper)

    for t in range(config.simulation_steps):
        ego_vehicles = sumo_sim.ego_vehicles
        commonroad_scenario = sumo_sim.commonroad_scenario_at_time_step(
            sumo_sim.current_time_step)

        # plan trajectories for all ego vehicles
        for id, ego_vehicle in ego_vehicles.items():
            current_state = ego_vehicle.current_state

            # plug in a trajectory planner here, currently staying on initial state
            next_state = copy.deepcopy(current_state)
            next_state.time_step = 1
            ego_trajectory: List[State] = [next_state]

            ego_vehicle.set_planned_trajectory(ego_trajectory)

        sumo_sim.simulate_step()

    sumo_sim.stop()

    print("Done simulating")
    simulated_scenario = sumo_sim.commonroad_scenarios_all_time_steps()
    CommonRoadFileWriter(simulated_scenario,
                         None,
                         author=scenario.author,
                         affiliation=scenario.affiliation,
                         source=scenario.source,
                         tags=scenario.tags,
                         location=scenario.location).write_scenario_to_file(
        os.path.join(
            output_folder,
            config.scenario_name + ".simulated.xml"),
        overwrite_existing_file=True)

