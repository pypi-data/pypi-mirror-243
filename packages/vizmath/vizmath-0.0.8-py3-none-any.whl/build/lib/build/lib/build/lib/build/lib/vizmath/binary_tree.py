#%%
from math import cos, sin, pi

# todo: replace with vizmath structure

class nicks_b_tree:
    
    def __init__(self, length, levels, angle, R_tag, L_tag, y_offset, Root_tag, lineage):
        self.bi_tree_list = []
        self.length = length
        self.levels = levels
        self.angle = angle
        self.R_tag = R_tag
        self.L_tag = L_tag
        self.y_offset = y_offset
        self.Root_tag = Root_tag
        self.lineage = lineage
        self.full_binary_tree()
    
    class b_tree:
        def __init__(self, level, side, x, y, lineage, group, tree=0): 
            self.level = level
            self.side = side
            self.x = x
            self.y = y
            self.lineage = lineage
            self.group = group
            self.tree = tree
        def to_dict(self):
            return {
                'level' : self.level,
                'side' : self.side,
                'x' : self.x,
                'y' : self.y,
                'lineage' : self.lineage,
                'group' : self.group,
                'tree' : self.tree }

    def generate_points(self, start_angle, start_x, start_y, angle, length, level):
        #sides
        length_a = length*cos(angle*pi/180.)
        length_b = length*cos((90.-angle)*pi/180.)
        #right
        xs_a1 = start_x + (length/2.)*cos(-start_angle*pi/180.)
        ys_a1 = start_y + (length/2.)*sin(-start_angle*pi/180.)
        xs_a2 = xs_a1 + (length_a/2.)*cos((-start_angle-angle+180.)*pi/180.)
        ys_a2 = ys_a1 + (length_a/2.)*sin((-start_angle-angle+180.)*pi/180.)
        xa = xs_a2 + (length_a)*cos((-start_angle-angle+90.)*pi/180.)
        ya = ys_a2 + (length_a)*sin((-start_angle-angle+90.)*pi/180.)
        #left
        xs_b1 = start_x + (length/2.)*cos((-start_angle+180.)*pi/180.)
        ys_b1 = start_y + (length/2.)*sin((-start_angle+180.)*pi/180.)
        xs_b2 = xs_b1 + (length_b/2.)*cos((-start_angle+(90.-angle))*pi/180.)
        ys_b2 = ys_b1 + (length_b/2.)*sin((-start_angle+(90.-angle))*pi/180.)
        xb = xs_b2 + (length_b)*cos((-start_angle+(90.-angle)+90.)*pi/180.)
        yb = ys_b2 + (length_b)*sin((-start_angle+(90.-angle)+90.)*pi/180.)
        #angles
        aa = start_angle + angle
        ab = 270. + start_angle + angle
        return xa, ya, aa, length_a, xb, yb, ab, length_b, level + 1
    
    def binary_tree(self, start_angle, length, level, levels, x, y, angle, lineage, R_tag, L_tag):
        if level == levels:
            return
        xa, ya, aa, length_a, xb, yb, ab, length_b, level = self.generate_points(start_angle, x, y, angle, length, level)
        #output
        #-- R-lines
        self.bi_tree_list.append(self.b_tree(level, self.R_tag, xa, ya, lineage + self.R_tag, lineage + '_' + lineage + self.R_tag))
        self.bi_tree_list.append(self.b_tree(level, self.R_tag, xa, ya, lineage + self.R_tag, lineage + self.R_tag + '_' + lineage + self.R_tag + self.R_tag)) #+'RR'
        self.bi_tree_list.append(self.b_tree(level, self.R_tag, xa, ya, lineage + self.R_tag, lineage + self.R_tag + '_' + lineage + self.R_tag + self.L_tag)) #+'RL'
        #-- L-lines
        self.bi_tree_list.append(self.b_tree(level, self.L_tag, xb, yb, lineage + self.L_tag, lineage + '_' + lineage + self.L_tag))
        self.bi_tree_list.append(self.b_tree(level, self.L_tag, xb, yb, lineage + self.L_tag, lineage + self.L_tag + '_' + lineage + self.L_tag + self.R_tag)) #+'LR'
        self.bi_tree_list.append(self.b_tree(level, self.L_tag, xb, yb, lineage + self.L_tag, lineage + self.L_tag + '_' + lineage + self.L_tag + self.L_tag)) #+'LL'
        #right
        self.binary_tree(aa, length_a, level, self.levels, xa, ya, self.angle, lineage + R_tag, R_tag, L_tag)
        #left
        self.binary_tree(ab, length_b, level, self.levels, xb, yb, self.angle, lineage + L_tag, R_tag, L_tag)
    
    def full_binary_tree(self):
        self.binary_tree(0., self.length, 0, self.levels, 0., 0., self.angle, self.lineage, self.R_tag, self.L_tag)
        self.bi_tree_list.append(self.b_tree(0, '', 0., -self.y_offset, self.Root_tag, '_'))
        self.bi_tree_list.append(self.b_tree(0, '', 0., 0., self.Root_tag, '_'))
        self.bi_tree_list.append(self.b_tree(0, '', 0., 0., self.Root_tag, '' + '_' + self.R_tag))
        self.bi_tree_list.append(self.b_tree(0, '', 0., 0., self.Root_tag, '' + '_' + self.L_tag))
        for o in self.bi_tree_list: o.y += self.y_offset

import copy
import functions as vf
import matplotlib.pyplot as plt

#%%
# fbt = nicks_b_tree(length=10, levels=10, angle=30, R_tag='M', L_tag='F', y_offset=5, Root_tag='dog', lineage='')
# bi_tree_list = fbt.bi_tree_list
# bi_tree_list_clone = copy.deepcopy(bi_tree_list)
# xmax = max([o.x for o in bi_tree_list])
# for o in bi_tree_list: 
#     o.tree = 1
# trees = 6
# for i in range(trees-1):
#     bi_tree_list_2 = []
#     bi_tree_list_2 = copy.deepcopy(bi_tree_list_clone)
#     for o in bi_tree_list_2: 
#         o.x += xmax*(i+1)
#         o.tree = i+2
#     bi_tree_list.extend(bi_tree_list_2)


fbt = nicks_b_tree(length=10, levels=14, angle=40, R_tag='M', L_tag='F', y_offset=30, Root_tag='dog', lineage='')
bi_tree_list = fbt.bi_tree_list
bi_tree_list_clone = copy.deepcopy(bi_tree_list)
xmax = max([o.x for o in bi_tree_list])
for o in bi_tree_list: 
    o.tree = 1
trees = 3
for i in range(trees-1):
    bi_tree_list_2 = []
    bi_tree_list_2 = copy.deepcopy(bi_tree_list_clone)
    for o in bi_tree_list_2: 
        o.x *= i+1
        o.tree = i+2
    bi_tree_list.extend(bi_tree_list_2)

#plot
x = [o.x for o in bi_tree_list]
y = [o.y for o in bi_tree_list]
max_x = max(x)
max_y = max(y)

offset = 0.0
stretch = 5.
angle = 0.

for o in bi_tree_list: 
    o.x = vf.rescale(o.x, 0.0, max_x, 0., 1.)
    o.y = vf.rescale(o.y, 0.0, max_y, 0., 1.)
    o.x, o.y = vf.polarize(o.x, stretch, o.y, offset)
    o.x = vf.rescale(o.x, 0.0, 1+offset, 0., 1.)
    o.y = vf.rescale(o.y, 0.0, 1+offset, 0., 1.)
    o.x, o.y =  vf.rotate(o.x, o.y, angle, 0., 0.)
    
x = [o.x for o in bi_tree_list]
y = [o.y for o in bi_tree_list]

plt.scatter(x, y)
plt.gca().set_aspect('equal', adjustable='box')
plt.show()