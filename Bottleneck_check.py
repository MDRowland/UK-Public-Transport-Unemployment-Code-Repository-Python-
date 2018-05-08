import sys
import operator

def file_len(fname):
    with open(fname) as f:

        i = 0
        for i, l in enumerate(f):
            pass
    return i + 1

def mst_matrix(ARCS, Nodes, CURRNODE):
    Initial = [CURRNODE]
    Translt = [CURRNODE]
    MST = 'Output Files/'+str(Places)+'/'+str(Places)+"_MST/MST_"+str(nodetype)+'_'+str(Method)+'_'+str(Start_Times_Tuple[arrivltme_list.index(arrivltme)][:2])+'_'+str(Start_Times_Tuple[arrivltme_list.index(arrivltme)][3:5])+'_'+str(CURRNODE)+'_'+str(Cost_matrix_name)+'.txt'
    MST_Size = file_len(MST)
    ARC_Size = file_len(ARCS)
    f = open(MST)
    line = f.readlines()
    g = open(ARCS)
    aline = g.readlines()
    n = 0
    while n < MST_Size:
        luc = line[n].split()          #nth arc on the MST is selected
        k = 0
        while k < ARC_Size:
            auc = aline[k].split()      #Filter through all possible arcs till current one is found
            if auc[0] == luc [0]:
                break
            k+=1
        if luc[1] == '1':                   #If the direction is from the first arc to  
            Initial.append(auc[2].rstrip()) #the second then first node gets added to the first
            Translt.append(auc[1].rstrip()) #list, otherwise is added to the second
        if luc[1] == '-1':                  #this matrix allows code to visualise the connection between nodes
            Initial.append(auc[1].rstrip())
            Translt.append(auc[2].rstrip())
        n+=1
    f.close()
    return(Initial, Translt)


nodenum=len(Nodes)
TallyPlaceholder =[element[0] for element in Nodes]
n = 0
Tally = [0]*nodenum
print("Bottlenecks Starting...")
while n < nodenum:  #Goes to total length of the nodes considered
    l = 0
    unrchpath=str("Output Files/"+str(Places)+"/"+str(Places)+'_UNRCH/UNRCH'+str(nodetype)+'_'+str(Method)+'_'+str(Start_Times_Tuple[arrivltme_list.index(arrivltme)][:2])+'_'+str(Start_Times_Tuple[arrivltme_list.index(arrivltme)][3:5])+'_'+str(Nodes[n][0])+'_'+str(Cost_matrix_name)+"_maxval_"+str(Max_Cost)+'.txt')
    unrchlen = file_len(unrchpath)
    Initial, Translt = mst_matrix(arc_file_loc, Nodes, Nodes[n][0]) #Gotta do this every time as it's defined in relation to a source node
    g = open(unrchpath)
    gline = g.readlines()
    if unrchlen > 1:
        while l < unrchlen:
            CurrNode = gline[l].split()[0]
            while True:
                trans_index = Initial.index(CurrNode)
                matcher = str(Translt[trans_index])
                if matcher in g.read().splitlines():
                    CurrNode = Translt[trans_index]     #As soon as it finds a place not in the unreachable nodes section,
                else:                                       #it gives it a tally as a "bottleneck"
                    var = Tally[TallyPlaceholder.index(CurrNode)]
                    Tally[TallyPlaceholder.index(CurrNode)]= var + 1#Need a fixed relation for the Tally so TallyPlaceholder is used for that
                    break
            l+=1
    
    g.close()
    if round((n/nodenum)*100)in thresholds:
        if round((n/nodenum)*100) != round(((n-1)/nodenum)*100):
            print("    "+str("{:5.2f}".format(round((n/nodenum)*100,2)))+"% Complete") # Prints out progress percentage for benifit of user
    
    n+=1
if os.path.exists("Output Files/"+str(Places)+"/"+str(Places)+"_BOTTLE"):
    pass
else:
    os.makedirs("Output Files/"+str(Places)+"/"+str(Places)+"_BOTTLE")
n=0
output = open("Output Files/"+str(Places)+"/"+str(Places)+'_BOTTLE/BOTTLE'+str(nodetype)+'_'+str(Method)+'_'+str(Start_Times_Tuple[arrivltme_list.index(arrivltme)][:2])+'_'+str(Start_Times_Tuple[arrivltme_list.index(arrivltme)][3:5])+'_'+str(Cost_matrix_name)+"_maxval_"+str(Max_Cost)+'.txt', "w")

while n <nodenum:
    max_index, max_value = max(enumerate(Tally), key=operator.itemgetter(1)) #Finds location and bottleneck value of a given node
    output.write(nodetype+" "+str(TallyPlaceholder.pop(max_index))+" is a bottleneck "+str(Tally.pop(max_index))+" times.\n")
    n+=1    #This removes items from nodes in this TallyPlaceholder

output.close()
print("Complete! See 'Output Folder' for details of the bottlenecks.")
