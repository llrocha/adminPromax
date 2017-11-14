
class TreeNode():
    nome = ''
    parent_node = None
    child_nodes = []

    def __init__(self, nome, parent = None):
        self.nome = nome
        if(parent):
            self.parent_node = parent

    def add(self, node):
        assert isinstance(node, TreeNode)
        child_nodes.append(node)

