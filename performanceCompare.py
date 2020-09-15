#On a ~2017 custom PC with a 4.2 GHz i7, and 16 GB of RAM at 2.1 GHz
#Experiment to test performance across machines and sorting algorithms

def mergeSort(a):

    if len(a)>1:
        # As long as input array has more than
        # one elements, split in half.
        
        halfPoint = len(a)//2
        leftHalf = a[:halfPoint]
        rightHalf = a[halfPoint:]

        mergeSort(leftHalf)
        mergeSort(rightHalf)        
       
        i=0 # Current element index for left half
        j=0 # Current element index for right half
        k=0 # Current element index for merged array
                
        while i < len(leftHalf) and j < len(rightHalf):
            
            # While there are elements in both halves:
            
            if leftHalf[i] <= rightHalf[j]:
                
                # Copy the current element of the left half
                # to the merged array and advance the left
                # index, making its next element the current one.
                
                a[k]=leftHalf[i]
                i=i+1
            else:
                
                # Copy the current element of the right half
                # to the merged array and advance the right
                # index, making its next element the current one.
                
                a[k]=rightHalf[j]
                j=j+1
            
            # Advance to the next element of the merged array.
            k=k+1
            
        # At least one of the two halves is now empty.
        # We can now copy the remaining elements of the
        # non-empty half, into the merged array. These
        # elements are already sorted, thus order is preserved.

        while i < len(leftHalf):
            a[k]=leftHalf[i]
            i=i+1
            k=k+1

        while j < len(rightHalf):
            a[k]=rightHalf[j]
            j=j+1
            k=k+1


def partition(arr, low, high):
    i = (low-1)         # index of smaller element
    pivot = arr[high]     # pivot
 
    for j in range(low, high):
 
        # If current element is smaller than or
        # equal to pivot
        if arr[j] <= pivot:
 
            # increment index of smaller element
            i = i+1
            arr[i], arr[j] = arr[j], arr[i]
 
    arr[i+1], arr[high] = arr[high], arr[i+1]
    return (i+1)
 
# The main function that implements QuickSort
# arr[] --> Array to be sorted,
# low  --> Starting index,
# high  --> Ending index
 
# Function to do Quick sort

def quickSort(arr, low, high):
    if len(arr) == 1:
        return arr
    if low < high:
 
        # pi is partitioning index, arr[p] is now
        # at right place
        pi = partition(arr, low, high)
 
        # Separately sort elements before
        # partition and after partition
        quickSort(arr, low, pi-1)
        quickSort(arr, pi+1, high)

import numpy as np
import time
import pandas as pd
import matplotlib.pyplot as plt
#matplotlib inline

arraySize = 2

# Start low, maxArraySize = 5000. If you do not notice any performance issues,
# go to 50,000; then 500,000 and keep trying. You can call it a day when it takes
# longer 1 hour to produce the next line of results.

maxArraySize = 68000000
largestElement = maxArraySize * 2

with open('results.txt', 'w') as f:

    while arraySize < maxArraySize:
        
        testArray = np.random.randint(0,largestElement,arraySize)
        testArray = list(testArray)
        
        startTime = time.time()
        mergeSort(testArray)
        mergeSortTime = time.time() - startTime
        
        testArray = np.random.randint(0,largestElement,arraySize)
        testArray = list(testArray)
        n = len(testArray)
        startTime = time.time()
        quickSort(testArray,0,n-1)
        quickSortTime = time.time()-startTime

        testArray = np.random.randint(0,largestElement,arraySize)
        testArray = list(testArray)
        startTime = time.time()
        testArray.sort()
        timSortTime = time.time()-startTime
        
        print(f'{arraySize:15d}{mergeSortTime:13f}{quickSortTime:13f}{timSortTime:13f}')
        print(f'{mergeSortTime:13f},{quickSortTime:13f},{timSortTime:13f}', file = f)
        arraySize = 2*arraySize
    
