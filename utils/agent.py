from anytree import Node, RenderTree


class Agent:
    
    def __init__(self, name, self_knowledge, map, memory = []):
        self.name = name
        self.self_knowledge = self_knowledge
        self.map = map
        self.memory = memory
    
    def __insert_child(self, parent):

        childs = 0 # map.get_clild(self.map)
        if childs == 0:
            return
        else:
            for child in childs:
                second = Node(child, parent=parent)
                self.__insert_child(second)

    def create_my_tree(self, known):

        # 建立自己的root
        root = Node(self.name)

        for place in known:
            first = Node(place, parent=root)
            self.__insert_child(first)
            # 繼續新增子節點
        
        for pre, fill, node in RenderTree(root):
            print("%s%s" % (pre, node.name))

    def print_self_knowledge(self):
        print(f"My name is {self.name}. {self.self_knowledge}")

    def new_observation(self, place):
        # 要是place沒有在自己的tree裡，要新增

        # 將place的observation push進memory stream
        self.memory.push("")# self.memory.push(get_place_observation(place))
        
    def get_memory(self, num):

        for i in num:
            self.memory.pop()
