import queue
import plotly.graph_objects as go

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
    def __init__(self , root_name):
        ### Tree ###
        # key   -> node name
        # value -> tree_node
        # root  -> root node name
        self.tree = {}
        self.tree[f"{root_name}"] = tree_node(root_name , None)
        self.root = root_name
    
    def insert_root(self , parent_name):
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
        

    def add_children_node(self, parent_key , children_name):
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
        
    
    def add_agent(self , node , agent , action):
        ### add a new agent into specific node ###
        self.tree[node].add_agent(agent , action)

    def remove_agent(self , node , agent):
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
            # state.append(1)

        # print(parent_li)
        # data = {'name' : bfs_li , 'parent' : parent_li }
        
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

    def __iter_around_env__(self , node_key , around_factor = 1):
        ### from the start node search around_factor parent as root , traversal the subtree ###
        # return traversal node list
        bfs_queue = queue.Queue()
        start_node = node_key
        for _ in range(around_factor):
            parent_name = self.tree[start_node].parent
            if parent_name != None:
                start_node = ','.join(start_node.split(":")[:-1])
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
    
    def observation(self , node , around_factor = 1):
        ### return the observation with a node & around_factor
        bfs_li = self.__iter_around_env__(node , around_factor)
        observation = []
        for node in bfs_li:
            observation += self.tree[node].observation()

        return observation     

    def __getitem__(self , key):
        return self.tree[key]

    def __str__(self):

        bfs_li = self.__iter_around_env__(self.root)
        ret = ""

        for node in bfs_li:
            ret += f"{node}\n{str(self.tree[node])}\n"

        return ret

def nuk_town_init():
    nuk_town = env_tree("NUK Town")
    # depth 1
    nuk_town.add_children_node("NUK Town" , "7-11")
    nuk_town.add_children_node("NUK Town" , "Yui's home")
    nuk_town.add_children_node("NUK Town" , "Pinyu's home")
    nuk_town.add_children_node("NUK Town", "school")
    nuk_town.add_children_node("NUK Town", "Prof. KCF's home")
    # depth 2
    nuk_town.add_children_node("NUK Town:7-11", "counter")
    nuk_town.add_children_node("NUK Town:7-11", "product shelf")

    nuk_town.add_children_node("NUK Town:Yui's home", "room")
    nuk_town.add_children_node("NUK Town:Yui's home", "bathroom")

    nuk_town.add_children_node("NUK Town:Pinyu's home", "room")
    nuk_town.add_children_node("NUK Town:Pinyu's home", "bathroom")

    nuk_town.add_children_node("NUK Town:school", "classroom 203")
    nuk_town.add_children_node("NUK Town:school", "Prof. KCF's lab")

    nuk_town.add_children_node("NUK Town:Prof. KCF's home" , "bedroom")
    nuk_town.add_children_node("NUK Town:Prof. KCF's home" , "study room")
    nuk_town.add_children_node("NUK Town:Prof. KCF's home" , "bathroom")
    # depth 3
    nuk_town.add_children_node("NUK Town:7-11:counter", "checkout counter 1")
    nuk_town.add_children_node("NUK Town:7-11:counter", "checkout counter 2")
    
    nuk_town.add_children_node("NUK Town:7-11:product shelf", "product shelf 1")
    nuk_town.add_children_node("NUK Town:7-11:product shelf", "product shelf 2")
    nuk_town.add_children_node("NUK Town:7-11:product shelf", "product shelf 3")

    nuk_town.add_children_node("NUK Town:Yui's home:room", "bed")
    nuk_town.add_children_node("NUK Town:Yui's home:room", "computer")
    nuk_town.add_children_node("NUK Town:Yui's home:room", "wardrobe")

    nuk_town.add_children_node("NUK Town:Yui's home:bathroom", "sink")
    nuk_town.add_children_node("NUK Town:Yui's home:bathroom", "toilet")
    nuk_town.add_children_node("NUK Town:Yui's home:bathroom", "shower room")

    nuk_town.add_children_node("NUK Town:Pinyu's home:room", "bed")
    nuk_town.add_children_node("NUK Town:Pinyu's home:room", "computer")
    nuk_town.add_children_node("NUK Town:Pinyu's home:room", "wardrobe")

    nuk_town.add_children_node("NUK Town:Pinyu's home:bathroom", "sink")
    nuk_town.add_children_node("NUK Town:Pinyu's home:bathroom", "toilet")
    nuk_town.add_children_node("NUK Town:Pinyu's home:bathroom", "tub")

    nuk_town.add_children_node("NUK Town:school:classroom 203", "desk 1")
    nuk_town.add_children_node("NUK Town:school:classroom 203", "desk 2")
    nuk_town.add_children_node("NUK Town:school:classroom 203", "podium")

    nuk_town.add_children_node("NUK Town:school:Prof. KCF's lab", "computer 1")
    nuk_town.add_children_node("NUK Town:school:Prof. KCF's lab", "computer 2")
    nuk_town.add_children_node("NUK Town:school:Prof. KCF's lab", "meeting table")

    nuk_town.add_children_node("NUK Town:Prof. KCF's home:bedroom" , "bed")
    nuk_town.add_children_node("NUK Town:Prof. KCF's home:bedroom" , "tv")
    nuk_town.add_children_node("NUK Town:Prof. KCF's home:bedroom" , "wardrobe")

    nuk_town.add_children_node("NUK Town:Prof. KCF's home:study room" , "compter")
    nuk_town.add_children_node("NUK Town:Prof. KCF's home:study room" , "bookcase")

    nuk_town.add_children_node("NUK Town:Prof. KCF's home:bathroom" , "sink")
    nuk_town.add_children_node("NUK Town:Prof. KCF's home:bathroom" , "tub")
    nuk_town.add_children_node("NUK Town:Prof. KCF's home:bathroom" , "toilet")

    # nuk_town.add_agent("school" , "yui" , "sleep")

    return nuk_town

if __name__ == "__main__":
    {
        "name" : "nuk" ,
        "agent" : [],
        "state" : None
    }


    nuk_town = nuk_town_init()
    # print(nuk_town)
    nuk_town.insert_root("123456")
    nuk_town.visualize()

    

    # print(a.iter_around_env("classroom" , 12))
    # print(nuk_town.observation("NUK Town:Prof. KCF's home" ))
    