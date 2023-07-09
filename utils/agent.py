from utils.environment import env_tree
from utils.environment import tree_node
from anytree import Node, RenderTree, AsciiStyle


class Agent:
    
    def __init__(self, name, self_knowledge, memory_stream = []):
        self.name = name
        self.self_knowledge = self_knowledge
        # self.map = map
        self.memory_stream = memory_stream
        self.tree = env_tree()
        self.location = ""
        self.current_action = "sleep"
        self.current_conversation = None
    
    def __insert_child(self, parent, current):
        
        node = parent+":"+current
        childs = self.map.__iter_around_env__(node, 0) 
        
        for child in childs:
            child_name = child.split(':')[-1]
            parent_name = ':'.join(child.split(':')[:-1])
            
            if child_name != "" and ":" not in child_name:
                self.tree.add_children_node(node , child_name)
                self.__insert_child(node, child_name)

    def agent_tree_init(self, known):

        # 建立自己的root
        self.tree = env_tree("NUK Town")

        for place in known:
            self.tree.add_children_node("NUK Town" , place)
            # 繼續新增子節點
            self.__insert_child(self.map.root, place)
            
        self.tree.visualize()

    def print_self_knowledge(self):
        print(f"My name is {self.name}. {self.self_knowledge}")
        

    def new_observation(self, map, place):

        # 要是place沒有在自己的tree裡，要新增
        # if findall(self.root, filter_=lambda node: node.name in (place)) == 0:
        #     first = Node(place, parent=self.root)
        #     self.__insert_child(first)
        # 將place的observation push進memory stream

        # print(f"{self.location}-{self.location.count(':')} {place}-{place.count(':')}")
        print(place)
        child_name = place.split(':')[-1]
        parent_name = ':'.join(place.split(':')[:-1])

        if self.tree == None:
            print("begin")
            self.tree = env_tree(place)
        elif place.count(":")==0:
            print("hi")
            self.tree.insert_root(place)
        else:
            print("byt")
            self.tree.add_children_node(parent_name, child_name)
            # self.tree.insert_root(place)
            # self.tree.visualize()

        # self.tree.visualize()
        self.location = place

        


        observations = map.observation(place)
        print(observations)
        # for observation in observations:
        #     self.memory_stream.append(observation)
        
    def get_memory(self, num):

        return self.memory_stream[-num:]