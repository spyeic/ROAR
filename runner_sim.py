import logging
from pathlib import Path

from ROAR_Sim.configurations.configuration import Configuration as CarlaConfig
from ROAR_Sim.carla_client.carla_runner import CarlaRunner

from ROAR.configurations.configuration import Configuration as AgentConfig
from ROAR.agent_module.pure_pursuit_agent import PurePursuitAgent
from ROAR.agent_module.special_agents.recording_agent import RecordingAgent
from ROAR.agent_module.pid_agent import PIDAgent
from ROAR.agent_module.occu_map_demo_driving_agent import OccuMapDemoDrivingAgent
from ROAR.agent_module.occupancy_map_agent import OccupancyMapAgent
from ROAR.agent_module.forward_only_agent import ForwardOnlyAgent
from ROAR.agent_module.rl_pid_agent import RLPIDAgent


def main():
    """Starts game loop"""
    agent_config = AgentConfig.parse_file(Path("./ROAR_Sim/configurations/agent_configuration.json"))
    carla_config = CarlaConfig.parse_file(Path("./ROAR_Sim/configurations/configuration.json"))

    carla_runner = CarlaRunner(carla_settings=carla_config,
                               agent_settings=agent_config,
                               npc_agent_class=PurePursuitAgent)
    try:
        my_vehicle = carla_runner.set_carla_world()
        # agent = ForwardOnlyAgent(vehicle=my_vehicle, agent_settings=agent_config)
        # agent = PurePursuitAgent(vehicle=my_vehicle, agent_settings=agent_config)
        # agent = RecordingAgent(vehicle=my_vehicle, agent_settings=agent_config)
        # agent = PIDAgent(vehicle=my_vehicle, agent_settings=agent_config)

        # agent = OccuMapDemoDrivingAgent(vehicle=my_vehicle, agent_settings=agent_config)
        agent = OccupancyMapAgent(vehicle=my_vehicle, agent_settings=agent_config)
        # agent = RLPIDAgent(vehicle=my_vehicle, agent_settings=agent_config)

        carla_runner.start_game_loop(agent=agent, use_manual_control=False)
    except Exception as e:
        logging.error(f"Something bad happened during initialization: {e}")
        carla_runner.on_finish()
        logging.error(f"{e}. Might be a good idea to restart Server")


if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s - %(asctime)s - %(name)s '
                               '- %(message)s',
                        datefmt="%H:%M:%S",
                        level=logging.DEBUG)
    import warnings
    warnings.filterwarnings("ignore", module="carla")
    main()
