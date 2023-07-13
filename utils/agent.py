from utils.environment import env_tree
from utils.environment import tree_node
from utils.retrieval import Retrieval
from utils.gpt import GPT_react
import json
from typing import Union , Tuple
from pathlib import Path
import datetime

class Agent:
    
    def __init__(self, json : Union[str , Path]):
        
        # self.tree = env_tree()
        self.current_action = None
        self.current_conversation = None
        self.current_plan_idx = 0

        self.memory_stream = []
        self.conversation_history : list[dict] = []
        self.load_json(json)
        self.knows_tree = env_tree(places = [self.location])

    def start_of_day(self , time):
        ### new day init ###
        self.current_plan_idx = 0
        self.current_action = None
        self.current_conversation = None
        self.actions[str(time.date())] = []
        self.__gen_plan__(time)
    
    def next_tick(self , observations : list[str] , places:list[str] , time:datetime , reflect_threshold : float):

        # 1. get observations & update knows places
        current_memory_stream , avg_importantance = self.update_observation(observations , time)
        self.update_knows_places(places)

        # 2. reflection
        if avg_importantance > reflect_threshold:
            self.__gen_reflection__(time , 50)

        # 3. current plan
        plan_time = self.plans[str(time.date())]['detail_plan'][self.current_plan_idx]['time']
        plan_time = datetime.datetime.strptime(plan_time , '%H:%M')
        
        while time.time() > plan_time.time():
            self.current_plan_idx += 1
            plan_time = self.plans[str(time.date())]['detail_plan'][self.current_plan_idx]['time']
            plan_time = datetime.datetime.strptime(plan_time , '%H:%M')

        self.current_action = self.plans[str(time.date())]['detail_plan'][self.current_plan_idx]['plan']


        # 4. dialogue
        if self.current_conversation != None and self.current_conversation['target'] != self.name:
            self.__gen_dialogue__()
        else:
        # 5. react
            for observation in current_memory_stream:
                is_react = self.__gen_reaction__(observation , time)
                if is_react: break

        # 6. move
        self.__agent_move__(places)

        # 7. log actions
        self.actions[str(time.date())].append({
            "time" : str(time.time()) ,
            "action" : self.current_action
        })


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
        self.plans : dict[str , dict[str , list]] = agent_info['Plan']
        
        self.actions = agent_info['action']

    def update_observation(self , observations : list[dict] , time : datetime) -> Tuple[list[dict] , float]:

        importantance = Retrieval.get_importantance(observations)
        current_memory_stream = []

        for idx , observation in enumerate(observations):
            memory = {
                "observation" : observation['observation'],
                "observed_entity" : observation['observation'].split(" ")[0],
                "time" : time,
                "last_used" : datetime.datetime(2023,1,1,0,0,0),
                "importantance" : importantance[idx],
                "entity_type" : observation['type']
            }
            self.memory_stream.append(memory)

        return current_memory_stream , importantance.sum() / len(observations)

    def update_knows_places(self , places : list[str]):
        self.knows_tree.add_places(places)

    def get_memory_stream(self , num : int) -> str:

        ret = ""
        
        for i in range(-min(num , len(self.memory_stream)) , 0):
            event = self.memory_stream[i]
            ret += f"[{event['time']}] : {event['observation']}  / last used {event['last_used']}\n"

        return ret            
    
    def __gen_plan__(self , time : datetime):
        ### gen the agent's plan ###
        ### TODO recursive / agent recent experiences ###

        # summary = self.__gen_summary__(str(date - datetime.timedelta(days=1)))
        prev_plan = ""

        prev_day = (time - datetime.timedelta(days=1)).date()


        for idx , plan in enumerate(self.plans[str(prev_day)]["rough_plan"]):
            prev_plan += f"{idx+1}) {plan}, "

        prompt = (
            f"Name: {self.name} (age: {self.age})\n"
            f"Innate traits: {self.innate_tendency}\n"
            ### !!! TODO agent recent experiences !!! ###
            f",{prev_plan}\n"
            f"Today is {time}. Here is {self.name}'s plan today in broad strokes: 1)\n"
            )
        
        ### !!! TODO LLM output !!! ###
        # plans = GPT_react(prompt)
        plans = "1)sleep at 8:00 am , 2) go to school at 8:30 am"


        self.plans[str(time.date())] = {
            'rough_plan' : [i.split(')')[-1] for i in plans.split(",")],
            'detail_plan' : []
        }
        
        self.__gen_detail_plan__(time)

    def __gen_detail_plan__(self , time):
        ### gen detail plan with finer-grained ###
        ### TODO prompt / recursize ###


        ### !!! TODO LLM output !!! ###
        plan = (
            "4:00 am: grab a light snack, such as a piece of fruit, a granola bar, or some nuts.\n"
            "4:50 pm: take a few minutes to clean up his workspace."
        )

        # plan string operation
        for subplan in plan.split('\n') :
            hour = int(subplan.split(':')[0].strip(' '))
            minute = subplan.split(':')[1].strip(' ')
            action = subplan.split(':')[2]

            plan_time = f"{hour}:{minute[:-2].strip(' ')}" if minute.endswith("am") else f"{hour + 12}:{minute[:-2].strip(' ')}"
            self.plans[str(time.date())]['detail_plan'].append({
                "plan" : action,
                "time" : plan_time
            })

    def __gen_summary_description__(self , time:datetime) -> str:
        ### gen [Agent’s Summary Description] ###
        prompt = (
            f"How would one describe {self.name}'s core characteristics given the following statements?\n"
            )
        
        retrieval = self.__gen_retrieval__(f"{self.name}'s core characteristics." , 10 , time)

        for observation in retrieval:
            prompt += f"- {observation['observation']}\n"

        ### !!! TODO LLM output !!! ###
        return "summary"
    
    def __gen_retrieval__(self , query : str, pick_num : int, time : datetime) -> list[dict]:
        ### gen top {pick_num} memory of retrieval score and update last used ###
        sorted_memeory_stream = Retrieval.get_retrieval(self.memory_stream , query, time)

        for observation in sorted_memeory_stream[:pick_num]:
            self.memory_stream[observation['ori_idx']]['last_used'] = time

        return sorted_memeory_stream[:pick_num]
        
    def __gen_reflection__(self , time , pick_num):
        ### reflection ###
        # pick lastest {pick_num} observation gen reflect and add into memory streams


        # memory = self.__gen_retrieval__(query, 50 , time)
        # retrieval = ''.join([f"{idx+1}. {i['observation']}\n" for idx , i in enumerate(memory)])
        recent_memeory_stream = ''.join([f"{idx+1}. {i['observation']}\n" for idx , i in enumerate(self.memory_stream[:pick_num])])

        prompt = (
            f"Statements about {self.name}\n"
            f"{recent_memeory_stream}"
            "What 5 high-level insights can you infer from the above statements?\n"
            "(example format: insight(because of 1, 5, 3))\n"
        )

        ### !!! TODO LLM output !!! ###
        reflect = "Klaus Mueller is dedicated to his research on gentrification (because of 1, 2, 8, 15)"
        reflection = {'observation': reflect, 'type': 0}

        self.update_observation([reflection] , time)
    
    
    def __gen_reaction__(self , observation : dict , time : datetime) -> Tuple[bool , str]:
        ### from observation decide whether to react ###
        # TODO retrieval A & B's summary / add into action

        agent_summary =  self.__gen_summary_description__(time)
        
        query_A = f"What is {self.name}'s relationship with the {observation['observed_entity']} ?"
        query_B = f"{observation['observation']}"

        memory = self.__gen_retrieval__(query_A , 10 , time) + self.__gen_retrieval__(query_B , 10 , time)

        ### !!! TODO memory summary !!! ###
        summary = "summary"

        
        prompt = (
            f"{agent_summary}\n"
            f"It is {str(time)}\n"
            f"{self.name}'s status: {self.current_action}\n"
            f"Observation: {observation['observation']}\n"
            # need retrieval A & B's summary
            f"Summary of relevant context from {self.name}'s memory: \n"
            f"{summary}"
        )

        react_prompt = prompt + f"Should {self.name} react to the observation, and if so, what would be an appropriate reaction?\n"
            
        ### !!! TODO LLM output !!! ###
        react = "John is asking Eddy about his music composition project"
        ### !!! TODO : Detect LLM output is react or not !!! ###
        is_react = True
        if not is_react:
            return False
        
        if observation['entity_type'] == 0:
            self.current_action = react
        else:
            dialogue_prompt = prompt + ( 
                f"{react}"
                f"What would he say to {observation['observed_entity']}?"
            )
            
            ### !!! TODO LLM output !!! ###
            conversation = "Hello"

            self.current_conversation = {
                "create_time" : str(time),
                "conversation" : f"{self.name} : {conversation}\n",
                "target"  : observation['observed_entity'],
                "target_action" : ""
            }

            ### !!! TODO summary of conversation !!! ###
            summary = "convsersation summary"
            self.current_action = f"conversing about {summary}"

            return True

        

    
    def __gen_dialogue__(self , time) -> bool:
        ### agent dialogue ###
        agent_summary =  self.__gen_summary_description__(time)
        
        query_A = f"What is {self.name}'s relationship with the {self.current_conversation['target']} ?"
        query_B = f"{self.current_conversation['target_action']}"

        memory = self.__gen_retrieval__(query_A , 10 , time) + self.__gen_retrieval__(query_B , 10 , time)
    
        ### !!! TODO memory summary !!! ###
        summary = "summary"
        
        prompt = (
            f"{agent_summary}\n"
            f"It is {str(time)}\n"
            f"{self.name}'s status: {self.current_action}\n"
            f"Observation: {self.current_conversation['target_action']}\n"
            # need retrieval A & B's summary
            f"Summary of relevant context from {self.name}'s memory: \n"
            f"{summary}"
            f"How would {self.name} respond to {self.current_conversation['target']}?"
        )

        ### !!! TODO LLM output !!! ###
        conversation = "Hello"
        ### !!! TODO Detect LLM output is continue or not !!! ###
        continue_conversation = True

        if continue_conversation:
            self.current_conversation["conversation"] += f"{self.name} : {conversation}\n"
            ### !!! TODO summary of conversation !!! ###
            summary = "convsersation summary"
            self.current_action = f"conversing about {summary}"
            return True
        else:
            self.conversation_history.append(self.current_conversation)
            self.current_conversation = None
            return False

    def __agent_move__(self , places):
        ### agent move to new node ###
        ### TODO recursive until leaf node ###
        places = ' , '.join(places)
        knows = ' , '.join(self.knows_tree.__iter_around_env__(self.knows_tree.root))        

        prompt = (
            f"{self.name} is currently in {self.location}) that has {places}"
            f"{self.name} knows of the following areas: {knows}"
            "* Prefer to stay in the current area if the activity can be done there."
            f"{self.name} is planning {self.current_action}"
            f"Which area should {self.name} go to?"
        )

        ### !!! TODO LLM output !!! ###
        area = "NUK Town:7-11:counter:checkout counter 1"
        self.location = area
        
        

    def __str__(self) -> str:
        ### TODO show more info ###
        ret = (
            f"-- {self.name} / Age : {self.age} --\n"
            "Personality and Lifestyle : \n"
            f"Innate tendency : {self.innate_tendency}\n"
            f"Learned tendency : {self.learned_tendency}\n"
            f"Currently : {self.currently}\n"
            f"Lifestyle : {self.lifestyle}\n"
            "Latest 50 memory :\n"
            f"{self.get_memory_stream(50)}\n"
            f"plan:\n"
            f"{self.plans}\n"
            f"conversation histtiory :\n"
            f"{self.conversation_history}"
        )
                
        return ret
    