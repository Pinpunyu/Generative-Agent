import queue
import plotly.graph_objects as go
import json
from typing import Union , Tuple
from pathlib import Path
class tree_node():
    def __init__(self , name , parent):
        ### Node INFO ###
        # name  : area name
        # state : object state (only leaf nodes)
        # agents : which agents at this node
        # parent : the node's parent (only one)
        # children : the node's childern (have many)

        ### Agent ###
        # key   -> name   : agent name
        # value -> action : agent current action
        self.name = name
        self.state = None
        self.agents = {}
        self.parent = parent
        self.children = []
    
    def insert_parent(self, parent):
        if self.parent == None:
            self.parent = parent

    def append_children(self , children):
        self.children.append(children)

    def add_agent(self , agent , action):
        self.agents[agent] = action

    def remove_agent(self , agent):
        self.agents.pop(agent)

    def change_state(self , state):
        self.state = state

    def observation(self):
        observation = []
        
        if self.state != None:
            observation.append(f"{self.name} is {self.state}")
        
        
        for agent , action in self.agents.items():
            observation.append(f"{agent} is {action}")

        return observation
    
    def __str__(self):
        return f"\tNode Name : {self.name} \n\tState : {self.state}\n\tParent : {self.parent} \n\tAgent : {self.agents} \n\tChildren : {self.children}\n"
    
class env_tree():
    def __init__(self , json : Union[str , Path] = None , places : list[str] = None):
        ### Tree ###
        # key   -> node name
        # value -> tree_node
        # root  -> root node name

        self.tree = {}
        self.root = None

        if json != None:
            self.load_from_json(json)

        if places != None:
            self.add_places(places)   
    
        
    def add_places(self , places : list[str]):
        ### add muti place into tree ###
        # place format = "A:B:C:D"
        for place in places:
            self.__add_place_node__(place)

    def __add_place_node__(self , node_key : str):

        node_path = node_key.split(':')
        if self.root == None:
            self.root = node_path[0]
            self.tree[self.root] = tree_node(self.root, None)

        children = ""
        parent = None

        for subnode in node_path:
            children += subnode
            # print(children)
            if children not in self.tree:
                self.tree[children] = tree_node(subnode , parent)
                # print(self.tree[children])
                self.add_children_node(parent , subnode)
            
            parent = children
            children += ":"
            
    
    def load_from_json(self , json_path : Union[str , Path]):
        ### load env form json ###
        # json formate
        # {
        #   "root" : "",
        #   "node_key" : "parents_key",
        #   "node_key" : "parents_key",
        #   ...
        # }
        with open(json_path) as f:
            tree_dict = json.load(f)

        for node , parent in tree_dict.items():
            node_name = node.split(':')[-1]
            if parent == "":
                self.root = node_name
                self.tree[node_name] = tree_node(node_name , None)
                parent = None 
            else:
                self.add_children_node(parent , node_name)

    

    def insert_root(self , parent_name:str):
        ### add a new root connect old root ###
        parent_key = parent_name
        old_root = self.root
        
        self.tree[parent_key] = tree_node(parent_name , None)


        children_li = self.__iter_around_env__(old_root , 0)
        
        for node_key in children_li:
            self.tree[f"{parent_name}:{node_key}"] = self.tree[node_key]
            self.tree.pop(node_key)

        new_children_key = f"{parent_name}:{old_root}"
        self.tree[new_children_key].insert_parent(parent_name)
        self.tree[parent_key].append_children(old_root)
        self.root = parent_name
        

    def add_children_node(self, parent_key:str , children_name:str):
        ### add a child node in parent node ###
        # parent_key -> node path
        # children_name -> children name


        # add a child node into parent
        
        children_key = f"{parent_key}:{children_name}"
        parent_name = parent_key.split(":")[-1]
        self.tree[children_key] = tree_node(children_name , parent_name)
        self.tree[children_key].change_state("idle")
        self.tree[parent_key].append_children(children_name)
        self.tree[parent_key].change_state(None)

        # add a parent node from child
        if parent_key not in self.tree:
            self.tree[parent_key] = tree_node(parent_key , None)
            self.tree[parent_key].append_children(children_name)      
            self.tree[children_name].insert_parent(parent_key)  

            # update root
            if self.root == children_name:
                self.root = parent_key

            if len(self.tree[children_name].children) == 0:
                self.tree[children_name].change_state("idle")

        # self.tree[parent].append_children(children)
        # self.tree[parent].change_state(None)
        
    
    def add_agent(self , node:str , agent:str , action:str):
        ### add a new agent into specific node ###
        self.tree[node].add_agent(agent , action)

    def remove_agent(self , node:str , agent:str):
        ### remove a agent of the specific node ###
        self.tree[node].remove_agent(agent)

    def visualize(self):
        ### show the env tree ###
        bfs_li = self.__iter_around_env__(self.root)
        parent_li = []
        state = []
        value = []
        for node_key in bfs_li:
            parent_li.append(':'.join(node_key.split(':')[:-1]))
            state.append(f"{node_key.split(':')[-1]} : {self.tree[node_key].state}")
            value.append(1)

        # for i in range(0, len(bfs_li)):
            # print(f"\"{bfs_li[i]}\" : \"{parent_li[i]}\",")
        
        fig = go.Figure(go.Treemap(
            labels=bfs_li , 
            parents=parent_li , 
            # branchvalues='total',
            text = state,
            values = value,
            name='',
            hovertemplate="<b>%{text} </b>",))
        fig.update_traces(root_color="lightgrey")
        fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
        fig.show()

    def __iter_around_env__(self , node_key:str , around_factor :int = 1) -> list[str]:
        ### from the start node search around_factor parent as root , traversal the subtree ###
        # return traversal node list
        bfs_queue = queue.Queue()
        start_node = node_key
        for _ in range(around_factor):
            parent_name = self.tree[start_node].parent
            if parent_name != None:
                start_node = ':'.join(start_node.split(":")[:-1])
            else:
                break

        bfs_queue.put(start_node)

        traversal_rel = []


        while not bfs_queue.empty():
            node_key = bfs_queue.get()
            traversal_rel.append(node_key)
            for child_name in self.tree[node_key].children:
                bfs_queue.put(f"{node_key}:{child_name}")

        return traversal_rel
    
    def observation(self , node:str , around_factor = 1) -> Tuple[list[str] , list[str]]:
        ### return the observation & place with a node & around_factor
        bfs_li = self.__iter_around_env__(node , around_factor)
        # root_node = bfs_li[0]
        # depth = len(root_node.split(":")) - 1
        observation = []
        place = []
        for node in bfs_li:

            place.append(node)
            node_observation = self.tree[node].observation()

            if len(node_observation) != 0:
                observation += node_observation
            
                # place.append(':'.join(node.split(':')[depth:]))
                

        return observation , place

    def __getitem__(self , key:str) -> tree_node:
        return self.tree[key]

    def __str__(self) -> str:

        bfs_li = self.__iter_around_env__(self.root)
        ret = ""

        for node in bfs_li:
            ret += f"{node}\n{str(self.tree[node])}\n"

        return ret



if __name__ == "__main__":
    {
        "name" : "nuk" ,
        "agent" : [],
        "state" : None
    }

    nuk_town = env_tree("./data/env/nuk_town.json")
    # nuk_town.load_from_json()
    # nuk_town = nuk_town_init()
    # print(nuk_town)
    # nuk_town.insert_root("123456")
    nuk_town.visualize()

    

    # print(a.iter_around_env("classroom" , 12))
    # print(nuk_town.observation("NUK Town:Prof. KCF's home" ))
    