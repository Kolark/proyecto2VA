import numpy as np
import queue


class Prediction:
    def __init__(self, size):
        self.QueueElements = queue.Queue()
        self.size = size
        for i in range(size):
            self.QueueElements.put(0)
        self.weights =[5,10,15,20,25]

    def Update(self,element):
        self.QueueElements.put(element)
        if self.QueueElements.qsize() > self.size:
            self.QueueElements.get()
        
        return self.GetPrediction()
    
    def GetPrediction(self):
        mylist = list(self.QueueElements.queue)
        multiplication = []
        for i in range(len(self.weights)):
            multiplication.append(self.weights[i]*mylist[i])

        return sum(multiplication)/sum(self.weights)
        # print(str())

    def printAll(self):
        print(list(self.QueueElements.queue))


# myprediction = Prediction(5)

# myprediction.Update(0)
# myprediction.Update(10)
# myprediction.Update(20)
# myprediction.Update(0)
# myprediction.Update(40)
# myprediction.GetPrediction()
# myprediction.printAll()