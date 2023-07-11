from sentence_transformers import SentenceTransformer, util
import numpy as np
import math
from datetime import datetime, timedelta

class Retrieval:

    def get_recency(current_time : datetime, memory_times : list[datetime]) :

        initial_value = 1.0
        decay_factor = 0.99

        score = [0 for i in range(len(memory_times))]

        for idx , memory_time in enumerate(memory_times):

            time = (current_time-memory_time)
            time = 24*time.days + time.seconds/3600
            
            score[idx] = initial_value * math.pow(decay_factor, time)
        
        score = np.array(score)
        return score / np.linalg.norm(score)
        

    def get_relevance(query : str , sentences : list[str]):

        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        query_embedding = model.encode(query , convert_to_tensor=True)
        score = [0 for i in range(len(sentences))]

        for idx , sentence in enumerate(sentences):
            embedding = model.encode(sentence, convert_to_tensor=True)
            score[idx] = util.pytorch_cos_sim(query_embedding, embedding).to("cpu").item()
        
        # print(score)
        score = np.array(score)
        return score / np.linalg.norm(score)
    
    def get_importantance(observations:list[str]):
        
        score = [0 for i in range(len(observations))]
        for idx , observation in enumerate(observations):
            prompt = (
            "On the scale of 1 to 10, \n"
            "where 1 is purely mundane (e.g., <相似範例(similary examples)>) \n"
            "and 10 is extremely poignant (e.g., <相似範例(similary examples)>), \n"
            "rate the likely poignancy of the following piece of memory.\n"
            f"Memory: {observation}"
            "Rating: <fill in>"
            )
            score[idx] = 50

        score = np.array(score)
        return score / np.linalg.norm(score)
    
    def get_retrieval(memory_stream:list[dict] , query , time):

        last_use = [0 for i in range(len(memory_stream))]
        observations = [0 for i in range(len(memory_stream))]
        importantance_score = [0 for i in range(len(memory_stream))]
        for idx , observation in enumerate(memory_stream):
            last_use[idx] = observation["last_use"]
            observations[idx] = observation["observation"]
            importantance_score = observation['importantance']

        importantance_factor = 1
        relevance_factor = 1
        recency_factor = 1
        
        recency_score = Retrieval.get_recency(time , last_use) * recency_factor
        # importantance_score = Retrieval.get_importantance(observations) * importantance_factor 
        relevance_score = Retrieval.get_relevance(query , observations) * relevance_factor
        
        score = recency_score * recency_factor + importantance_score * importantance_factor + relevance_score * relevance_factor


        sorted_memory_streams = memory_stream.copy()

        for idx , sc in enumerate(sorted_memory_streams):
            sorted_memory_streams[idx]["score"] = score[idx]

        sorted_memory_streams.sort(key=lambda element: element['score'] , reverse=True)

        return sorted_memory_streams
        
        
    


        

if __name__ == "__main__":
    
    

    current_time = datetime(2022,6,13,0,20,15)
    memory_stream = []
    

    for time in range(0, 14):
        memory_time = datetime(2022,6,10,15-time,20,15)
    
        memory_stream.append({
            "observation" : str(time),
            "time" : memory_time,
            "last_use" : memory_time,
        })

    # print(y)
    
    Retrieval.get_retrieval(memory_stream , "123" , current_time)
    # score = Retrieval.get_recency(current_time , time)
    # print(score)

