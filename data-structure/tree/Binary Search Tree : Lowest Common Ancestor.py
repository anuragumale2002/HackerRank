class Node:
    def __init__(self, info): 
        self.info = info  
        self.left = None  
        self.right = None 
        self.level = None 

    def __str__(self):
        return str(self.info) 

class BinarySearchTree:
    def __init__(self): 
        self.root = None

    def create(self, val):  
        if self.root == None:
            self.root = Node(val)
        else:
            current = self.root
         
            while True:
                if val < current.info:
                    if current.left:
                        current = current.left
                    else:
                        current.left = Node(val)
                        break
                elif val > current.info:
                    if current.right:
                        current = current.right
                    else:
                        current.right = Node(val)
                        break
                else:
                    break

# Enter your code here. Read input from STDIN. Print output to STDOUT
'''
class Node:
      def __init__(self,info): 
          self.info = info  
          self.left = None  
          self.right = None 
           

       // this is a node of the tree , which contains info as data, left , right
'''

def lca(root, v1, v2):
  #Enter your code here
  
  # Base case: if root is None
    if root is None:
        return None
    
    # If both v1 and v2 are smaller than root, LCA lies in left subtree
    if v1 < root.info and v2 < root.info:
        return lca(root.left, v1, v2)
    
    # If both v1 and v2 are greater than root, LCA lies in right subtree
    if v1 > root.info and v2 > root.info:
        return lca(root.right, v1, v2)
    
    # If v1 and v2 are on different sides of root, or one of them is equal to root
    # then root is the LCA
    return root