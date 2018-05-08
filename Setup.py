import openpyxl as opxl
####################################
####### Generic Functions ##########
def file_len(fname):              ##
    with open(fname) as f:        ##
        for i, l in enumerate(f): ##
            pass                  ##
    return i + 1                  ##
####################################
####### Files and other ############
conversion_file = "ExcelSheets/SCR_LSOA_Estimates.xlsx"
wb = opxl.load_workbook(conversion_file, read_only = True)
print('Performing first-time setup.')

print("Identifying numbers of LSOAs and MSOAs.")
LSOA_dictionary = {}
MSOA_dictionary = {}
places =wb.get_sheet_names()
for place in places:
    LSOA_dictionary[place]=(wb[place].max_row-5)
    n=1
    temp=[]
    while n<(wb[place].max_row-5):
        if wb[place]["C"+str(n+5)].value[:-1] in temp:
            pass
        else:
            temp.append(wb[place]["C"+str(n+5)].value[:-1])
        n+=1
    MSOA_dictionary[place]=int(len(temp))
    print(place,"complete")
f =open("Programme Files/LSOA_Dictionary.txt", "w")
f.write(str(LSOA_dictionary))
f.close()
f =open("Programme Files/MSOA_Dictionary.txt", "w")
f.write(str(MSOA_dictionary))
f.close()
print('LSOAs counted.')

    

print('Setup complete!')
