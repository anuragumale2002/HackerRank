#
# Complete the 'reverse' function below.
#
# The function is expected to return an INTEGER_DOUBLY_LINKED_LIST.
# The function accepts INTEGER_DOUBLY_LINKED_LIST llist as parameter.
#

#
# For your reference:
#
# DoublyLinkedListNode:
#     int data
#     DoublyLinkedListNode next
#     DoublyLinkedListNode prev
#
#

def reverse(llist):
    # Write your code here
    # Initialize current to head of the list
    current = llist
    temp = None

    # Traverse the list
    while current is not None:
        # Swap next and prev pointers
        temp = current.prev
        current.prev = current.next
        current.next = temp

        # Move to the next node (which is the previous node due to the swap)
        current = current.prev

    # If the list is empty or contains only one node, return llist
    if temp is not None:
        llist = temp.prev

    return llist