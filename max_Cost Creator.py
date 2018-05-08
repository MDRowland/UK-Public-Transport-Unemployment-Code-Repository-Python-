from tabulate import tabulate
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
try:
    f=open("Programme Files/MaxCost.txt")
    maxcostdict=eval(f.readline())
    f.close()
    Ticket_Output = []
    print("To see a list of existing max cost names, type '#'.\nTo see the complete list of max costs and names, type '~'.\nTo exit this session type '*'")
    Coefficent_Name = input("Please give an appropriate name for this max cost.\nPlease note the names must be unique.\n")
    
    while True:
        if Coefficent_Name == '#':
            print("Currently saved settings are ")
            for element in maxcostdict.keys():
                  print(str(element)+", ", end="")
            Coefficent_Name = input("\n\nPlease give another input, or '*' to exit.\n")
            continue
        
        if Coefficent_Name == '~':
            print(tabulate(maxcostdict.items(), headers=["Ticket","Max Cost"], tablefmt="rst"))
            Coefficent_Name = input("\n\nPlease give another input, or '*' to exit.\n")
            continue
        if Coefficent_Name in maxcostdict.keys():
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
                test=input('Are you sure you wish to add '+str(Coefficent_Name)+"= "+str(val)+" ? y/n\n")
            if test =='y':
                maxcostdict[Coefficent_Name]=val
            Coefficent_Name = input("\n\nPlease give another input, or '*' to exit.\n")
            continue
finally:
    f=open("Programme Files/MaxCost.txt","w")
    f.write(str(maxcostdict))
    f.close()
    print("Files saved.")

