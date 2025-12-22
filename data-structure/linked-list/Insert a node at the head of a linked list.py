# Complete the insertNodeAtHead function below.

#
# For your reference:
#
# SinglyLinkedListNode:
#     int data
#     SinglyLinkedListNode next
#
#
def insertNodeAtHead(llist, data):
    # Write your code here
    new_node = SinglyLinkedListNode(data)
    new_node.next = llist
    return new_node