import sys
import numpy as np

def file_len(fname):              
    i=0           
    with open(fname) as f:        
        for i, l in enumerate(f): 
            pass                  
    return i + 1               
singles_only = 0  #Won't use singles
fare = 4.5  #Current Dayrider cost
def Dijkstra_mst(Nodes, arc, source):
    '''A function tht will find the minimum spanning tree of a set of nodes in terms of the arcs chosen.'''
    NULL = ["NULL", "NULL", "NULL", float("inf")]  # Defining a null arc to test against, of infinite length.
    S = [source]
    Cost_to_node = [0]
    ARCS = []
    nodes_length = len(Nodes)                                          # Finds the number of nodes and arcs respectively
    arcs_length = int(file_len(arc))
    n = 0
    f = open(arc, "r")
    line = f.readlines()
    f.close()
    DIR = []                                                                    # Empty list for storing the direction traveled along
    while len(S) < nodes_length:                                                # Ensures we can search for a link to every node using this while loop
                                   
        k = 0
        AUC = NULL
        CostToNode_UC = float("inf")                                            # Setting "Arc Under Consideration" - the arc currently considered the shortest availible - to the NULL arc.
        
        while k < arcs_length:                                                  # While loop to extract from file the data about the arcs
                                                                                 # Ensuring the data extracted from file is treated as a list
            cl = line[k].split()                                                                   # Reading file
            if(cl[1] in S):                                                     # If the "origin" is in the currently considered node set, then this arc will be considered.
                if(cl[2] not in S):
                    cost = Cost_matrix[0]*fare
                    x=3
                    while x<len(cl)-1:
                        cost += float(cl[x])*float(Cost_matrix[x-2])
                        x+=1
                                                                                # If the "destinaiton" is in the currently considered node set, then this arc will not be considered, as would visit already visited node.
                    CostToNode = Cost_to_node[S.index(cl[1])]+float(cost)       # Setting current cost to node as the value to reach the connecting node, plus the value to reach the considered node
                    if(CostToNode < CostToNode_UC):                             # Testing if length is shorter than currently shortest
                        AUC = cl                                                # Conditions satisfied, this is now the shortest arc.
                        direction = 1                                           # Direction refers to the direction travesed along the arc, 1 being from the first listed node to the second, and -1 vice versa.
                        CostToNode_UC = CostToNode
                              

            elif (cl[2] in S):                                                  # If the "destinaiton" is in the currently considered node set, then this arc will be considered.
                if (cl[1] not in S):
                    cost = Cost_matrix[0]*fare
                    x=3
                    while x<len(cl)-1:
                        cost += float(cl[x])*float(Cost_matrix[x-2])
                        x+=1
                    CostToNode = Cost_to_node[S.index(cl[2])]+float(cost)       # If the "origin" is in the currently considered node set, then this arc will not be considered, as would visit already visited node.
                    if (CostToNode< CostToNode_UC):                             # Testing if length is shorter than currently shortest arc
                        AUC = cl                                                # Conditions satisfied, this is now the shortest arc.
                        direction = -1
                        CostToNode_UC = CostToNode
            k+=1
        if AUC[0] != "NULL":                                                    # If the shortest arc found is not the NULL arc, then it will be added to the minimum spanning tree (ARCS).
            ARCS.append(AUC[0])
            DIR.append(direction)
            Cost_to_node.append(CostToNode_UC)
        if (AUC[1] in S):                                                       # This if elif pair find which node the arc is attached to that isn't already connected, and add it to the list of connected nodes "S"
            S.append(AUC[2])
        elif (AUC[2] in S):
            S.append(AUC[1])
        
        n+=1                                                                    # The n term is used to ensure an infinite loop is not created in the event that all nodes are not actually connected together, and prints appropriate error message.
        if n == (len(S)+2):
            print("Some points are disconnected from the source!")
            sys.exit()
            break
    return(S, ARCS, DIR, Cost_to_node)                                          # Returns the list of connected nodes (primarily for debugging reasons) and the arcs that compose the MST.




arc_file_loc = str("Output Files/"+str(Places)+"/"+str(Places)+'_Arcs/Arcs_'+str(nodetype)+'_'+str(Method)+'_'+str(Start_Times_Tuple[arrivltme_list.index(arrivltme)][:2])+str(Start_Times_Tuple[arrivltme_list.index(arrivltme)][3:5])+'.txt')


   
                                                                                # Defining the file locations of the Node and Arc data.
k = 0
if os.path.exists('Output Files/'+str(Places)+'/'+str(Places)+"_MST"):
    pass
else:
    os.makedirs('Output Files/'+str(Places)+'/'+str(Places)+"_MST")
if os.path.exists('Output Files/'+str(Places)+'/'+str(Places)+"_CTN"):
    pass
else:
    os.makedirs('Output Files/'+str(Places)+'/'+str(Places)+"_CTN")
print("Starting Djikstras' Algorithm ...")
while k < (int(len(Nodes))):                                       # While loop to generate and save the MST of each node in question, in this case all of them.
                   
    source = Nodes[k][0]

    S, ARCS, DIR, Cost_to_node = Dijkstra_mst(Nodes, arc_file_loc, source)
    file_loc = ('Output Files/'+str(Places)+'/'+str(Places)+"_MST/MST_"+str(nodetype)+'_'+str(Method)+'_'+str(Start_Times_Tuple[arrivltme_list.index(arrivltme)][:2])+'_'+str(Start_Times_Tuple[arrivltme_list.index(arrivltme)][3:5])+'_'+str(source)+'_'+str(Cost_matrix_name)+'.txt')
    if os.path.exists(file_loc):
        if round((k/len(Nodes))*100)in thresholds:
            if round((k/len(Nodes))*100) != round(((k-1)/len(Nodes))*100):
                print("    "+str("{:5.2f}".format(round((k/len(Nodes))*100,2)))+"% Complete") # Prints out progress percentage for benifit of user

        k+=1
        continue
    # Code to write to a file the minimum spanning arcs for use
    file = open(file_loc,"w")
    n = 0

    m=0

    while n < len(ARCS):
        file.write(str(ARCS[n])+" "+str(DIR[n])+"\n")
        n+=1
    file.close()
    
    CTNfile = open("Output Files/"+str(Places)+"/"+str(Places)+'_CTN/COSTS_'+str(nodetype)+'_'+str(Method)+'_'+str(Start_Times_Tuple[arrivltme_list.index(arrivltme)][:2])+'_'+str(Start_Times_Tuple[arrivltme_list.index(arrivltme)][3:5])+'_'+str(source)+'_'+str(Cost_matrix_name)+'.txt',"w")
    
    while m < len(Cost_to_node):
        CTNfile.write(str(S[m])+" "+str(Cost_to_node[m])+"\n")
        m+=1
    CTNfile.close()
    if round((k/len(Nodes))*100)in thresholds:
                if round((k/len(Nodes))*100) != round(((k-1)/len(Nodes))*100):
                    print("    "+str("{:5.2f}".format(round((k/len(Nodes))*100,2)))+"% Complete") # Prints out progress percentage for benifit of user
            

    k+=1
    
print(str(Places)+" "+str(nodetype)+" at "+str(Start_Times_Tuple[arrivltme_list.index(arrivltme)][:2])+'_'+str(Start_Times_Tuple[arrivltme_list.index(arrivltme)][3:5])+" via "+str(Method)+"complete! See 'NODE_MST_Files' Folder for the minimum spanning trees, and 'CostsToNode' Folder for the costs to reach each node.")

#########################################################################################################
# Footnotes:                                                                                            #
# The Dijkstra function relies on the node document only for the total number of nodes,                 #
# This means that if nodes that aren't actually listed in nodes file are connected to by arcs or nodes  # 
# listed arent,programme will be unaware and thus potentially stop short of a complete MST.             #
# Preventing this will require a consistency check at some point before this, ideally after the lists   #
# are created.                                                                                          #
#########################################################################################################
