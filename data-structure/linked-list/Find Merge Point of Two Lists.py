# Complete the findMergeNode function below.

#
# For your reference:
#
# SinglyLinkedListNode:
#     int data
#     SinglyLinkedListNode next
#
#
def findMergeNode(head1, head2):
    current1 = head1
    current2 = head2

    while current1 != current2:
        if current1.next is None:
            current1 = head2
        else:
            current1 = current1.next

        if current2.next is None:
            current2 = head1
        else:
            current2 = current2.next

    return current1.data