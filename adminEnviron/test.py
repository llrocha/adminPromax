import os.path
#from tree import TreeNode

root = None
parent = None

tree = {}

def insert_dict(d, l):
    if(len(l)):
        if(not l[0] in d.keys()):
            d[l[0]] = {}
        d[l[0]] = insert_dict(d[l[0]], l[1:])
    else:
        d = {}
    return d


def print_tree(d, l):
    l += 1
    for k, v in d.items():
        
        if(len(v) > 0):
            print('{0}<li><a href="#">{1}</a>\n{0}  <ul>'.format('\t'*l, k))
            print_tree(v, l)
            print('{0}  </ul>\n{0}</li>'.format('\t'*l))
        else:
            print('{0}<li>{1}</li>'.format('\t'*l, k))


fp = open('input.test', 'r')
for path in fp:    
    path = path.split()[0]
    path = path.split('/')
    path.remove('')
    insert_dict(tree, path)
fp.close()

print('<div class="container" style="margin-top:30px;">')
print('    <div class="row">')
print('        <div class="col-md-12">')
print('<ul id="tree1">')

print_tree(tree, 0)

print('</ul>')
print('        </div>')
print('    </div>')
print('</div>')