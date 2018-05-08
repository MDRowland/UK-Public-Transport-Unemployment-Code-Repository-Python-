#####
#Script to find the mean cost per head of (unemployed) population to reach any given node from the nodes that they are resident
#So all unemployed individuals everywhere in the network are considered, be they near or far
#####
import sys
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def PopCostFinder(Nodes, CTNfile):   
    TOT_Weight = 0
    TOT_squares = 0
    TOT_pop = 0
    k = 0
    N = []
    Pop = []
    while k < len(Nodes):
        N.append(Nodes[k][0])
        Pop.append(eval(Nodes[k][1])*float(Nodes[k][2]))
        k+=1
    l=0

    g = open(CTNfile, "r")
    line = g.readlines()
    while l < file_len(CTNfile):
        #print("Check")
        cline = line[l].split()
        #print("Check")
        currpop = float(Pop[N.index(cline[0])])
        #print("Check")
        TOT_pop += currpop
        TOT_Weight += (float(cline[1])*currpop)
        
        TOT_squares += ((currpop)*float(cline[1])**2)
        l+=1
    return(TOT_Weight, TOT_pop, TOT_squares)

             # Defining the file locations of the Node and Arc data.

f_length = len(Nodes)
if os.path.exists("Output Files/"+str(Places)+"/"+str(Places)+"_PopCosts"):
    pass
else:
    os.makedirs("Output Files/"+str(Places)+"/"+str(Places)+"_PopCosts")
output =open("Output Files/"+str(Places)+"/"+str(Places)+"_PopCosts/PopCost"+str(nodetype)+'_'+str(Method)+'_'+str(Start_Times_Tuple[arrivltme_list.index(arrivltme)][:2])+str(Start_Times_Tuple[arrivltme_list.index(arrivltme)][3:5])+'.txt',"w")
#print(f_length)
n = 0
while n < f_length:
    
    CTNfile = str("Output Files/"+str(Places)+"/"+str(Places)+'_CTN/COSTS_'+str(nodetype)+'_'+str(Method)+'_'+str(Start_Times_Tuple[arrivltme_list.index(arrivltme)][:2])+'_'+str(Start_Times_Tuple[arrivltme_list.index(arrivltme)][3:5])+'_'+str(Nodes[n][0])+'_'+str(Cost_matrix_name)+'.txt')
    
    TOT_weight, TOT_pop, TOT_squares = PopCostFinder(Nodes,CTNfile)

    #print("The Mean value is"+" "+str(TOT_weight/TOT_pop))              # Cost per head of pop (mean)
    
    #print("The standard deviation is"+" "+str(((TOT_squares/TOT_pop)-(TOT_weight/TOT_pop)**2)**.5))
    
    mean = TOT_weight/TOT_pop
    variance = ((TOT_squares/TOT_pop)-(TOT_weight/TOT_pop)**2)**.5
    output.write(str(Nodes[n][0])+" "+str(mean)+" "+str(variance)+"\n")
    n+=1
print(str(Places)+" complete! See the '"+str(Places)+"' directory for the results.")
output.close()
