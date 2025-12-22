#
# Complete the 'reverse' function below.
#
# The function is expected to return an INTEGER_SINGLY_LINKED_LIST.
# The function accepts INTEGER_SINGLY_LINKED_LIST llist as parameter.
#

#
# For your reference:
#
# SinglyLinkedListNode:
#     int data
#     SinglyLinkedListNode next
#
#

def reverse(llist):
    # Write your code here
    previous = None
    current = llist
    while current:
        next_node = current.next
        current.next = previous
        previous = current
        current = next_node
    return previous