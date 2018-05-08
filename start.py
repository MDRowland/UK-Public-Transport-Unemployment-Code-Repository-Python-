import re
from tabulate import tabulate
nodetypes = ['LSOA','MSOA']
import socket
def check_internet():
    for timeout in [1,5,10]:
        try:
            socket.setdefaulttimeout(timeout)
            host = socket.gethostbyname("www.google.com")
            s = socket.create_connection((host, 80), 2)
            s.close()
            return True
        except Exception:
            pass
    return False


#try:
f = open("Programme Files/LSOA_dictionary.txt")
LSOA_dictionary = eval((f.readline()))
f.close()
f = open("Programme Files/MSOA_dictionary.txt")
MSOA_dictionary = eval((f.readline()))
f.close()
Places=[]
#################################
###LSOA/MSOA Retrival section####
#################################
print("## Census Geography ##")

print("Type the name of the authorities you would like to consider. \n"+"To stop adding enter 'done'.\n")
plcename = input()

while True:
    if plcename in LSOA_dictionary:
        Places.append(plcename)
        plcename=input("Give another input:\n")         #USER INPUT SECTION
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
print(Places)
while True:
    print("Type the name of the census level you would like to consider. \nValid types are LSOA or MSOA.") 
    nodetype = input()
    if nodetype in nodetypes:
        break
    else:
        print('Invalid type')
        pass
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

#USER INPUT ENDS

print("\n\n\n\n\n\n#####################################################\n\n\n\n\n\n")
for placename in Places:
    exec(open("DataExtractorFinal.py").read())
### Arrival time- arrival at destination determined as on the coming monday (from current date as of script being intiated) ###
print("\n\n\n\n\n\n#####################################################\n\n\n\n\n\n")
######      Checking internet connection exists at current time     #########
test = check_internet()
if test == True:
    pass
else:
    print('Python cannot currently access the internet. This could be caused by a multitude of isssues: the most likely being a poor connection.\nUnfortunately, this means that the next stage of the process is not possible at this time. Should you wish to try again later, the node data should be saved to file.')
    quit()
#####
  
   
#try:#
exec(open("FinalArcfinder.py").read())
#except:
#    print("an exception has occured")
#    
#    pass
Nodes=[]
for placename in Places:         #Takes all the considered places and puts the nodes in this list
    node_loc=str("Locality Files/"+str(placename)+'_Nodes/'+str(nodetype)+'s.txt')
    node_number = file_len(node_loc)
    f = open(node_loc, "r")
    line = f.readlines()
    
    for n in range(node_number):
        Nodes.append(line[n].split())    
print("\n\n\n\n\n\n#####################################################\n\n\n\n\n\n")           


for arrivltme in arrivltme_list: 
        for Method in Transport_Mode:
            exec(open("djikstra_test.py").read())

for arrivltme in arrivltme_list: 
        for Method in Transport_Mode:
            exec(open("PopulationCostfinder.py").read())

for arrivltme in arrivltme_list: 
        for Method in Transport_Mode:
            exec(open("Unreachable_Nodes.py").read())
for arrivltme in arrivltme_list: 
        for Method in Transport_Mode:
            exec(open("Bottleneck_check.py").read())               
