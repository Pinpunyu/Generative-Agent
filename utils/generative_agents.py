from utils.agent import Agent
from utils.environment import env_tree , tree_node
from pathlib import Path
import datetime
from typing import Union , Tuple

class generative_agents():
    
    def __init__(self , env_json : Union[str , Path], agents_path : Union[str , Path], init_time : datetime = datetime.datetime(2023,7,9,00,00,00,00) , tick :int= 10):
        self.env = env_tree(env_json)
        self.agents : dict[str , Agent]  = {}
        self.time = init_time
        self.tick = tick
        for agent in Path(agents_path).glob("*.json"):
            new_agent = Agent(agent)
            self.agents[new_agent.name] = new_agent
            self.env.add_agent(new_agent.location , new_agent.name , "idle")

    def next_tick(self):
        ### system time add tick and all agents update tick ###
        self.time += datetime.timedelta(seconds=self.tick)
        
        # all agent get prev tick observation & places
        for agent in self.agents.values():
            observations , places = self.env.observation(agent.location)
            agent.next_tick(observations, places , self.time , 0.5)

        # clear prev tick's agents location
        self.env.clear_all_agent()

        
        for agent in self.agents.values():
            # update this tick agents location
            self.env.add_agent(agent.location , agent.name , agent.current_action)

            # if agent have conversation , 
            # update the conversation to it's target
            # and swap conversation target
            if agent.current_conversation != None:
                self.agents[agent.current_conversation['target']].current_conversation = agent.current_conversation
                agent.current_conversation['target'] = agent.name
                


    def new_day(self , time):
        for agent in self.agents.values():
            agent.start_of_day(time)
    
    

