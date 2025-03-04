#!/usr/bin/env python


__author__ = "Jing Zhang"
__email__ = "jingzbu@gmail.com"
__status__ = "Development"


from util import *
import numpy as np
from math import exp


link_label_dict = zload('../temp_files/link_label_dict.pkz')
link_label_dict_ = zload('../temp_files/link_label_dict_.pkz')
link_length_dict = zload('../temp_files/link_length_dict.pkz')

# number of links
m = 24
# number of routes (obtained by counting the rows with '->' in 'path-link_incidence.txt')
r = 140

# initialize the path-link incidence matrix
A = np.zeros((m, r))

# read in the manually created path-link incidence file 
# create path-link incidence matrix A
with open('../temp_files/path-link_incidence.txt', 'r') as the_file:
    # path counts
    i = 0  
    for row in the_file:
        if '->' in row:
            for j in range(m):
                if link_label_dict[str(j)] in row:
                    A[j, i] = 1
            i = i + 1
    assert(i == r)
zdump(A, '../temp_files/path-link_incidence_matrix.pkz')

# link_length_dict['0'].length

# link_label_dict_

# read in the manually created path-link incidence file 
# calculate length of each route

length_of_route_list = []
with open('../temp_files/path-link_incidence.txt', 'r') as the_file:
    for row in the_file:
        if '->' in row:
            link_list = []
            node_list = []
            for i in row.split('->'):
                node_list.append(int(i))
            for i in range(len(node_list))[:-1]:
                link_list.append('%d->%d' %(node_list[i], node_list[i+1]))
            length_of_route = sum([link_length_dict[str(link_label_dict_[link])].length \
                                  for link in link_list])
            length_of_route_list.append(length_of_route)
zdump(length_of_route_list, '../temp_files/length_of_route_list.pkz')

# length_of_route_list[139]

OD_pair_label_dict = zload('../temp_files/OD_pair_label_dict.pkz')

# OD_pair_label_dict['(1, 2)']

# read in the manually created path-link incidence file 
# create label of each route
OD_pair_route_label_list = []
OD_pair_idx_list = []
route_idx_list = []
with open('../temp_files/path-link_incidence.txt', 'r') as the_file:
    route_idx = 0
    for row in the_file:
        if '->' in row:
            node_list = []
            for i in row.split('->'):
                node_list.append(int(i))
            OD_pair_idx = OD_pair_label_dict[str((node_list[0], node_list[-1]))]
            OD_pair_idx_list.append(OD_pair_idx)
            route_idx_list.append(route_idx)
            OD_pair_route_label_list.append((OD_pair_idx, route_idx))
            route_idx += 1

OD_pair_route_dict = {}

for i in range(56):
    route_list = []
    for r in range(140):
        if OD_pair_idx_list[r] == i:
            route_list.append(r)
    OD_pair_route_dict[str(i)] = route_list
zdump(OD_pair_route_dict, '../temp_files/OD_pair_route_dict.pkz')

# OD_pair_route_dict['6']


# calculate route choice probability matrix P
# logit choice parameter
theta = 0.5

P = np.zeros((56, 140))
for i in range(56):
    for r in OD_pair_route_dict[str(i)]:
        P[i, r] = exp(- theta * length_of_route_list[r]) / \
                    sum([exp(- theta * length_of_route_list[j]) \
                         for j in OD_pair_route_dict[str(i)]])
zdump(P, '../temp_files/logit_route_choice_probability_matrix.pkz')

# P[2, 3], P[2, 4], P[2, 5]

# length_of_route_list[3], length_of_route_list[4], length_of_route_list[5]

# sum(P[2,:])

link_list = []
node_list = []
for i in '1->2->3->5->4'.split('->'):
    node_list.append(int(i))
for i in range(len(node_list))[:-1]:
    link_list.append('%d->%d' %(node_list[i], node_list[i+1]))

# node_list
# link_list
# range(5)[:-1]
# link_label_dict
# A[23]
# np.size(A, 1)
# B = np.ones((140, 2))
# np.dot(A, B)
