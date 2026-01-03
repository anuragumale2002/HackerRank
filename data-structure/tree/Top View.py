"""
Node is defined as
self.left (the left child of the node)
self.right (the right child of the node)
self.info (the value of the node)
"""
def topView(root):
    #Write your code here
    from collections import deque, defaultdict
    if root is None:
        return

    # Dictionary to store the top view of the binary tree
    top_view = {}

    # Queue to store nodes along with horizontal distance
    queue = deque([(root, 0)])

    while queue:
        node, hd = queue.popleft()

        # If the horizontal distance is not already in the dictionary
        if hd not in top_view:
            top_view[hd] = node.info

        # Enqueue left and right children of the node with updated horizontal distance
        if node.left:
            queue.append((node.left, hd - 1))
        if node.right:
            queue.append((node.right, hd + 1))

    # Print the values in the top view dictionary sorted by horizontal distance
    for key in sorted(top_view):
        print(top_view[key], end=' ')