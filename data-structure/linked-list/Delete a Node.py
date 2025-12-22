#
# Complete the 'deleteNode' function below.
#
# The function is expected to return an INTEGER_SINGLY_LINKED_LIST.
# The function accepts following parameters:
#  1. INTEGER_SINGLY_LINKED_LIST llist
#  2. INTEGER position
#

#
# For your reference:
#
# SinglyLinkedListNode:
#     int data
#     SinglyLinkedListNode next
#
#

def deleteNode(llist, position):
    # Write your code here
    if position == 0:
        return llist.next
    current = llist
    for _ in range(position - 1):
        current = current.next
    current.next = current.next.next
    return llist