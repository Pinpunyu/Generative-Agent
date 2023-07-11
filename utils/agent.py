from utils.environment import env_tree
from utils.environment import tree_node
from utils.retrieval import Retrieval
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

        importantance = Retrieval.get_importantance(observations)
        for idx , observation in enumerate(observations):
            self.memory_stream.append({
                "observation" : observation,
                "observed_entity" : observation.split(" ")[0],
                "time" : time,
                "last_use" : datetime.datetime(2023,1,1,0,0,0),
                "importantance" : importantance[idx]
            })

    def update_knows_places(self , places : list[str]):
        self.knows_tree.add_places(places)

    def get_memory_stream(self , num : int) -> str:

        ret = ""
        
        for i in range(-min(num , len(self.memory_stream)) , 0):
            event = self.memory_stream[i]
            ret += f"[{event['time']}] : {event['observation']}  / Last Use {event['last_use']}\n"

        return ret            
    
    def __gen_plan__(self , date : datetime):
        ### gen the agent's plan ###
        # TODO recursive / summarize prev day

        # summary = self.__gen_summary__(str(date - datetime.timedelta(days=1)))
        prev_plan = ""

        for idx , plan in enumerate(self.plans[str(date - datetime.timedelta(days=1))]):
            prev_plan += f"{idx+1}) {plan}, "

        prompt = (
            f"Name: {self.name} (age: {self.age})\n"
            f"Innate traits: {self.innate_tendency}\n"
            # need prev day summary
            f",{prev_plan}\n"
            f"Today is {date}. Here is {self.name}’s plan today in broad strokes: 1)\n"
            )
        
        plans = "1)sleep , 2) go to school"


        self.plans[str(date)] = [i.split(')')[-1] for i in plans.split(",")]

    def __gen_summary_description__(self , time:datetime) -> str:
        ### gen [Agent’s Summary Description] ###
        prompt = (
            f"How would one describe {self.name}'s core characteristics given the following statements?\n"
            )
        
        retrieval = self.__gen_retrieval__(f"{self.name}'s core characteristics." , 10 , time)

        for observation in retrieval:
            prompt += f"- {observation['observation']}\n"

        return "summary"
    
    def __gen_retrieval__(self , query : str, pick_num : int, time : datetime) -> list[dict]:
        ### gen top {pick_num} memory of retrieval score ###
        # TODO update last_use
        sorted_memeory_stream = Retrieval.get_retrieval(self.memory_stream , query, time)
        return sorted_memeory_stream[:pick_num]
        
    def __gen_reflection__(self):
        ### reflection ###
        # TODO add into memory


        # memory = self.__gen_retrieval__(query, 50 , time)
        # retrieval = ''.join([f"{idx+1}. {i['observation']}\n" for idx , i in enumerate(memory)])
        recent_memeory_stream = ''.join([f"{idx+1}. {i['observation']}\n" for idx , i in enumerate(self.memory_stream[:100])])

        prompt = (
            f"Statements about {self.name}\n"
            f"{recent_memeory_stream}"
            "What 5 high-level insights can you infer from the above statements?\n"
            "(example format: insight(because of 1, 5, 3))\n"
        )
    
        # print(prompt)
        # return "Klaus Mueller is dedicated to his research on gentrification (because of 1, 2, 8, 15)"
    
    def __gen_reaction__(self , observation , date):
        ### from observation decide whether to react ###
        # TODO retrieval A & B's summary / add into action


        query_A = f"What is {self.name}'s relationship with the {observation['observed_entity']} ?"
        query_B = f"{observation['observation']}"

        memory = self.__gen_retrieval__(query_A , 10 , date) + self.__gen_retrieval__(query_B , 10 , date)
        statements = [i['observation'] for i in memory]
        
        # summary = self.__gen_summary__(statements)
        # print(statement)

        prompt = (
            "[Agent's Summary Description]"
            f"It is {str(date)}"
            f"{self.name}'s status: <status>"
            f"Observation: {observation}"
            # need retrieval A & B's summary
            f"Summary of relevant context from {self.name}'s memory: "
            "Should <Name> react to the observation, and if so, what would be an appropriate reaction?"
        )
    
    def __gen_dialogue__(self):
        # TODO all
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
    