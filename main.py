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


def perform_encryption(filename):
    # Generate a new key
    key = Fernet.generate_key()

    # Write on file for decryption
    with open("key.txt", "w") as file_write:
        file_write.write(key.decode())
    print("Please Keep the 'key.txt' file secure as it is required for decryption")

    # Read entire data from csv in List of Dict
    with open(filename, "r") as file:
        myCSVReader = csv.reader(file, delimiter=",", quotechar='"')
        main_heading = spread_list(next(myCSVReader))  # first row is One, Two
        secondary_heading = spread_list(next(myCSVReader))  # second row is A, B, C
        outrows = []
        for row in myCSVReader:
            for index, item in enumerate(row):
                if item == "":
                    item = "-"
                found = False
                for outrow in outrows:
                    if outrow['main_heading'] == main_heading[index] and outrow['secondary_heading'] == \
                            secondary_heading[index]:
                        if outrow['data'] == None:
                            outrow['data'] = [item]
                        else:
                            outrow['data'].append(item)
                        found = True
                        break
                if not found:
                    outrow = {"main_heading": main_heading[index],
                              "secondary_heading": secondary_heading[index],
                              "data": [item]}
                    outrows.append(outrow)

        # Encrypt Data
        fernet = Fernet(key)
        for outrow in outrows:
            outrow['main_heading'] = fernet.encrypt(outrow['main_heading'].encode())
            outrow['secondary_heading'] = fernet.encrypt(outrow['secondary_heading'].encode())
            for i in range(len(outrow['data'])):
                outrow['data'][i] = fernet.encrypt(outrow['data'][i].encode())

        # Convert in Writable Format
        ROWS = []
        ROW = ""
        for entry in outrows:
            ROW += "," + entry['main_heading'].decode()
        ROWS.append(ROW[1:] + "\n")
        ROW = ""
        for entry in outrows:
            ROW += "," + entry['secondary_heading'].decode()
        ROWS.append(ROW[1:] + "\n")
        for j in range(len(outrows[0]['data'])):
            ROW = ""
            for entry in outrows:
                ROW += "," + entry['data'][j].decode()
            ROWS.append(ROW[1:] + "\n")

        # Write Data in file
        total = filename.split("_")
        if total[len(total) - 1].startswith("decrypted") or total[len(total) - 1].startswith("encrypted"):
            filename = "".join(total[:-1]) + "_encrypted.csv"
        else:
            filename = filename.split(".")[0] + "_encrypted.csv"

        with open(filename, "w") as file:
            for row in ROWS:
                file.write(row)
        print("Encrypted Successfully !")


def perform_decryption(filename):
    try:
        # Get Key for decryption from file
        with open("key.txt", "r") as file_read:
            key = file_read.read().encode()
    except:
        print("Please Paste the 'key.txt' file in current directory for decryption")
        return

    # Read entire data from csv in List of Dict
    with open(filename, "r") as file:
        myCSVReader = csv.reader(file, delimiter=",", quotechar='"')
        main_heading = spread_list(next(myCSVReader))  # first row is One, Two
        secondary_heading = spread_list(next(myCSVReader))  # second row is A, B, C
        outrows = []
        for row in myCSVReader:
            for index, item in enumerate(row):
                if item == "":
                    item = "-"
                found = False
                for outrow in outrows:
                    if outrow['main_heading'] == main_heading[index] and outrow['secondary_heading'] == \
                            secondary_heading[index]:
                        if outrow['data'] == None:
                            outrow['data'] = [item]
                        else:
                            outrow['data'].append(item)
                        found = True
                        break
                if not found:
                    outrow = {"main_heading": main_heading[index],
                              "secondary_heading": secondary_heading[index],
                              "data": [item]}
                    outrows.append(outrow)

        try:
            # Decrypt Data
            fernet = Fernet(key)
            for outrow in outrows:
                outrow['main_heading'] = fernet.decrypt(outrow['main_heading'].encode()).decode()
                outrow['secondary_heading'] = fernet.decrypt(outrow['secondary_heading'].encode()).decode()
                for i in range(len(outrow['data'])):
                    outrow['data'][i] = fernet.decrypt(outrow['data'][i].encode()).decode()
        except:
            print("Decryption Key Not Matches Encryption Key !!!")
            return

        # Convert in Writable Format
        ROWS = []
        ROW = ""
        for entry in outrows:
            ROW += "," + entry['main_heading']
        ROWS.append(ROW[1:] + "\n")
        ROW = ""
        for entry in outrows:
            ROW += "," + entry['secondary_heading']
        ROWS.append(ROW[1:] + "\n")
        for j in range(len(outrows[0]['data'])):
            ROW = ""
            for entry in outrows:
                ROW += "," + entry['data'][j]
            ROWS.append(ROW[1:] + "\n")

        # Write Data in file
        total = filename.split("_")
        if total[len(total) - 1].startswith("decrypted") or total[len(total) - 1].startswith("encrypted"):
            filename = "".join(total[:-1]) + "_decrypted.csv"
        else:
            filename = filename.split(".")[0] + "_decrypted.csv"

        with open(filename, "w") as file:
            for row in ROWS:
                file.write(row)
        print("Decrypted Successfully !")


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
