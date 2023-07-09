from utils.agent import Agent
from utils.environment import env_tree , tree_node
from pathlib import Path
import datetime
from typing import Union , Tuple

class generative_agents():
    
    def __init__(self , env_json : Union[str , Path], agents_path : Union[str , Path], init_time : datetime = datetime.datetime(2023,1,1,00,00,00,00) , tick :int= 10):
        self.env = env_tree(env_json)
        self.agents : list[Agent] = []
        self.time = init_time
        self.tick = tick
        for agent in Path(agents_path).glob("*.json"):
            self.agents.append(Agent(agent))

    def next_tick(self):
        self.time += datetime.timedelta(seconds=self.tick)

        for agent in self.agents:
            observations , places = self.env.observation(agent.location)
            agent.update_observation(observations , self.time)
            agent.update_knows_places(places)

    
    

