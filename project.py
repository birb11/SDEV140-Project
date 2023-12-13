"""
Program: project.py
Author: Daven Kim
Date: 12/12/2023

This program records user names and respective account balances and displays them.
The program uses a .csv file to record accounts and balances and to search users.
It also allows users to withdraw and deposit to their account or close an account.
"""

from breezypythongui import EasyFrame
import csv
from tempfile import NamedTemporaryFile
import shutil
from tkinter import PhotoImage



class window(EasyFrame):
    def __init__(self):
        EasyFrame.__init__(self, title = "DK Banking App")
        
        self.cash = PhotoImage(file = 'cash.gif')
        self.background = self.addLabel(text = '', row = 0, column = 0, rowspan = 2, columnspan = 3)
        self.background["image"] = self.cash
        
        self.addLabel(text = "Enter Name:", row = 0, column = 0)
        self.searchInput = self.addTextField(text = "", row = 0, column = 1)
        self.search = self.addButton(text = "Search", row = 1, column = 0, command = self.searchAccount)
        self.add = self.addButton(text = "New Account", row = 1, column = 1, command = self.addAccount)
        self.exit = self.addButton(text = "Quit", row = 1, column = 2, command = self.byebye)

    def searchAccount(self):
        temp = self.searchInput.getText()
        try:
            with open("data.csv", 'r') as csvfile:
                accountreader = csv.DictReader(csvfile)
                found = False
                for row in accountreader:
                    print(row)
                    check = row["name"]
                    if check.lower() == temp.lower():
                        found = True
                        funds = row["balance"]
                        person = row["name"]
                csvfile.close()
            if found == False:
                self.messageBox(title = "ERROR", message = "Input existing user")
            else:
                show = display()
                show.nameField["text"] = person
                show.fundField["text"] = funds

 
        except ValueError:
            self.messageBox(title = "ERROR", message = "Input existing user")

    def addAccount(self):
        name = self.prompterBox(title = "Add Account", promptString = "Enter full name:")
        money = self.prompterBox(title = "Account balance", promptString = "Add account balance:")

        try:
            float(money)
            with open("data.csv", 'r') as csvfile:
                fieldNames = ['name', 'balance']
                accountreader = csv.DictReader(csvfile, fieldnames = fieldNames)
                for row in accountreader:
                    if row['name'].lower() == name.lower():
                        self.messageBox(title = "ERROR", message = "User already exists.")
                        csvfile.close()
                        return
                csvfile.close()
            with open("data.csv", 'a') as csvfile:
                fieldNames = ["name", "balance"]
                accountwriter = csv.DictWriter(csvfile, fieldnames = fieldNames)
                accountwriter.writerow({"name": name, "balance": money})
                csvfile.close()
            
            self.searchInput.setText(name)
            self.searchAccount()
        except ValueError:
            self.messageBox(title = "ERROR", message = "Input valid account balance.")
    
    def byebye(self):
        self.quit()

class display(EasyFrame):
    def __init__(self):
        EasyFrame.__init__(self, title = "Account Details")
        self.addLabel(text = "Name", row = 0, column = 0)
        self.nameField = self.addLabel(text = "", row = 0, column = 1)
        self.addLabel(text = "Balance", row = 1, column = 0)
        self.fundField = self.addLabel(text = '', row = 1, column = 1)
        self.addButton(text = "Withdraw", row = 2, column = 0, command = self.withdraw)
        self.addButton(text = "Deposit", row = 2, column = 1, command = self.deposit)
        self.addButton(text = "Close Account", row = 3, column = 0, command = self.delete)
        self.addButton(text = "Exit", row = 3, column = 1, command = self.exit)
        self.updateButton = self.addButton(text = '', row = 4, column = 0, command = self.update)
        self.refresh = PhotoImage(file = 'refresh1.gif')
        self.updateButton['height'] = 30
        self.updateButton['width'] = 30
        self.updateButton["image"] = self.refresh
        


    def withdraw(self):
        amount = self.prompterBox(title = "Withdraw", promptString = "Withdraw amount:")
        try:
            stuff = float(amount)
            if float(amount) > float(self.fundField['text']):
                self.messageBox(title = 'ERROR', message = "Insufficient funds.")
            else:
                tempfile = NamedTemporaryFile('w+t', newline = '', delete = False)
                with open('data.csv', newline = '') as csvfile, tempfile:
                    fieldNames = ['name', 'balance']
                    fundWriter = csv.DictWriter(tempfile, fieldnames = fieldNames)
                    fundWriter.writeheader()
                    fundReader = csv.DictReader(csvfile)
                    for row in fundReader:
                        if row['name'] == self.nameField['text']:
                            minus = float(row['balance']) - float(amount)
                            fundWriter.writerow({'name':row['name'], 'balance':str(minus)})
                        else:
                            fundWriter.writerow({'name':row['name'], 'balance':row['balance']})
                shutil.move(tempfile.name, 'data.csv')
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
