from utils.agent import Agent
from anytree import Node, RenderTree

Nuk = Node("Nuk")
School = Node("School", parent=Nuk)
classrooom1 = Node("classrooom1", parent=School)
classrooom2 = Node("classrooom2", parent=School)
Home = Node("Home", parent=Nuk)
bedrooom = Node("bedrooom", parent=Home)
bathrooom = Node("bathrooom", parent=Home)
Park = Node("Park", parent=Nuk)
Store = Node("Store", parent=Nuk)

# print(udo)
# Node('/Udo')
# print(joe)
# Node('/Udo/Dan/Joe')

for pre, fill, node in RenderTree(Nuk):
    print("%s%s" % (pre, node.name))
print("")

pinyu = Agent("Pinyu", "21 years old is a student", Nuk)

known = ["Home", "School", "Park"]

pinyu.create_my_tree(known)
pinyu.print_self_knowledge()
