'''
Game Shop Kiosk System (Inventory And Membership Management)

BY:
    SaurSum8

CLASS: 12
'''

import mysql.connector as sql
import sys
import random
import datetime

#Initialization
print("Attempting Connection To SQL Server...")

db = sql.connect(host="localhost",
                 user="root",
                 passwd="",
                 charset="utf8") #Connect To SQL

cursor = db.cursor() #Create SQL Cursor

print("SQL Server Connection Successful!\n")

#Database
try:
    print("Checking For Database....")
    cursor.execute("CREATE DATABASE ShopDatabase") #Run SQL Cmd To Make Database
    print("No Database Found, New Database Created!")
    
except:
    print("Database Found!") #If It Already Exists, Use It

print("Attempting Connection To Database...")
cursor.execute("USE ShopDatabase") #Use Database
print("Connection Successful!\n")

#Create/Check For Tables
#Inventory
try:
    print("Checking For Inventory Table...")
    cursor.execute("CREATE TABLE Inventory (ID INT PRIMARY KEY, Name VARCHAR(50), Category VARCHAR(50), Age_Rating INT, Release_Date DATE, Price INT, Stock INT)") #Make Inventory Table
    print("No Inventory Table Found, New Inventory Table Created!")

except:
    print("Inventory Table Found!")

#Membership
try:
    print("Checking For Membership Table...")
    cursor.execute("CREATE TABLE Membership (ID INT PRIMARY KEY, Name VARCHAR(50), Phone_No INT, Points INT)") #Make Membership Table
    print("No Membership Table Found, New Membership Table Created!")

except:
    print("Membership Table Found!")

print("\nKiosk Is Now Ready To Serve!\n")


#User Interface

#Greets Customer
def greet():
    print("*" * 15 ,"WELCOME TO GAME SHOP KIOSK SYSTEM", "*" * 15)


#Handles Choice Inputs
def inputChoiceHandler(lBound, uBound, message = "\nEnter Your Choice: "):
    
    while(True):
        try:
            inp = int(input(message))

            if(inp < lBound or inp > uBound):
                raise Exception()

            return inp

        except:
            print("ERROR: Invalid Input! Please enter values in range [", lBound, ",", uBound, "]")


#Handle Checkout
memID = 0
pt = 0

def checkout(idV, quan):
    print()
    print("#"*60)
    print("\nPlease Get Your Method Of Payment Ready!")
    print("An Employee Will Arrive At This Kiosk With Your Purchase Shortly :)")
    print("\n--- After Payment, Please Confirm Completion Of Purchase Below! ---")

    global pt
    global memID
    
    while(True):
        comp = input("\nWas The Purchase Successful? (Y/N): ")
        
        if(comp.upper() == 'Y'):

            cmd = "UPDATE Inventory SET Stock = " + str(quan) + " WHERE ID = " + str(idV)
            cursor.execute(cmd)

            if(memID != 0):
                cmd = "UPDATE Membership SET Points = " + str(pt) + " WHERE ID = " + str(memID)
                cursor.execute(cmd)

            pt = 0
            memID = 0
            
            db.commit()
            
            print("\nThank You For Shopping At Game Store! :D")
            print("Enjoy Your Purchase! <3")
            print("Preparing Kiosk For Next Customer And Returning To Main Menu... \n\n")
            greet()
            break
        
        elif(comp.upper() == 'N'):

            pt = 0
            memID = 0

            print("\nWe Are Sorry For The Unsuccessful Purchase! :(")
            print("We Wish You Have A Better Experience Next Time <3")
            print("Preparing Kiosk For Next Customer And Returning To Main Menu... \n\n")
            greet()
            break

        else:
            print("Invalid Input!")


#Membership Registration
def memRegister():
    try:
        nam = input("Please Enter Your Name: ")
        phon = int(input("Enter Your Phone No: "))
        genK = random.randrange(1000, 1000000)

        cursor.execute("INSERT INTO Membership (ID, Name, Phone_No, Points) VALUES ({}, '{}', {}, {})".format(genK, nam, phon, 0))

        print("\nYou Have Been Successfully Enrolled In Our Membership Program!")
        print("Please Note Down Your Unique ID: \n")
        print(genK)
        
        input("\nPress Enter To Proceed Back To Membership Menu...")

        db.commit()
        
    except:
        print("\nSomething Went Wrong! Please Try Again...")


#Check For Membership
def memCheck(purchase = True, cost = 0):

    while(True):
        inp = input("\n>> Are You Part Of Our Membership Program? (Y/N): ")
        
        if(inp.upper() == 'Y'):
            idV = input("\nPlease Enter Your Unique ID (Or 'N' To Go Back): ")

            if(idV.upper() != 'N'):
                cursor.execute("SELECT ID FROM Membership")

                try:
                    idV = int(idV)
                except:
                    print("Error! Try Again!")
                    cursor.fetchall() #Reads All, To Reset Cursor
                    continue
                
                for i in cursor:

                    if(i[0] == int(idV)):

                        cmd = "SELECT Points FROM Membership WHERE ID = " + str(idV)
                        cursor.fetchall() #Reads All, To Reset Cursor
                        cursor.execute(cmd)

                        pnt = cursor.fetchone()[0]
                        print("\nYou Have", pnt, "Points!")
                        
                        if(purchase):
                            
                            d = inputChoiceHandler(0, min(pnt, cost), "Enter No. Of Points To Use (0 If None): ")
                            
                            print("\nYou Will Be Awarded", int((cost - d) * 0.15), "Points, After Purchase!")
                            print("\n### Final Price To Pay:", cost - d, "###")

                            global pt
                            global memID
                            
                            memID = idV
                            pt = pnt + int((cost - d) * 0.15) - d
                            
                        input("\nPress Enter To Continue...")
                        break
                    
                else:
                    print("Not Found!")

                break
                
        elif(inp.upper() == 'N'):
            ask = input("Would You Like To Register? (Y/N): ")

            if(ask.upper() == 'Y'):
                memRegister()
                
            elif(ask.upper() == 'N'):
                break
                
            else:
                print("Invalid Option!")
            
        else:
            print("Invalid Option!")


#Age Verification
def ageCheck(idV):
    cmd = "SELECT Age_Rating FROM Inventory WHERE ID = " + str(idV)
    cursor.execute(cmd)
    minAge = cursor.fetchone()[0]
    while(True):
        try:
            x = int(input("Please Enter Your Year Of Birth: "))
            y = str(datetime.date.today())[:4]
            
            age = int(y) - x

            if(age < minAge):
                return False

            print("Age Verification Complete!")
            return True
            
        except:
            print("Invalid Input! Please Try Again!")


idS = []

#Present Products
def present(extra = ""):

    #Print Out Inventory Table In Presentable Format:

    cmd = "DESCRIBE Inventory"
    
    cursor.execute(cmd)
    desc = []
    for i in cursor:
        desc.append(i[0].replace("_", " "))

    cmd = "SELECT * FROM Inventory" + extra
    
    cursor.execute(cmd)
    size = 0

    print("\n", "=" * 30)

    global idS
    idS = []
        
    for i in cursor:
        size += 1
        for j in range(len(i)):
            if(j == 0):
                print(desc[j], ":", i[j])
                idS.append(i[j])
            else:
                print("\t", desc[j], ":", i[j])
        print("\n", "=" * 30)
            
    print()

#Purchase Menu
def purchaser():

    global idS
    newCall = False
    
    while(True):
        print("\n", "$" * 4, "What Would You Like To Purchase?", "$" * 4)

        #Print Out Inventory Table In Presentable Format:
        if(not newCall):
            present()

        newCall = False

        #User Inputs And Forward
        while(True):
            try:
                print("\nSpecial Commands: \n(Enter -1 To Return To Menu OR Enter -2 To Search By Category)")
                idV = int(input("\nEnter ID Of Product To Buy: "))

                if(idV not in idS and idV != -1 and idV != -2):
                    raise Exception()

                #SEARCH BY CATEGORY
                elif(idV == -2):
                    liCat = []
                    cursor.execute("SELECT Category FROM Inventory")
                    for i in cursor:
                        if(i[0] not in liCat):
                            liCat.append(i[0])
                        
                    if(len(liCat) != 0):
                        z = 0
                        print("\nCategories:")
                        for i in liCat:
                            z += 1
                            print("Option ", z, ")" , i)

                        inpC = inputChoiceHandler(1, z + 1, f"\nChoose Category Number (Enter {z + 1} For All Categories): ")

                        if(inpC == z + 1):
                            break
                        
                        cmdC = " WHERE Category = '" + str(liCat[inpC - 1] + "'")

                        present(cmdC)
                        newCall = True

                    else:
                        print("Error!")
                    
                break
            
            except:
                print("Invalid Input! Try Again!")

        if(idV == -1):
            break
        
        elif(idV == -2):
            continue
            
        if(not ageCheck(idV)):
            print("\nSorry, You Do Not Meet The Age Requirements For This Product!")
            print("Please Pick Something Else!")
            input("Press Enter To Continue...")
            continue
        
        cmd = "SELECT STOCK FROM Inventory WHERE ID = " + str(idV)
        cursor.execute(cmd)

        inStock = True
        q = 1
        
        i = cursor.fetchone()[0]

        if(i <= 0):
            print("\nSorry! We Are Out Of Stock For That Product!")
            print("Please Pick Something Else!")
            inStock = False
            
        else:
            q = inputChoiceHandler(1, i, f"\nEnter Quantity: ")

        if(not inStock):
            continue
        
        #Confirm Order
        cmd = "SELECT Name FROM Inventory WHERE ID = " + str(idV)
        cursor.execute(cmd)
        
        print("\n", "#"*8, "CONFIRMATION", "#"*8)
        print("You Are Purchasing:")
        
        n = cursor.fetchone()[0]
        print("\n\t", q, "x", n)

        cmd = "SELECT Price FROM Inventory WHERE ID = " + str(idV)
        cursor.execute(cmd)
            
        p = cursor.fetchone()[0]
        print("\t", "Current Price:", q, "x", p, "=", q * p)

        check = input("\nProceed? (Y/N): ")
        
        if(check.upper() == 'Y'):
            memCheck(cost = q * p)
            checkout(idV, i - q)
            break

        else:
            print("Returning Back To Purchase Menu...")


#ADMIN Functions:

#Prints Either Inventory Or Membership Table Based On Call Paramemter
def tablePrint(x):
    if(x == 1):
        cursor.execute("DESCRIBE Inventory")
        print("\nFormat: ")
        for i in cursor:
            print("[", i[0], end=" ] ")

        cursor.execute("SELECT * FROM Inventory")
        print("\nContents: \n")
        for i in cursor:
            print(i)
    else:
        cursor.execute("DESCRIBE Membership")
        print("\nFormat: ")
        for i in cursor:
            print("[", i[0], end=" ] ")

        cursor.execute("SELECT * FROM Membership")
        print("\nContents: \n")
        for i in cursor:
            print(i)

    input("\nPress Enter To Continue...")


#Inserts Record Into Inventory/Membership Based On Given Parameter(s)
def insert(x):
    if(x == 1):
        try:
            idV = int(input("Enter Unique ID: "))
            nameV = input("Enter Name: ")
            catV = input("Enter Category: ")
            ageV = int(input("Enter Minimum Permitted Age: "))
            dateV = input("Enter Release Date (YYYY-MM-DD): ")
            priceV = int(input("Enter Price: "))
            stockV = int(input("Enter Stock: "))
            
            cursor.execute("INSERT INTO Inventory (ID, Name, Category, Age_Rating, Release_Date, Price, Stock) VALUES ({}, '{}', '{}', {}, '{}', {}, {})".format(idV, nameV, catV, ageV, dateV, priceV, stockV))
            db.commit()
            print("\nSuccess!")
        except:
            print("\nThere Was An Error! Please ensure the ID is unique and all values are inputted in correct format!")

    else:
        try:
            idV = int(input("Enter Unique ID: "))
            nameV = input("Enter Name: ")
            phV = int(input("Enter Phone_No: "))
            ptV = int(input("Enter Points: "))
            
            cursor.execute("INSERT INTO Membership (ID, Name, Phone_No, Points) VALUES ({}, '{}', {}, {})".format(idV, nameV, phV, ptV))
            db.commit()
            print("\nSuccess!")
        except:
            print("\nThere Was An Error! Please ensure the ID is unique and all values are inputted in correct format!")

    input("\nPress Enter To Continue...")


#Deletes A Record
def delete(x):
    c = 'y'
    while(c.upper() == 'Y'):
        tablePrint(x)
        
        cmd = "Membership"
        if(x == 1):
            cmd = "Inventory"

        inp = input("\nEnter ID Of Record To Delete (Enter E To Return To Admin Menu): ")

        if(inp.upper() == 'E'):
            break
        
        try:
            cursor.execute("DELETE FROM " + cmd + " WHERE ID = " + inp)
            db.commit()
            print("Success!")
        except:
            print("There Was An Error!")

        c = input("Delete More? (y): ")
            


#Updates An Element Of Record From Inventory/Membership Table
def update(x):
    c = "y"
    while(c.upper() == "Y"):
        tablePrint(x)
        table = "Membership"
        if(x == 1):
            table = "Inventory"

        cmd = "DESCRIBE " + table
        cursor.execute(cmd)
        
        print("\nChoose What To Update: ")
        q = 1
        li = []
        for i in cursor:
            print("(Option ", q, ") [", i[0], "]")
            li.append(str(i[0]))
            q+=1

        print("(Option ", q, ") Back To Admin Menu")
        
        inp = inputChoiceHandler(1,q)
        if(inp == q):
            break
        
        idV = input("Enter Current ID of Object: ")
        up = input("Enter Updated Value (If String Surround With ''): ")
        cmd = "UPDATE " + table + " SET " + li[inp - 1] + " = " + up + " WHERE ID = " + idV
        print()
        
        try:
            cursor.execute(cmd)
            db.commit()
            print("Success!")
        except:
            print("There was an Error! (Ensure Strings Are Surrounded By ' ') ")

        c = input("Update more? (y): ")
        print()


#Admin Control Menu
def adminPanel():
    p = input("\nEnter Admin Password: ")

    if(p != "abc"):
        print("Incorrect Password!")
    
    while(p == "abc"):
        print("\n", "%"*4, "Admin Panel", "%"*4)

        print("\n", "1. Print Inventory Table")
        print(" 2. Print Membership Table\n")
        print(" 3. Reset Inventory")
        print(" 4. Reset Membership\n")
        print(" 5. Insert Into Inventory Table")
        print(" 6. Delete From Inventory Table\n")
        print(" 7. Insert Into Membership Table")
        print(" 8. Delete From Membership Table\n")
        print(" 9. Update Inventory Table")
        print(" 10. Update Membership Table\n")
        print(" 11. Close Kiosk")
        print(" 12. Back To Main Menu")
        
        inp = inputChoiceHandler(1, 12)

        if(inp == 12):
            print()
            greet()
            break
        
        elif(inp == 11):
            print()
            sys.exit("This Kiosk Has Been Closed By An Adminstrator!")

        elif(inp == 10):
            update(0)
            
        elif(inp == 9):
            update(1)
        
        elif(inp == 8):
            delete(0)
            
        elif(inp == 7):
            insert(0)
            
        elif(inp == 6):
            delete(1)
            
        elif(inp == 5):
            insert(1)
        
        elif(inp == 4):
            it = input("Are you sure you want to delete all records? (y/n): ")
            if(it == 'y'):
                cursor.execute("TRUNCATE TABLE Membership")
                db.commit()
                print("All records of Membership have been deleted!")
                
        
        elif(inp == 3):
            it = input("Are you sure you want to delete all records? (y/n): ")
            if(it == 'y'):
                cursor.execute("TRUNCATE TABLE Inventory")
                db.commit()
                print("All records of Inventory have been deleted!")
            
        elif(inp == 2):
            tablePrint(0)
                
        elif(inp == 1):
            tablePrint(1)


#Main Menu
def menu():
    while(True):
        print("\n", "-" * 5, "Main Menu", "-" * 5)
        print("\n", "1. Purchase Items")
        print(" 2. Register/Check Membership Program")
        print(" 3. Admin Control")
        
        inp = inputChoiceHandler(1, 3)

        if(inp == 1):
            purchaser()
        elif(inp == 2):
            memCheck(False)
        elif(inp == 3):
            adminPanel()
    

greet() #Greet
menu() #Start The Menu
