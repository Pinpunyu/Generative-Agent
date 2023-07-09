from sentence_transformers import SentenceTransformer, util
import numpy as np
import matplotlib.pyplot as plt
import math
from datetime import datetime, timedelta

class Retrieval:

    def get_Recency(self, current_time, memory_time):

        initial_value = 1.0
        decay_factor = 0.99
        time = (current_time-memory_time)
        time = 24*time.days + time.seconds/3600

        return initial_value * math.pow(decay_factor, time)

    def get_Relevance(self, sentence1, sentence2):

        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

        embedding_1= model.encode(sentence1, convert_to_tensor=True)
        embedding_2 = model.encode(sentence2, convert_to_tensor=True)
        
        return util.pytorch_cos_sim(embedding_1, embedding_2)
        

if __name__ == "__main__":
    
    test = Retrieval()

    current_time = datetime(2022,6,13,0,20,15)
    
    x = list(range(0, 14))
    y = []

    for time in range(0, 14):
        memory_time = datetime(2022,6,10,15-time,20,15)
        y.append(test.get_Recency(current_time, memory_time))     

    plt.plot(x, y, 'r')   
    plt.show()

    # get_relevance
    # sentence1 = "I eat an apple."
    # sentence2 = "I use Apple cellphone."
    # sentence3 = "My favorite fruit is apple."

    sentence1 = "Just now, the teacher taught us something related to chemistry."
    sentence2 = "After class, my classmates and I were discussing chemistry."
    sentence3 = "I have cereal and milk for breakfast."

    print(test.get_Relevance(sentence1, sentence2))
    print(test.get_Relevance(sentence2, sentence3))
    print(test.get_Relevance(sentence3, sentence1))