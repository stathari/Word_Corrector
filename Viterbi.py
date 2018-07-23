import math
import string
class Viterbi:
    def __init__(self, prob_states, prob_paths, test_data):
        self.delta = []
        self.alphabets = list(string.ascii_lowercase)
        self.len_a = len(self.alphabets)
        
        self.test_data = test_data
        
        #probabilities of paths and states
        self.prob_states = prob_states
        self.prob_paths = prob_paths
         
        # Same initial probabilities for every states
        self.prob_ini = float(1)/self.len_a     

        # calculating values required for recall and precision
        self.TP = 0
        self.FP = 0
        self.FN = 0
        self.word_count = 0
        
    def calc_delta(self, symChar):
        #calculates the delta to find the path with max probability
        #back tracking in case of finding a highest probability path.
        back_track = [None] * self.len_a
        temp = [None] * self.len_a
        for j in range(0, self.len_a):
            max = None
            for i in range(0, self.len_a):
                path = self.prob_paths[i][j]
                mul = self.delta[i] + math.log(path)
                if (mul > max or max is None):
                    max = mul
                    back_track[j] = self.alphabets[i]
            calc = max + math.log((self.prob_states[j][self.alphabets.index(symChar)]))
            temp[j] = calc
        self.delta = temp
        return back_track

    def correct_word(self, back_track):
        #find the possible word and return
        temp = self.delta.index(max(self.delta))
        word = [self.alphabets[temp]]
        if back_track:
            for l in back_track:
                word.append(l[temp])
                temp = self.alphabets.index(l[temp])
            word.reverse()
        return ''.join(word)

    def parse_data(self, testSet):
        testSet = [x for x in testSet if x.isalpha()]
        index = 0
        for word in self.test_data:
            # print "==============================="
            # print "Actual:", testSet[index]
            # print "Corrupted:", word
            back_track = []
            for i in range(0, len(word)):
                char = word[i]
                if (i is 0):
                    self.delta = []
                    for j in range(0, self.len_a):
                        #fetching initial probabilities
                        ini = self.prob_ini
                        #probabilities of states from HMM model
                        state = self.prob_states[j][self.alphabets.index(char)]
                        self.delta.append(math.log(state) + math.log(ini))
                else:
                    back_track.insert(0, self.calc_delta(char))

            updated_word = self.correct_word(back_track)
            self.word_count += 1
            if testSet[index] != word:    
                #true positive
                if testSet[index] == updated_word:
                    self.TP += 1
                
                #false negative
                if word != updated_word:
                    self.FN += 1
                    
                #false positive
            else:
                if (word != updated_word):
                    self.FP += 1
            index += 1
            
    def calc_precision_recall(self):        
        #Precision = TP/(TP + FN)
        #Recall = TP/(TP + FP)
        print "recall = ", float(self.TP) / (self.TP + self.FN) * 100
        print "precision = ", float(self.TP) / (self.TP + self.FP) * 100