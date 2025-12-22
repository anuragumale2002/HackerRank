#
# Complete the 'matchingStrings' function below.
#
# The function is expected to return an INTEGER_ARRAY.
# The function accepts following parameters:
#  1. STRING_ARRAY stringList
#  2. STRING_ARRAY queries
#

def matchingStrings(stringList, queries):
    # Write your code here
    # Create a dictionary to store the frequency of each string in stringList
    frequency_dict = {}
    
    for string in stringList:
        if string in frequency_dict:
            frequency_dict[string] += 1
        else:
            frequency_dict[string] = 1
    
    # Create a list to store the results for each query
    results = []
    
    for query in queries:
        results.append(frequency_dict.get(query, 0))
    
    return results