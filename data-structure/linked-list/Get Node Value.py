#
# Complete the 'getNode' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. INTEGER_SINGLY_LINKED_LIST llist
#  2. INTEGER positionFromTail
#

#
# For your reference:
#
# SinglyLinkedListNode:
#     int data
#     SinglyLinkedListNode next
#
#

def getNode(llist, positionFromTail):
    # Write your code here
    slow = llist
    fast = llist
    for _ in range(positionFromTail):
        fast = fast.next
    while fast.next:
        slow = slow.next
        fast = fast.next
    return slow.data