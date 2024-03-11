def swapPositions(list, pos1, pos2):
    list[pos1], list[pos2] = list[pos2], list[pos1]
    return list
 
# Function to find the next permutation
def nextPermutation(arr):
    n = len(arr)
    i = len(arr)-2
    j = 0
     
    # Find for the pivot element.
    # A pivot is the first element from
    # end of sequencewhich doesn't follow
    # property of non-increasing suffix
    while i>=0:
      if arr[i]<arr[i+1]:
        break
      i=i-1
             
    # Check if pivot is not found
    if (i < 0):
        arr.reverse()
 
    # if pivot is found
    else:
        # Find for the successor of pivot in suffix
        for j in range(n-1, i, -1):
            if (arr[j] > arr[i]):
                break
 
        # Swap the pivot and successor
        swapPositions(arr, i, j)
         
        # Minimise the suffix part
        # initializing range
        strt, end = i+1, len(arr)
 
        # Third arg. of split with -1 performs reverse
        arr[strt:end] = arr[strt:end][::-1]

 
# This code is contributed by Rohit Pradhan

if __name__ == "__main__":
    arr = [1, 1, 1, 0, 0]
    for i in range(10):
        nextPermutation(arr)
        print(arr)