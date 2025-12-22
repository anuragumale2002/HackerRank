#
# Complete the 'reversePrint' function below.
#
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

def reversePrint(llist):
    # Write your code here
    stack = []
    current = llist
    while current:
        stack.append(current.data)
        current = current.next
    while stack:
        print(stack.pop())