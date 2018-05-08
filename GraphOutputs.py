import matplotlib.pyplot as plt
from matplotlib.colors import Colormap, Normalize
import numpy as np
import scipy.stats
import time,sys,datetime,os,re
from tabulate import tabulate
####### Generic Functions ##########
def file_len(fname):              ##
    i=0           ##
    with open(fname) as f:        ##
        for i, l in enumerate(f): ##
            pass                  ##
    return i + 1                  ##
####################################
x,y,size,jobs,name,unemployfrac,pop=[],[],[],[],[],[],[]
f = open("Programme Files/LSOA_dictionary.txt")
LSOA_dictionary = eval((f.readline()))
f.close()
f = open("Programme Files/MSOA_dictionary.txt")
MSOA_dictionary = eval((f.readline()))
f.close()
Places=[]
print("Type the name of the authorities you would like to consider. \n"+"To stop adding enter 'done'.\n")
plcename = input()
nodetypes = ['LSOA','MSOA']
while True:
    if plcename in LSOA_dictionary:
        Places.append(plcename)
        plcename=input("Give another input:\n")
        continue
    elif plcename=='done':
        if len(Places)>0:
            print('Places are confirmed.')
            break

        else:
            print('You must input at least one place.')
            plcename=input("Give another input:\n")
            pass
    else:
        print('Invalid placename')
        plcename=input("Give another input:\n")
        pass
Places.sort()
Places_text =""
for place in Places:
    Places_text+=str(" "+str(place))
print(Places_text)
while True:
    print("Type the name of the census level you would like to consider. \nValid types are LSOA or MSOA.") 
    nodetype = input()
    if nodetype in nodetypes:
        break
    else:
        print('Invalid type')
        pass

Nodes=[]
for placename in Places:         #Takes all the considered places and puts the nodes in this list
    node_loc=str("Locality Files/"+str(placename)+'_Nodes/'+str(nodetype)+'s.txt')
    node_number = file_len(node_loc)
    f = open(node_loc, "r")
    line = f.readlines()
    
    for n in range(node_number):
        Nodes.append(line[n].split()) 


for node in Nodes:
    x.append(float(node[4]))
    y.append(float(node[3]))
    pop.append(int(node[1]))
    size.append(int(node[1])/100)
    jobs.append(int(node[5]))
    name.append(node[0])
    unemployfrac.append(float(node[2]))

#labels = ['point{0}'.format(i) for i in range(len(Nodes))]

plt.scatter(x,y,c=jobs,s=size,cmap=plt.get_cmap("PRGn"),norm=Normalize(vmin=0,vmax=2000),edgecolors="gainsboro")
#for legp, x, y in zip(name, x, y):
 #   plt.annotate(
  #      legp,
   #     xy=(x, y), xytext=(-20, 20),
    #    textcoords='offset points', ha='right', va='bottom',
     #   bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5))
        #arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'))
plt.title(nodetype+" in "+Places_text+"\ncoloured according to number of target jobs.")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.figure( figsize=(50,50))
plt.savefig("Figures/"+nodetype+"_in_"+Places_text+"_target_jobs.png")
plt.close()
plt.scatter(x,y,s=size,c=unemployfrac,cmap=plt.get_cmap("seismic"),norm=Normalize(vmin=0,vmax=.4),edgecolors="gainsboro")
plt.title(nodetype+" in "+Places_text+"\ncoloured by unemployment fraction.")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
#plt.show()
plt.savefig("Figures/"+nodetype+"_in_"+Places_text+"_unemployment.png")
plt.close()
##Pop against unemployment frac
print("Correlation between fraction of unemployed population and total population")
print(scipy.stats.pearsonr(unemployfrac,pop))
plt.plot(unemployfrac,pop,'x')
plt.title("Population of "+nodetype+"s against unemployment rates in those "+nodetype+"s in\n"+Places_text+".")
plt.xlabel("Unemployment Fraction")
plt.ylabel("Population")
plt.savefig("Figures/"+nodetype+"_in_"+Places_text+"_pop_unemploy.png")
plt.close()
##Pop against jobs
print("Correlation between target jobs and total population")
print(scipy.stats.pearsonr(jobs,pop))
plt.plot(jobs,pop,'x')
plt.title("Population of "+nodetype+"s against target jobs in those "+nodetype+"s in\n"+Places_text+".")
plt.xlabel("Target Jobs")
plt.ylabel("Population")
plt.savefig("Figures/"+nodetype+"_in_"+Places_text+"_pop_target_job.png")
plt.close()
##Jobs agianst unemplyoement
print("Correlation between fraction of unemployed population and target jobs")
print(scipy.stats.pearsonr(unemployfrac,jobs))
plt.plot(unemployfrac,jobs,'x')
plt.title("Target jobs in "+nodetype+"s against unemployment rates in those "+nodetype+"s in\n"+Places_text+".")
plt.ylabel("Target Jobs")
plt.xlabel("Unemployment Fraction")
plt.savefig("Figures/"+nodetype+"_in_"+Places_text+"_unemployment_target_job.png")
plt.close()
cost_tuple,unemployfrac2=[],[]
Start_Times_Tuple=[]
print('Please give the shift start arrival times you would like to consider.\nThese should be of the format HH:MM. To cease adding times type "done".\nNote that it may be advisable to input the arrival time as ten minutes prior to shift start.')
while True:
    timetext=input()                # This allows user to define sets of arrival times
    style=re.compile('^[0-9]{2}:[0-9]{2}$')
    if style.match(timetext) and int(timetext[:2])<24 and int(timetext[3:5])<60:
        Start_Times_Tuple.append(timetext)
        print('Please give further arrival times, or type "done".')
    elif timetext=='done':
        if len(Start_Times_Tuple)>0:
            print('Start times are confirmed.')
            break

        else:
            print('You must input at least one time.')
            pass
    else:
        print('The format is incorrect. Please use HH:MM.')
        pass
Transport_Mode = []    #Transit is public transport, allows multiple methods to be considered
Transport_dic = {'Public Transport':'transit','Drive':"driving",'Cycle':"bicycling",'Walk':'walking','p':'transit'}
print('\nPlease give the transport method you would like to consider.\nTo cease adding methods type "done".\nValid inputs are "Public Transport", "Drive", "Cycle", or "Walk".')
while True:
    placetext=input()                # This allows user to define transport method
    if placetext in Transport_dic:
        Transport_Mode.append(Transport_dic[placetext])
        print('Please give further modes, or type "done".')
    elif placetext=='done':
        if len(Transport_Mode)>0:
            print('Transport modes are confirmed.')
            break
        else:
            print('You must input at least one mode.')
            pass
    else:
        print('This is not a valid input.\nValid inputs are "Public Transport", "Drive", "Cycle", or "Walk".')
        pass
f=open("Programme Files/CostCoefficients.txt")
coeffdict=eval(f.readline())
f.close()
g=open("Programme Files/CostCoefficients_MetaData.txt")
meta= g.readline().split()
g.close()
Cost_matrix_name = input("Please select the cost coefficent set you would like to use for this model.\nTo add more type #, and to see the list type ~\n")
    
while True:
    if Cost_matrix_name == '#':
        exec(open("Cost_Coefficient Creator.py").read())
        Cost_matrix_name = input("Please give the name of the cost set you require.\n")
        continue
    if Cost_matrix_name == '~':
        print(tabulate(coeffdict.items(), headers=["Name","Coefficents"], tablefmt="rst"))
        print("\nCoefficents are in order: ")
        for element in meta:
            if (element !="Name"): print(element, end=" ")
        Cost_matrix_name = input("\n\nPlease give another input, or '*' to exit.\n")
        continue
    if Cost_matrix_name in coeffdict.keys():
        Cost_matrix = coeffdict[Cost_matrix_name]
        print(Cost_matrix_name+" confirmed")
        break
    else:
        print("That isn't a saved setting!\n")
            
        Cost_matrix_name = input("\n\nPlease give another input.\n")
        continue
f=open("Programme Files/MaxCost.txt")
maxcostdict=eval(f.readline())
f.close()
Max_Cost_name = input("Please select the Maximum cost you would like to consider.\nTo add more type #, and to see the list type ~\n")
    
while True:
    if Max_Cost_name == '#':
        exec(open("max_Cost Creator.py").read())
        Max_Cost_name = input("Please give the name of the max cost you require.\n")
        continue
    if Max_Cost_name == '~':
        print(tabulate(maxcostdict.items(), headers=["Name","Cost"], tablefmt="rst"))
        print("\nCoefficents are in order: ")
        for element in meta:
            if (element !="Name"): print(element, end=" ")
        Max_Cost_name = input("\n\nPlease give another input, or '*' to exit.\n")
        continue
    if Max_Cost_name in maxcostdict.keys():
        Max_Cost = maxcostdict[Max_Cost_name]
        print(Max_Cost_name+" confirmed")
        break
    else:
        print("That isn't a saved setting!")
        Max_Cost_name = input("\nPlease give another input.\n")
        continue
arrivltme_list=[]
now = datetime.datetime.now()
for start in Start_Times_Tuple:
    startday=now+datetime.timedelta(days=((8-int(now.strftime("%w"))%7)))
    arrivltme_list.append(time.mktime(time.struct_time((int(startday.year),int(startday.month),int(startday.day),int(start[:2]),int(start[3:5]),0,0,int(startday.strftime("%j")),-1))))

for arrivltme in arrivltme_list: 
        for Method in Transport_Mode:
            f = open("Output Files/"+str(Places)+"/"+str(Places)+"_PopCosts/PopCost"+str(nodetype)+'_'+str(Method)+'_'+str(Start_Times_Tuple[arrivltme_list.index(arrivltme)][:2])+str(Start_Times_Tuple[arrivltme_list.index(arrivltme)][3:5])+'.txt')
            cost_values=f.readlines()
            for element in cost_values:
                cost_tuple.append(float(element.split()[1])/60)
                for node in Nodes:
                    if str(element.split()[0])==str(node[0]):
                        unemployfrac2.append(float(node[2]))
        plt.plot(unemployfrac2,cost_tuple,"x")
        plt.title("Cost to "+nodetype+" in"+Places_text+" against unemploment there.")
        plt.savefig("Figures/CTN_"+nodetype+str(Method)+str(Start_Times_Tuple[arrivltme_list.index(arrivltme)][:2])+'_'+str(Start_Times_Tuple[arrivltme_list.index(arrivltme)][3:5])+"_unemploy_"+Places_text+".png")
        
        plt.close()
        print("Correlation between fraction of unemployed population and cost to node")
        print(scipy.stats.pearsonr(cost_tuple,unemployfrac2))

        plt.plot(jobs,cost_tuple,"x")
        plt.title("Cost to "+nodetype+" in"+Places_text+" against jobs there.")
        plt.xlabel("Jobs in "+nodetype)
        plt.savefig("Figures/CTN_"+nodetype+str(Method)+str(Start_Times_Tuple[arrivltme_list.index(arrivltme)][:2])+'_'+str(Start_Times_Tuple[arrivltme_list.index(arrivltme)][3:5])+"_jobs_"+Places_text+".png")
        
        plt.close()
        print("Correlation between fraction of unemployed population and jobs there")
        print(scipy.stats.pearsonr(jobs,unemployfrac2))
        cost_tuple = np.array(cost_tuple)
        jobs =np.array(jobs)
        plt.plot(jobs[jobs>200],cost_tuple[jobs>200],"x")
        plt.title("Cost to "+nodetype+" in"+Places_text+" against jobs there.")
        plt.xlabel("Jobs in "+nodetype)
        plt.savefig("Figures/CTN_"+nodetype+str(Method)+str(Start_Times_Tuple[arrivltme_list.index(arrivltme)][:2])+'_'+str(Start_Times_Tuple[arrivltme_list.index(arrivltme)][3:5])+"_jobs_nonlocal100_"+Places_text+".png")
        
        plt.close()
        print("Correlation between fraction of unemployed population and jobs there")
        print(scipy.stats.pearsonr(jobs[jobs>100],cost_tuple[jobs>100])) 
for arrivltme in arrivltme_list: 
        for Method in Transport_Mode:
            f = open("Output Files/"+str(Places)+"/"+str(Places)+'_BOTTLE/BOTTLE'+str(nodetype)+'_'+str(Method)+'_'+str(Start_Times_Tuple[arrivltme_list.index(arrivltme)][:2])+'_'+str(Start_Times_Tuple[arrivltme_list.index(arrivltme)][3:5])+'_'+str(Cost_matrix_name)+"_maxval_"+str(Max_Cost)+'.txt')
            lines=f.readlines()
            f.close()
            bottleneck =[]
            for node in Nodes:
                k=0
                while k<len(lines):
                    if str(lines[k].split()[1]) == str(node[0]):
                        bottleneck.append(int(lines[k].split()[5]))
                        break
                    k+=1
            plt.scatter(x,y,c=bottleneck,s=size,cmap=plt.get_cmap("spring"),norm=Normalize(vmin=0,vmax=60),edgecolors="gainsboro")
            plt.title(nodetype+" in "+Places_text+"\ncoloured according to 'bottlenecks' at that location\nfor a threshold cost of "+Max_Cost+".")
            plt.xlabel("Longitude")
            plt.ylabel("Latitude")
            plt.savefig("Figures/"+nodetype++str(Method)+str(Start_Times_Tuple[arrivltme_list.index(arrivltme)][:2])+'_'+str(Start_Times_Tuple[arrivltme_list.index(arrivltme)][3:5])+"_in_"+Places_text+"_bottlenecks.png")
            plt.close()
            f = open("Output Files/"+str(Places)+"/"+str(Places)+"_PopCosts/PopCost"+str(nodetype)+'_'+str(Method)+'_'+str(Start_Times_Tuple[arrivltme_list.index(arrivltme)][:2])+str(Start_Times_Tuple[arrivltme_list.index(arrivltme)][3:5])+'.txt')
            lines =f.readlines()
            f.close()
            n=0
            goodnodes,costy=[],[]
            goodnodesxcoords,goodnodesycoords=[],[]
            while n<8:
                cl = lines[0].split()
                m=1
                index =0 
                while m<len(lines):
                    if lines[m].split()[1]<cl[1]:
                        cl = lines[m].split()
                        index = m
                    m+=1
                del lines[index]
                goodnodes.append(cl[0])
                goodnodesxcoords.append(x[name.index(cl[0])])
                goodnodesycoords.append(y[name.index(cl[0])])
                costy.append(cl[1])
                n+=1
            plt.scatter(goodnodesxcoords,goodnodesycoords,c=costy,cmap=plt.get_cmap("magma"),norm=Normalize(vmin=4000,vmax=4500),edgecolors="gainsboro")
            plt.title(nodetype+" in "+Places_text+"\ncoloured according to jobs at that location,\nreccomended jobsites only.")
            plt.xlabel("Longitude")
            plt.ylabel("Latitude")
            plt.savefig("Figures/"+nodetype+str(Method)+str(Start_Times_Tuple[arrivltme_list.index(arrivltme)][:2])+'_'+str(Start_Times_Tuple[arrivltme_list.index(arrivltme)][3:5])+"_in_"+Places_text+"_reccomended_jobsites.png")
            plt.show()
