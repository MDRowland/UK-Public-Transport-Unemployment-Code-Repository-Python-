import sys
import os
def file_len(fname):
    i = 0
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def Cost_Constrained_Reach_Nodes(Nodes, Max_Cost, cost_to_node):
    n = 0
    nodelen = len(Nodes)
    can_reach = []
    cannot_reach = []
    f = open(cost_to_node, "r")
    line = f.readlines()  #if the cost of getting from x node is greater than
    while n < nodelen:    #whatever was selected then that node is added to the list for this node source
        cline = line[n].split()
        if float(cline[1]) > float(Max_Cost):
            cannot_reach.append(cline[0])
        else:
            can_reach.append(cline[0])
        n+=1
    return(cannot_reach)

l = 0

if os.path.exists("Output Files/"+str(Places)+"/"+str(Places)+"_UNRCH"):
    pass
else:
    os.makedirs("Output Files/"+str(Places)+"/"+str(Places)+"_UNRCH")
nodelen = len(Nodes)
while l < nodelen:
    nuc = Nodes[l]
    CTNfile = str("Output Files/"+str(Places)+"/"+str(Places)+'_CTN/COSTS_'+str(nodetype)+'_'+str(Method)+'_'+str(Start_Times_Tuple[arrivltme_list.index(arrivltme)][:2])+'_'+str(Start_Times_Tuple[arrivltme_list.index(arrivltme)][3:5])+'_'+str(Nodes[l][0])+'_'+str(Cost_matrix_name)+'.txt')
    cannot_reach = Cost_Constrained_Reach_Nodes(Nodes, Max_Cost,CTNfile)
    g = open(str("Output Files/"+str(Places)+"/"+str(Places)+'_UNRCH/UNRCH'+str(nodetype)+'_'+str(Method)+'_'+str(Start_Times_Tuple[arrivltme_list.index(arrivltme)][:2])+'_'+str(Start_Times_Tuple[arrivltme_list.index(arrivltme)][3:5])+'_'+str(Nodes[l][0])+'_'+str(Cost_matrix_name)+"_maxval_"+str(Max_Cost)+'.txt'), "w")
    n = 0
    while n < len(cannot_reach):
        g.write(cannot_reach[n]+"\n")
        n+=1
    g.close()
    
    l+=1
print("Complete! See 'Unreachable Nodes' for lists of unreachable nodes.")

    
