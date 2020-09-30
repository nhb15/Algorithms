
from queue import PriorityQueue
import os

#from class notes
english_alphabet_frequencies = {
    'a' : 8.167, 'b' : 1.492, 'c' : 2.782, 'd' : 4.253, 'e' : 12.702, 'f' : 2.228, 'g' : 2.015, 'h' : 6.094, 
    'i' : 6.966, 'j' : 0.153, 'k' : 0.747, 'l' : 4.025, 'm' : 2.406, 'n' : 6.749, 'o' : 7.507,'p' : 1.929,
    'q' : 0.095, 'r' : 5.987, 's' : 6.327, 't' : 9.056, 'u' : 2.758, 'v' : 1.037, 'w' : 2.365, 'x' : 0.150, 'y' : 1.974, 'z' : 0.074
    }
    
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
        self.str = str.lower()
        self.priorityQueue = PriorityQueue()  
        self.dictFoundChars = dict()    
        self.totalSize = 0  
        self.uncompressedSize = 0
        self.encodedChars = dict()

#In this case, we can just grab frequency from our dict.  
    def getFrequency(self, char):
        return english_alphabet_frequencies[char]

#and we can check if we already did a letter by putting used ones in hashmap. Once we have frequency, we can add the characters to our  node class and our PQ. 
    def buildPQ(self):
        
        for char in self.str:

            if char not in self.dictFoundChars:

                self.dictFoundChars[char] = None
            
                node = Node(self.getFrequency(char), char, '')

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
            self.encodedChars[node.char] = node.code
        if node.left is not None:
            node.left.code = node.left.code + node.code + '1'
            self.decodeTreeToPrint(node.left)
        if node.right is not None:
            node.right.code = node.right.code + node.code + '0'
            self.decodeTreeToPrint(node.right)
    
    #Now we can use our dict of encodings to print the code for each character in the string
    def encodeString(self):

        for char in self.str:
            code = self.encodedChars[char]
            self.totalSize += len(code)
            self.uncompressedSize += 8
            print(code, end = " ")

    #Thanks to Euclid a few short years ago, we can find the greatest common divisor like this for the ratio: 
    def gcd(self, num1, num2):

        if (num2 == 0):
             return num1
        return self.gcd(num2, num1 % num2)

    #Once we have the gcd above, we can find the ratio and print it: 
    def printCompressionRatio(self, compressed, uncompressed):

        divisor = self.gcd(compressed, uncompressed)
        print (compressed / divisor, ':', uncompressed / divisor)
        


    
#Because we hard code frequencies, the string to encode must be lowercase and have no punctuation or spaces. 
stringToEncode = 'beekeeper'    
testHW = Encoding(stringToEncode)
  
testHW.buildPQ()
testHW.mergeEntireTree()
print('')
print('The huffman coding for each individual letter of ', stringToEncode, 'is below: ')
testHW.decodeTreeToPrint(testHW.priorityQueue.get())

print('The huffman encoding of the string', stringToEncode, 'that would send is: ')
testHW.encodeString()
print('')
print('The total size of the encoding in bytes is: ', testHW.totalSize)
print('Normally, the uncompressed size of transmitting', stringToEncode, 'is: ', testHW.uncompressedSize)
print('This means that the compression ratio is ', end = " ")

testHW.printCompressionRatio(testHW.totalSize, testHW.uncompressedSize)