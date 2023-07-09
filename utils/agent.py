from utils.environment import env_tree
from utils.environment import tree_node
import json
from typing import Union , Tuple
from pathlib import Path
import datetime

class Agent:
    
    def __init__(self, json : Union[str , Path]):
        
        # self.tree = env_tree()
        self.current_conversation = None
        self.memory_stream = []
        self.load_json(json)
        self.knows_tree = env_tree(places = [self.location])
        
    
    def load_json(self , json_file : Union[str , Path]):
        with open(json_file) as f:
            agent_info = json.load(f)

        self.name = f"{agent_info['First name']} {agent_info['Last name']}"
        self.age = agent_info['Age']
        self.innate_tendency = agent_info['Innate tendency']
        self.learned_tendency = agent_info['Learned tendency']
        self.currently = agent_info['Currently']
        self.lifestyle = agent_info['Lifestyle']
        self.location = agent_info['location']
        self.plan = agent_info['Plan']

    def update_observation(self , observations : list[str] , time : datetime):

        for observation in observations:
            self.memory_stream.append({
                "observation" : observation,
                "time" : time,
                "last_use" : 0,
            })

    def update_knows_places(self , places : list[str]):
        self.knows_tree.add_places(places)

    def get_memory_stream(self , num : int) -> str:

        ret = ""
        
        for i in range(-min(num , len(self.memory_stream)) , 0):
            event = self.memory_stream[i]
            ret += f"[{event['time']}] : {event['observation']}  / Last Use {event['last_use']}\n"

        return ret            

        

    def __str__(self) -> str:
        ret = f"""-- {self.name} / Age : {self.age} --
Personality and Lifestyle : 
    Innate tendency : {self.innate_tendency}
    Learned tendency : {self.learned_tendency}
    Currently : {self.currently}
    Lifestyle : {self.lifestyle}
Latest 50 memory :
{self.get_memory_stream(50)}
------------------"""
                
        return ret