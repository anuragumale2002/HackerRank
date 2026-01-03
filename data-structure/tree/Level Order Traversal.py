"""
Node is defined as
self.left (the left child of the node)
self.right (the right child of the node)
self.info (the value of the node)
"""
def levelOrder(root):
    #Write your code here
    if not root:
        return
    queue = []
    queue.append(root)
    while queue:
        node = queue.pop(0)
        print(node.info, end=" ")
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)