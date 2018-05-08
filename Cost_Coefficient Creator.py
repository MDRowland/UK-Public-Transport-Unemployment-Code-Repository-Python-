from tabulate import tabulate
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
try:
    f=open("Programme Files/CostCoefficients.txt")
    coeffdict=eval(f.readline())
    f.close()
    g=open("Programme Files/CostCoefficients_MetaData.txt")
    meta= g.readline().split()
    g.close()
    Coefficent_Output = []
    print("To see a list of existing coefficent names, type '#'.\nTo see the complete list of coefficent names and values, type '~'.\nTo exit this session type '*'")
    Coefficent_Name = input("Please give an appropriate name for this coeffiecent set.\nPlease note the names must be unique.\n")
    
    while True:
        if Coefficent_Name == '#':
            print("Currently saved settings are ")
            for element in coeffdict.keys():
                  print(str(element)+", ", end="")
            Coefficent_Name = input("\n\nPlease give another input, or '*' to exit.\n")
            continue
        
        if Coefficent_Name == '~':
            print(tabulate(coeffdict.items(), headers=["Name","Coefficents"], tablefmt="rst"))
            print("\nCoefficents are in order: ")
            for element in meta:
                if (element !="Name"):print(element, end=" ")
            Coefficent_Name = input("\n\nPlease give another input, or '*' to exit.\n")
            continue
        if Coefficent_Name in coeffdict.keys():
            print('That name is already taken!\n')
            print(str(Coefficent_Name)+": "+str(coeffdict[Coefficent_Name]))
            Coefficent_Name = input("\nPlease give another input, or '*' to exit.\n")
            continue
        if Coefficent_Name == '*':
            print('Exiting..')
            break
        else:
            values=[]
            x=1
            while x<=len(meta)-1:
                val=input("Add value for "+str(meta[x])+":\n")
               
                if is_number(val):
                    values.append(eval(val))
                    x+=1
                else:
                    print('This is an invalid value type.')
            if sum(values) == 0:
                print('Cannot have zero for all values. Please start again.')
                Coefficent_Name = input("\n\nPlease give another input, or '*' to exit.\n")
                continue
            test=input('Are you sure you wish to add '+str(Coefficent_Name)+": "+str(values)+" ? y/n\n")
            if test =='y':
                coeffdict[Coefficent_Name]=values
            Coefficent_Name = input("\n\nPlease give another input, or '*' to exit.\n")
            continue
finally:
    f=open("Programme Files/CostCoefficients.txt","w")
    f.write(str(coeffdict))
    f.close()
    print("Files saved.")
    
