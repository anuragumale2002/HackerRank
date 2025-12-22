# Complete the insertNodeAtTail function below.

#
# For your reference:
#
# SinglyLinkedListNode:
#     int data
#     SinglyLinkedListNode next
#
#
def insertNodeAtTail(head, data):
    new_node = SinglyLinkedListNode(data)
    if head is None:
        head = new_node
    else:
        current = head
        while current.next:
            current = current.next
        current.next = new_node
    return head