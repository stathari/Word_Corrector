import Viterbi
import numpy as np
import re
import random
import string

class WordCorrector:
    def __init__(self):
        #training and test data
        self.training_data = []
        self.test_data = []
        self.c_training_data = []
        self.c_test_data = []
        
        # initialize required variables
        self.alphabets = string.ascii_lowercase #alphabets - 26 for states in words
        self.words = []
        self.len_a = len(string.ascii_lowercase) 
        
        # 26 X 26 size for all paths, states and their probabilities
        self.states = np.zeros((self.len_a, self.len_a), dtype=int)
        self.paths = np.zeros((self.len_a, self.len_a), dtype=int) 
        
        self.prob_paths = np.zeros((self.len_a, self.len_a), dtype=float)
        self.prob_states = np.zeros((self.len_a, self.len_a), dtype=float)

    def corrupt_words_training(self, words, percent):
        #corrupt training data        
        updatedlist = []
        for word in words:
            temp = ""
            if (word.isalpha()):
                for i in range(0, len(word)):
                    ran = random.uniform(0, 1)
                    #corrupt the words in word list if falls in the percent range
                    if (ran < percent):
                        temp += chr(random.randint(97,122))   
                    else:
                        temp += word[i].lower()
                
                    #update state at i and j
                    self.states[self.alphabets.index(word[i].lower())][self.alphabets.index(temp[i].lower())] += 1
                    
                    #transition from state i to j
                    if (i is not len(word)-1):
                        self.paths[self.alphabets.index(word[i].lower())][self.alphabets.index(word[i+1].lower())] += 1
                updatedlist.append(temp.strip())
        return updatedlist
    
    def corrupt_words_test(self, words, percent):
        #corrupt test data
        updatedlist = []
        for word in words:
            temp = ""
            if (word.isalpha()):
                for i in range(0, len(word)):
                    ran = random.uniform(0, 1)
                    #corrupt the words in word list if falls in the percent range
                    if (ran < percent):
                        temp += chr(random.randint(97,122))
                            
                    else:
                        temp += word[i].lower()
                updatedlist.append(temp.strip())    
        return updatedlist

    def construct_HMM(self, percent):
        
        file = open('Unabom.txt', "r")
        doc = file.read()
        self.words = re.findall('\w+', doc)
        index = int(0.8 * len(self.words))
        # Training data
        self.training_data = [a.lower().strip() for a in self.words[:index]]
        #test data
        self.test_data = [a.lower().strip() for a in self.words[index:]]
        
        # Corrupt the text splited for training set and test set
        self.c_training_data = self.corrupt_words_training(self.training_data, percent)
        # Calculate the probability for transition from state i to state j
        self.c_test_data = self.corrupt_words_test(self.test_data, percent)

        #calculate state and path probabilities
        for i in range(0, self.len_a):
            # Smoothing to prevent divide by zero error
            if (0 in self.paths[i]):
                self.paths[i] = [a+1 for a in self.paths[i]]
            sum_paths = self.paths[i].sum()
            
            if (0 in self.states[i]):
                self.states[i] = [a+1 for a in self.states[i]]
            sum_states = self.states[i].sum()
            
            for j in range(0, self.len_a):
                self.prob_paths[i][j] = float(self.paths[i][j]) / sum_paths
                self.prob_states[i][j] = float(self.states[i][j]) / sum_states

#percentage corruption:
percentages = [0.1, 0.2]
#create wordcorrector class object
wc = WordCorrector()
#call model
for percent in percentages: 
    print "Results for corruption percentage: ",percent
    wc.construct_HMM(percent)

    #create viterbi object
    viterbi = Viterbi.Viterbi(wc.prob_states, wc.prob_paths, wc.c_test_data)
    #invoke the execution process of viterbi
    viterbi.parse_data(wc.test_data)
    viterbi.calc_precision_recall()