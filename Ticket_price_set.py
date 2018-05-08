from tabulate import tabulate
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
try:
    f=open("Programme Files/TicketCosts.txt")
    ticketdict=eval(f.readline())
    f.close()
    Ticket_Output = []
    print("To see a list of existing ticket names, type '#'.\nTo see the complete list of ticket names and prices, type '~'.\nTo exit this session type '*'")
    Coefficent_Name = input("Please give an appropriate name for this ticket.\nPlease note the names must be unique.\n")
    
    while True:
        if Coefficent_Name == '#':
            print("Currently saved settings are ")
            for element in ticketdict.keys():
                  print(str(element)+", ", end="")
            Coefficent_Name = input("\n\nPlease give another input, or '*' to exit.\n")
            continue
        
        if Coefficent_Name == '~':
            print(tabulate(ticketdict.items(), headers=["Ticket","Price"], tablefmt="rst"))
            Coefficent_Name = input("\n\nPlease give another input, or '*' to exit.\n")
            continue
        if Coefficent_Name in ticketdict.keys():
            print('That name is already taken!\n Update? (y)')
            test = input()
            if test == 'y':
                pass
            else:
                Coefficent_Name = input("\nPlease give another input, or '*' to exit.\n")
            continue
        if Coefficent_Name == '*':
            print('Exiting..')
            break
        else:
            val=input("Add cost:\n")
               
            if is_number(val):    
                test=input('Are you sure you wish to add '+str(Coefficent_Name)+"= £"+str(val)+" ? y/n\n")
            if test =='y':
                ticketdict[Coefficent_Name]=val
            Coefficent_Name = input("\n\nPlease give another input, or '*' to exit.\n")
            continue
finally:
    f=open("Programme Files/TicketCosts.txt","w")
    f.write(str(ticketdict))
    f.close()
    print("Files saved.")
