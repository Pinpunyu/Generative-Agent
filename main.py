from utils.agent import Agent
from utils.environment import env_tree , tree_node
from utils.generative_agents import generative_agents
import datetime
from pathlib import Path
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


nuk_town_path = Path("./data/envs/nuk_town.json")
agents_path = Path("./data/agents/")

nuk_town = generative_agents(nuk_town_path , agents_path, tick=60)
# nuk_town.env.add_agent("NUK Town:7-11:counter:checkout counter 1" , "yui" , "sleep")
# nuk_town.env.add_agent("NUK Town:7-11:counter:checkout counter 1" , "pin" , "sleep")
# nuk_town.env.clear_all_agent()
print(nuk_town.time)
nuk_town.env.visualize()
nuk_town.new_day(nuk_town.time)
nuk_town.next_tick()
print(nuk_town.time)
nuk_town.env.visualize()
nuk_town.next_tick()
print(nuk_town.time)
nuk_town.env.visualize()
print(nuk_town.agents["Isabella Rodriguez"])
# print(nuk_town.agents[0].__gen_plan__(nuk_town.time.date()))
# print(nuk_town.agents[0].__gen_reflection__("123" , nuk_town.time.date()))

# nuk_town.new_day(nuk_town.time)
# nuk_town.next_tick()
# print(nuk_town.agents[0].__gen_reflection__("123" , nuk_town.time))
# print(nuk_town.agents[0].get_memory_stream(1)[0])
# nuk_town.agents[0].__gen_reaction__(nuk_town.agents[0].memory_stream[-1], nuk_town.time)
# nuk_town.agents[0].next_tick()
# nuk_town.agents[0].__gen_plan__(nuk_town.time)
# nuk_town.agents[0].__gen_reflection__(nuk_town.time , 50)
# nuk_town.agents["Isabella Rodriguez"].__gen_reaction__(nuk_town.agents["Isabella Rodriguez"].memory_stream[-1] , nuk_town.time)
nuk_town.next_tick()
print(nuk_town.time)
nuk_town.env.visualize()
# print("current_conversation " , nuk_town.agents[0].current_conversation)
# print("summary_description " , nuk_town.agents[0].__gen_summary_description__(nuk_town.time))
# print("retrieval " , nuk_town.agents[0].__gen_retrieval__("123" , 3 , nuk_town.time))
# print(nuk_town.agents[0])
# print(datetime.datetime(2023,7,9,0,0,0).date())
# nuk_town.env.visualize()


# print(nuk_town.agents[0])


# print(nuk_town.agents[0])

# nuk_town.next_tick()

# print(nuk_town.agents[0])
# observations , places = nuk_town.observation(pinyu.location)
# print(observations)
# print(place)
# pinyu.knows_tree.visualize()
# pinyu.update_knows_place(places)
# pinyu.update_observation(observations , datetime.datetime.today())
# pinyu.knows_tree.visualize()

# observations , places = nuk_town.observation("NUK Town:Yui's home")
# pinyu.update_knows_place(places)
# pinyu.update_observation(observations , datetime.datetime.today())
# pinyu.knows_tree.visualize()
# nuk_town.add_places(["NUK Town:123:bathroom:456"])
# nuk_town.visualize()
# print(nuk_town.observation("NUK Town:Prof. KCF's home:bathroom"))
# print(pinyu)