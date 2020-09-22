#We want to transmit BEEKEEPER with the shortest and fastest transmission

#We want to use symbols only from a set of three, with the space character reserved for separating. '

# Zeros are faster than 1's by a factor of three (0.1 for a 0, 0.3 for a 1), so we want our letters used the most to have the most zeros. 

#FREQUENCIES:
#B: 1
#E: 5
#K: 1
#P: 1
#R: 1

#Since E has the most frequency, we want to make sure it has the most zero's in our algorithm and is prioritized. 
#The frequency should determine priority. Since zero's transmit 3x the speed of 1's, we should use these the most for the highest priority. 

#B: 00
#E: 0
#K: 000
#P: 10
#R: 01

#Therefore E transmits at 0.1 ms, B transmits at 0.2 ms, and K/P/R all transmit at 0.3 ms, but they all have unique codes. 
#We would then trasmit: 00 0 0 000 0 0 10 0 01

#Getting more general to apply it to any string: 



import heapq
from queue import PriorityQueue
import os

#Node will hold our frequency, character, and current encoding for itself
class Node:
    def __init__(self, freq, char, code):
        self.freq = freq
        self.char = char
        self.right = None
        self.left = None
        self.code = code
    
    #As I learned doing this unsuccessfully the first time, these two methods are similar to java's comparable method implementation where they are needed to compare nodes. 
    #We want to compare frequency:
    def __lt__(self, other):
        return self.freq < other.freq

    def __le__(self,other):
        return self.freq <= other.freq

#Encoding will hold all of the structural methods needed to do Huffman Encoding
class Encoding:

    def __init__(self,str):
        self.str = str
        self.priorityQueue = PriorityQueue()
        self.dictFoundChars = dict()

    #This method was built at the start to just hard-code beekeeper. 
    def printEncodedBeeKPR (self):
        
        hwCode = dict()
        hwCode['e'] = '0'
        hwCode['b'] = '00'
        hwCode['k'] = '000'
        hwCode['p'] = '10'
        hwCode['r'] = '01'

        print('The HARD-CODED encryption for beekeeper is: ')
        for c in self.str:
            print (hwCode[c], end =' ')
            

#We want to calc freq first in our program - 
    def getFrequency(self, str, char):
        return str.count(char)

#and we can check if we already did a letter by putting used ones in hashmap. Once we have frequency, we can add the characters to our  node class and our PQ. 
    def buildPQ(self):
        
        for char in self.str:
            
            if char not in self.dictFoundChars:
                self.dictFoundChars[char] = None
                
                node = Node(self.getFrequency(self.str, char), char, '')

                self.priorityQueue.put(node)
            

    #We want to merge the two smallest nodes in the tree until the tree is one node - this includes merging parent nodes into parent nodes, etc. 
    def mergeTwoSmallestInTree(self):  

        firstNode = self.priorityQueue.get()
        
        secNode = self.priorityQueue.get()       

        parentNode = Node(firstNode.freq + secNode.freq, None, '')
        parentNode.code = firstNode.code + secNode.code        
        parentNode.left = firstNode        
        parentNode.right = secNode
        
        self.priorityQueue.put(parentNode)
        
    #This method might be able to get combined with the above, but in building this the first time I separated them. 
    def mergeEntireTree(self):

        while (self.priorityQueue.qsize() > 1):
            
            self.mergeTwoSmallestInTree()

    #This decoder actually spits out the codes from the tree and adds a 0 to left nodes and a 1 to right nodes to ensure uniqueness. 
    def decodeTreeToPrint(self, node):


        if node.left is None and node.right is None:
            print(node.char, ' ', node.code)
        if node.left is not None:
            node.left.code = node.left.code + node.code + '0'
            self.decodeTreeToPrint(node.left)
        if node.right is not None:
            node.right.code = node.right.code + node.code + '1'
            self.decodeTreeToPrint(node.right)



    

    
testHW = Encoding('beekeeper')
testHW.printEncodedBeeKPR()

   
#testHW = Encoding('TEST HERE')
testHW.buildPQ()
testHW.mergeEntireTree()
print('')
print('The huffman coding attempt for any string is below: ')
testHW.decodeTreeToPrint(testHW.priorityQueue.get())
print('To test any future generic strings, use the Encoding class constructor commented out on line 134. ')





    





