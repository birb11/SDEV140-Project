"""
Program: project.py
Author: Daven Kim
Date: 12/12/2023

This program records user names and respective account balances and displays them.
The program uses a .csv file to record accounts and balances and to search users.
It also allows users to withdraw and deposit to their account or close an account.
"""
#Importing the necessary classes
from breezypythongui import EasyFrame
import csv
from tempfile import NamedTemporaryFile
import shutil
from tkinter import PhotoImage


#Main startup GUI, has an image, a label, an entry field, and 3 buttons.
class window(EasyFrame):
    #Instantiating the window class
    def __init__(self):
        #Calling parent class instantiation method
        EasyFrame.__init__(self, title = "DK Banking App")
        #Setting background image, self.cash represents imported image, self.background instantiates the label the image will be displayed in
        self.cash = PhotoImage(file = 'cash.gif')
        self.background = self.addLabel(text = '', row = 0, column = 0, rowspan = 2, columnspan = 3)
        #Setting the label image to the imported cash photo
        self.background["image"] = self.cash

        self.addLabel(text = "Enter Name:", row = 0, column = 0) #Display text for entry field
        self.searchInput = self.addTextField(text = "", row = 0, column = 1) #Instantiate text field
        self.search = self.addButton(text = "Search", row = 1, column = 0, command = self.searchAccount) #Instantiate button to search for inputted text using searchAccount
        self.add = self.addButton(text = "New Account", row = 1, column = 1, command = self.addAccount) #Instantiate button to add an account via addAccount
        self.exit = self.addButton(text = "Quit", row = 1, column = 2, command = self.byebye) #Instantiate button to exit program using byebye

    #Defining searchAccount method
    def searchAccount(self):
        #temp is the input from the entry field
        temp = self.searchInput.getText()
        #try-except may not be necessary here, checks for ValueError
        try: 
            with open("data.csv", 'r') as csvfile: #open the data.csv file in read mode
                accountreader = csv.DictReader(csvfile) #accountreader imports rows of dictionary entries
                found = False #value for locating the name in dictionary or not
                for row in accountreader: #checking each row for user
                    print(row)
                    check = row["name"] #check is temporary value for name in the dictionary
                    if check.lower() == temp.lower(): #compares name values without being case sensitive
                        found = True #set found to true if name matches
                        funds = row["balance"] #set funds to value of account when name matches
                        person = row["name"] #set person to name as appears in dictionary
                csvfile.close() #closing file when finished
            if found == False: #check for no name matches
                self.messageBox(title = "ERROR", message = "Input existing user") #output when user is not found
            else: #executes when name matches
                show = display() #creates new window with account details
                show.nameField["text"] = person #set the name field in new window to user
                show.fundField["text"] = funds #set account value field in new window

 
        except ValueError: #check for ValueError
            self.messageBox(title = "ERROR", message = "Input existing user") #output when ValueError occurs

    #defining addAccount method used to add account entries to dictionary data file
    def addAccount(self): 
        name = self.prompterBox(title = "Add Account", promptString = "Enter full name:") #name is the returned value entered by user in prompt box
        money = self.prompterBox(title = "Account balance", promptString = "Add account balance:") #money is the returned value entered by user in prompt box

        #try except clause when user enters a nonnumeric value in account balance prompt box
        try:
            float(money) #performs a check to make sure money is numeric value
            with open("data.csv", 'r') as csvfile: #open data.csv file to check if entered name exists already
                fieldNames = ['name', 'balance'] #defines fieldNames for following command
                accountreader = csv.DictReader(csvfile, fieldnames = fieldNames) #accountreader is row of dictionary entries retrieved from csv file
                for row in accountreader: #checking each dictionary entry by row
                    if row['name'].lower() == name.lower(): #check to see if name is already inputted into system, not case sensitive
                        self.messageBox(title = "ERROR", message = "User already exists.") #return message if user already exists in csv file
                        csvfile.close() #closes csv file when match is discovered
                        return #ends method since account is not added because user exists already
                csvfile.close() #close csv file after no matches discovered
            with open("data.csv", 'a') as csvfile: #open csv file again in append mode
                fieldNames = ["name", "balance"] #defining fieldNames for dictionary entries
                accountwriter = csv.DictWriter(csvfile, fieldnames = fieldNames) #accountwriter adds entries to csv file
                accountwriter.writerow({"name": name, "balance": money}) #adding the new entry via accountwriter
                csvfile.close() #closes csv file once entry is added
            
            self.searchInput.setText(name) #sets text value to user name for following method
            self.searchAccount() #performs a search on newly added user to create new window with account details
        except ValueError: #error check if account balance entry is not a valid number
            self.messageBox(title = "ERROR", message = "Input valid account balance.") #message outputted in new box if invalid number entered

    #defined byebye method which quits the program
    def byebye(self):
        self.quit() #quits the program when executed

#new class display to define windows that populate upon searching for user
class display(EasyFrame):
    def __init__(self): #redefining __init__ method from parent class
        EasyFrame.__init__(self, title = "Account Details") #instantiates window from parent __init__ method
        self.addLabel(text = "Name", row = 0, column = 0) #Add label to display Name
        self.nameField = self.addLabel(text = "", row = 0, column = 1) #Add label nameField to set user name from dictionary
        self.addLabel(text = "Balance", row = 1, column = 0) #add label to display Balance
        self.fundField = self.addLabel(text = '', row = 1, column = 1) #add fundField label to set balance from dictionay entry
        self.addButton(text = "Withdraw", row = 2, column = 0, command = self.withdraw) #adding Withdraw button
        self.addButton(text = "Deposit", row = 2, column = 1, command = self.deposit) #adding Deposit button
        self.addButton(text = "Close Account", row = 3, column = 0, command = self.delete) #adding Close Account button
        self.addButton(text = "Exit", row = 3, column = 1, command = self.exit) #adding button to close the extra window
        self.updateButton = self.addButton(text = '', row = 4, column = 0, command = self.update) #adding updateButton for update command and add image
        self.refresh = PhotoImage(file = 'refresh1.gif') #setting refresh to imported refresh1 image
        self.updateButton['height'] = 30 #setting height of updateButton
        self.updateButton['width'] = 30 #setting width of updateButton
        self.updateButton["image"] = self.refresh #setting updateButton to refresh image

    #setting withdraw method
    def withdraw(self):
        amount = self.prompterBox(title = "Withdraw", promptString = "Withdraw amount:") #amount is returned value from user entry in prompt box
        try: #try except clause to ensure that entered value is numeric
            stuff = float(amount) #check for numeric entry and sets stuff to amount converted to float datatype
            if float(amount) > float(self.fundField['text']): #checks to see if entered amount is greater than account value
                self.messageBox(title = 'ERROR', message = "Insufficient funds.") #message displayed if withdraw amount is greater than account balance
            else: #performs withdraw when account balance is greater than withdraw
                tempfile = NamedTemporaryFile('w+t', newline = '', delete = False) #creates tempfile NamedTemporaryFile to update dictionary entry in csv
                with open('data.csv', newline = '') as csvfile, tempfile: #opens data.csv as csvfile and tempfile
                    fieldNames = ['name', 'balance'] #defined fieldNames with dictionary headers for following command
                    fundWriter = csv.DictWriter(tempfile, fieldnames = fieldNames) #creates fundWriter to write entries into tempfile
                    fundWriter.writeheader() #writes header for new csv file
                    fundReader = csv.DictReader(csvfile) #fundReader imports data from existing csv file to perform update
                    for row in fundReader: #checks each row of dictionary entries
                        if row['name'] == self.nameField['text']: #checks to see if names match updated account
                            minus = float(row['balance']) - float(amount) #minus is new balance after subtracting withdrawal
                            fundWriter.writerow({'name':row['name'], 'balance':str(minus)}) #writes new ditionary entry with updated balance into tempfile
                        else: #checks for name mismatch
                            fundWriter.writerow({'name':row['name'], 'balance':row['balance']}) #writes new dictionary entry without updating balance since no transaction performed
                shutil.move(tempfile.name, 'data.csv') #copies tempfile into data.csv name
                self.update()
        except ValueError:
            self.messageBox(title = "ERROR", message = "Input valid amount.")

    def deposit(self):
        amount = self.prompterBox(title = "Deposit", promptString = "Deposit amount:")
        try:
            float(amount)
            tempfile = NamedTemporaryFile('w+t', newline = '', delete = False)
            with open('data.csv', newline = '') as csvfile, tempfile:
                fieldNames = ['name', 'balance']
                fundWriter = csv.DictWriter(tempfile, fieldnames = fieldNames)
                fundWriter.writeheader()
                fundReader = csv.DictReader(csvfile)
                for row in fundReader:
                    if row['name'] == self.nameField['text']:
                        plus = float(row['balance']) + float(amount)
                        fundWriter.writerow({'name':row['name'], 'balance':str(plus)})
                    else:
                        fundWriter.writerow({'name':row['name'], 'balance':row['balance']})
            shutil.move(tempfile.name, 'data.csv')
            self.update()
        except ValueError:
            self.messageBox(title = "ERROR", message = "Input valid amount.")

    def delete(self):
        sure = self.prompterBox(title = "Are you sure?", promptString = "Enter y to confirm")
        if sure == "y":
            tempfile = NamedTemporaryFile('w+t', newline = '', delete = False)
            with open('data.csv', newline = '') as csvfile, tempfile:
                fieldNames = ['name', 'balance']
                acctWriter = csv.DictWriter(tempfile, fieldnames = fieldNames)
                acctWriter.writeheader()
                acctReader = csv.DictReader(csvfile)
                for row in acctReader:
                    if row['name'] != self.nameField['text']:
                        acctWriter.writerow({'name':row['name'], 'balance':row['balance']})
            shutil.move(tempfile.name, 'data.csv')
            self.destroy()            

    def exit(self):
        self.destroy()

    def update(self):
        with open("data.csv", 'r') as csvfile:
            fieldNames = ["name", "balance"]
            accountReader = csv.DictReader(csvfile, fieldnames = fieldNames)
            for row in accountReader:
                if row["name"] == self.nameField['text']:
                    self.fundField["text"] = row['balance']
            csvfile.close()



def main():
    window().mainloop()

if __name__ == "__main__":
    main()
