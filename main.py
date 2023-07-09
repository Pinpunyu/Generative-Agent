from utils.agent import Agent
from utils.environment import nuk_town_init
from anytree import Node, RenderTree

# Nuk = Node("Nuk")
# School = Node("School", parent=Nuk)
# classrooom1 = Node("classrooom1", parent=School)
# classrooom2 = Node("classrooom2", parent=School)
# Home = Node("Home", parent=Nuk)
# bedrooom = Node("bedrooom", parent=Home)
# bathrooom = Node("bathrooom", parent=Home)
# Park = Node("Park", parent=Nuk)
# Store = Node("Store", parent=Nuk)


# for pre, fill, node in RenderTree(Nuk):
#     print("%s%s" % (pre, node.name))
# print("")

{
    "name" : "nuk" ,
    "agent" : [],
    "state" : None
}


nuk_town = nuk_town_init()
print(nuk_town.observation("NUK Town:Pinyu's home", 0))
# nuk_town.insert_root("123456")
# print(nuk_town)
# nuk_town.visualize()



pinyu = Agent("Pinyu", "21 years old is a student")




# pinyu.print_self_knowledge()

# known = ["Pinyu's home", "school"]
# pinyu.agent_tree_init(known)

# pinyu.new_observation(nuk_town, "NUK Town:Pinyu's home")
# pinyu.new_observation(nuk_town, "NUK Town:Pinyu's home:room")
# pinyu.new_observation(nuk_town, "NUK Town")
# pinyu.new_observation(nuk_town, "NUK Town:Yui's home")
# print(pinyu.get_memory(5))
