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
        self.plans = agent_info['Plan']
        
        self.actions = agent_info['action']

    def update_observation(self , observations : list[str] , time : datetime):

        for observation in observations:
            self.memory_stream.append({
                "observation" : observation,
                "time" : time,
                "last_use" : 0,
                "importantance" : 0
            })

    def update_knows_places(self , places : list[str]):
        self.knows_tree.add_places(places)

    def get_memory_stream(self , num : int) -> str:

        ret = ""
        
        for i in range(-min(num , len(self.memory_stream)) , 0):
            event = self.memory_stream[i]
            ret += f"[{event['time']}] : {event['observation']}  / Last Use {event['last_use']}\n"

        return ret            
    
    def __gen_plan__(self , date):
        
        summary = self.__gen_summary__(date)
        prev_plan = ""

        for idx , plan in enumerate(self.plans[date]):
            prev_plan += f"{idx+1}) {plan}, "

        prompt = (
            f"Name: {self.name} (age: {self.age})\n"
            f"Innate traits: {self.innate_tendency}\n"
            f"{summary},{prev_plan}\n"
            f"Today is {date}. Here is {self.name}’s plan today in broad strokes: 1)\n"
            )
        
        return prompt

    def __gen_summary__(self , date):

        prompt = (
            f"How would one describe {self.name}'s core characteristics given the following statements?\n"
            )
        
        for action in self.actions[date]:
            prompt += f"- {action['action']}\n"

        return "summary"
    
    def __gen_retriebal__():
        pass
        

        

    def __str__(self) -> str:
        ret = (
            f"-- {self.name} / Age : {self.age} --\n"
            "Personality and Lifestyle : \n"
            f"Innate tendency : {self.innate_tendency}\n"
            f"Learned tendency : {self.learned_tendency}\n"
            f"Currently : {self.currently}\n"
            f"Lifestyle : {self.lifestyle}\n"
            "Latest 50 memory :\n"
            f"{self.get_memory_stream(50)}\n"
        )
                
        return ret