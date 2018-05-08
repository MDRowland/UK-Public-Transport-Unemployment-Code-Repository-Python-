import googlemaps
from googlemaps import Client
import time,sys,datetime,os,re

def file_len(fname):
    i=-1
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

thresholds= [1,5,10,20,25,30,40,50,60,70,75,80,90,95,99,100] #Threshold percentage values
Nodes =[]
for placename in Places:         #Takes all the considered places and puts the nodes in this list
    node_loc=str("Locality Files/"+str(placename)+'_Nodes/'+str(nodetype)+'s.txt')
    node_number = file_len(node_loc)
    f = open(node_loc, "r")
    line = f.readlines()
    for n in range(node_number):
        Nodes.append(line[n].split())
    f.close()   
        
node_number = len(Nodes) #Number of nodes under consideration

arrivltme_list=[]
now = datetime.datetime.now()
for start in Start_Times_Tuple:
    startday=now+datetime.timedelta(days=((8-int(now.strftime("%w"))%7)))
    arrivltme_list.append(time.mktime(time.struct_time((int(startday.year),int(startday.month),int(startday.day),int(start[:2]),int(start[3:5]),0,0,int(startday.strftime("%j")),-1))))


print('\nStarting...')
### Aquires the value of api key from a saved file, determining if it can be used (If 24 hours have certaintly passed since last use) ###
api_keys = ["AIzaSyC8eZSE47velxVNPDX8rPaTwYsHCgDAEMw","AIzaSyDtmU9F-g3J9W7lqm3FLA8B8ywP1nnZYwU","AIzaSyAFjWSIDUmQoNG9m_UualK_O2R-tRHbbcQ","AIzaSyDsvsI2q1WsZzeWRBPnENKdhYYt6P5YPZY","AIzaSyDKQDnygFy1Tn5VyDvW12Ic5qfoiG2iW6g","AIzaSyBwnvW1RbOZ6QO4OuS1Z6Lug8AIcDl7ttI","AIzaSyBN_VCujwDnJHr3h0GuLleOvW2XGo-QALQ","AIzaSyAuIMKGuBULNHlNXfgEeeyfr39UcUq3dV0","AIzaSyAEZ_qhPSZz0vzFoEcY0jB65SXTERek3cs","AIzaSyASo8s2NW12eynofqEQ95y3u94DJbUB0gs","AIzaSyD5JyGeQZsHxljjUXz1Bp-M1RxA37L6X3E","AIzaSyBKk9ee5R3_Sr0b8DpXzwP1affX2XjmaCo"]
#

zvalue=open("Programme Files/z.txt","r")
zline = zvalue.readlines()[0].split()
ztime=zline[1]
if (float(ztime)+86400)>time.time():
    z = int(zline[0])
    if z==len(api_keys):
        print('Run out of API access!\nAllow at least 24 hours, or extend. See Readme for details.')
        quit()
else:
    z=0
zvalue.close()
Key_Use_Number = 0
###
n = 0
try:
    
    for arrivltme in arrivltme_list: #Allows multiple Shift times to be considered
        for Method in Transport_Mode:
            print('Transport Mode '+str(Method)+' at '+str(Start_Times_Tuple[arrivltme_list.index(arrivltme)])+' arrival starting.')
            
            arcpath="Output Files/"+str(Places)+"/"+str(Places)+'_Arcs/Arcs_'+str(nodetype)+'_'+str(Method)+'_'+str(Start_Times_Tuple[arrivltme_list.index(arrivltme)][:2])+str(Start_Times_Tuple[arrivltme_list.index(arrivltme)][3:5])+'.txt'
            if os.path.exists("Output Files/"+str(Places)+"/"+str(Places)+"_Arcs"):
                pass
            else:
                os.makedirs("Output Files/"+str(Places)+"/"+str(Places)+"_Arcs")
            if os.path.exists(arcpath) and (int(node_number*(node_number-1)/2))==file_len(arcpath):  #tests to see if the file already exists, if it does and is correct will skip this.
                print('Arc data for '+str(Method)+' at '+str(Start_Times_Tuple[arrivltme_list.index(arrivltme)])+' already exists!')
                continue
            g = open(arcpath,"w")
            
            while z<len(api_keys):
                gmaps = Client(api_keys[z])
                n = 0
                while n < (node_number):
                    pnuc = Nodes[n]
                    l = (n + 1)
                    while l < node_number:
                        snuc = Nodes[l]
                        start_coords = str(str(pnuc[3])+" "+str(pnuc[4]))
                        end_coords = str(str(snuc[3])+" "+str(snuc[4]))
                        maps_output = gmaps.directions(start_coords, end_coords, mode=Method, arrival_time = arrivltme)
                        if maps_output ==[]:
                            #No route between locations-gotta walk it but google doesn't do this intelligently for some reason
                            maps_output = gmaps.directions(start_coords, end_coords, mode='walking', arrival_time = arrivltme)
                            #Should proceed as normal after here: if the arc is so long it is unwalkable the algorith will discount it anyway
                        timetaken = maps_output[0]['legs'][0]['duration']['value']
                        tot_dist_traveled = maps_output[0]['legs'][0]['distance']['value']
                        transport_boardings = 0
                        walking_distance=int(tot_dist_traveled)
                        walking_time=int(timetaken)
                        
                        if Method == 'transit':
                            for element in maps_output[0]['legs'][0]['steps']:
                                if element['travel_mode']=='TRANSIT':
                                    transport_boardings+=1
                                    walking_distance-=int(element['distance']['value'])
                                    walking_time-=int(element['duration']['value'])       
                        else:   #If you aren't using PubTrans this is an irrelevant metric 
                            walking_distance=0
                            walking_time=0
                        
                        
                        g.write(str(pnuc[0])+str(snuc[0])+" "+str(pnuc[0])+" "+str(snuc[0])+" "+str(timetaken)+" "+str(tot_dist_traveled)+" "+str(transport_boardings)+" "+str(walking_time)+" "+str(walking_distance)+" "+'1\n')
                        l+=1
                        Key_Use_Number+=1
                        if Key_Use_Number>2450:
                            z+=1
                            if z>=len(api_keys):
                                print("Run out of API access!")
                            gmaps = Client(api_keys[z])
                            Key_Use_Number=0
                    if round((n/node_number)*100)in thresholds:
                        if round((n/node_number)*100) != round(((n-1)/node_number)*100):
                            print("    "+str("{:5.2f}".format(round((n/node_number)*100,2)))+"% Complete") # Prints out progress percentage for benifit of user

                    n+=1
                print('Transport mode '+str(Method)+' Complete!\n')
                g.close()
                break
            if z>=len(api_keys):
                print('Run out of API access!\nAllow at least 24 hours, or extend. See Readme for details.')
                g.close()
                zvalue=open("Programme Files/z.txt","w")
                zvalue.write(str(z)+' '+str(time.time()))   
                zvalue.close()
                quit()
    
except(googlemaps.exceptions.Timeout):
    print('The API has timed-out.')
    pass
except(googlemaps.exceptions.ApiError):
    print('Some unspecified error. Likely API key has not been activated correctly.\nVisit https://console.developers.google.com/apis/api/directions_backend?project=_ for activation, and consult the Readme for further help.')
    pass         
finally:
    print('Saving files.')
    if Key_Use_Number !=0:
        with open("Programme Files/z.txt","w") as  zvalue:
            zvalue.write(str(z+1)+' '+str(time.time()))
        zvalue.closed
    f.close()    
    

