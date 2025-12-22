#
# Complete the 'sortedInsert' function below.
#
# The function is expected to return an INTEGER_DOUBLY_LINKED_LIST.
# The function accepts following parameters:
#  1. INTEGER_DOUBLY_LINKED_LIST llist
#  2. INTEGER data
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

def sortedInsert(llist, data):
    # Write your code here
    new_node = DoublyLinkedListNode(data)
    if not llist:
        return new_node
    
    if data < llist.data:
        new_node.next = llist
        llist.prev = new_node
        return new_node
    
    current = llist
    while current.next and current.next.data < data:
        current = current.next
    
    new_node.next = current.next
    if current.next:
        current.next.prev = new_node
    current.next = new_node
    new_node.prev = current
    return llist