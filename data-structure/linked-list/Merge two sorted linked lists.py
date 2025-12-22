# Complete the mergeLists function below.

#
# For your reference:
#
# SinglyLinkedListNode:
#     int data
#     SinglyLinkedListNode next
#
#
def mergeLists(head1, head2):
    # If either list is empty, return the other list
    if not head1:
        return head2
    if not head2:
        return head1

    # Initialize the merged list head and tail
    if head1.data <= head2.data:
        merged_head = head1
        head1 = head1.next
    else:
        merged_head = head2
        head2 = head2.next
    merged_tail = merged_head

    # Merge the two lists
    while head1 and head2:
        if head1.data <= head2.data:
            merged_tail.next = head1
            head1 = head1.next
        else:
            merged_tail.next = head2
            head2 = head2.next
        merged_tail = merged_tail.next

    # Append the remaining elements
    if head1:
        merged_tail.next = head1
    else:
        merged_tail.next = head2

    return merged_head