from cryptography.fernet import Fernet
import csv


def spread_list(inlist):
    """
    Function to spread list values left to right.
    Used to deal with implicit multiple headers pf multi Index csv.
    ["","value1","","","value2",""] ==> ["","value1","value1","value1","value2","value2"]
    """
    outlist = []
    curr = ""
    for item in inlist:
        if item:
            curr = item
        outlist.append(curr)
    return outlist




def menu():
    # TODO: Check if CSV is multi index or not
    entry = input("1. Encrypt CSV\n2. Decrypt CSV\n3. Exit\n => ")
    entry_int = 0
    try:
        entry_int = int(entry)
    except:
        print("Enter Real Numbers Only !!!")
        menu()
    if entry_int == 1:
        filename = input("Enter File Name to Encrypt (with .csv at end)\n => ")
        perform_encryption(filename)
    elif entry_int == 2:
        filename = input("Enter File Name to Decrypt (with .csv at end)\n => ")
        perform_decryption(filename)
    elif entry_int == 3:
        quit()
    menu()








menu()
quit()



'''
data = "one,,,two,,,\na,b,c,a,b,c\n1.0,1.1,1.2,1.3,1.4,1.5\n2.0,2.1,2.2,2.3,2.4,2.5\n3.0,3.1,3.2,3.3,3.4,3.5\n4.0,4.1,4.2,4.3,4.4,4.5\n5.0,5.1,5.2,5.3,5.4,5.5"
with open("test.csv", "w") as file:
    file.write(data)
quit()
'''
