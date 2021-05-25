import numpy as np 
import tflearn 
import tensorflow as tf
from tensorflow import keras 
import random 
import json

model.load("/content/model/")

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
        if w == se:
            bag[i] = 1
    return np.array(bag)

def chat():
    print("Start talking with the bot!")
    while True:
        inp = input("You: ")
        if inp.lower() == "quit":
            break
        
        results = model.predict([bag_of_words(inp, words)])[0]
        results_index = np.argmax(results)
        tag = labels[results_index]
        
        if results[results_index] > 0.7:
            for tg in data['intents']:
                if tg['tag'] == tag:
                    responses = tg['responses']
                
                print(random.choice(responses))
        else:
            print("I don't know.")
        
chat()