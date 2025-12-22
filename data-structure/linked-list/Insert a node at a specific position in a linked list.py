#
# Complete the 'insertNodeAtPosition' function below.
#
# The function is expected to return an INTEGER_SINGLY_LINKED_LIST.
# The function accepts following parameters:
#  1. INTEGER_SINGLY_LINKED_LIST llist
#  2. INTEGER data
#  3. INTEGER position
#

#
# For your reference:
#
# SinglyLinkedListNode:
#     int data
#     SinglyLinkedListNode next
#
#

def insertNodeAtPosition(llist, data, position):
    # Write your code here
    new_node = SinglyLinkedListNode(data)
    if position == 0:
        new_node.next = llist
        return new_node
    current = llist
    for _ in range(position - 1):
        current = current.next
    new_node.next = current.next
    current.next = new_node
    return llist