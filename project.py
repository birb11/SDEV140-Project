"""
Program: project.py
Author: Daven Kim
Date: 12/3/2023

This program records user names and respective account balances and displays them.
It also allows users to withdraw and deposit to their account.
"""

from breezypythongui import EasyFrame
import csv
from tempfile import NamedTemporaryFile
import shutil

class window(EasyFrame):
    def __init__(self):
        EasyFrame.__init__(self, title = "DK Banking App")
        self.addLabel(text = "Enter Name:", row = 0, column = 0)
        self.searchInput = self.addTextField(text = "", row = 0, column = 1)
        self.search = self.addButton(text = "Search", row = 1, column = 0, command = self.searchAccount)
        self.add = self.addButton(text = "New Account", row = 1, column = 1, command = self.addAccount)

    def searchAccount(self):
        temp = self.searchInput.getText()
        try:
            with open('data.csv', newline = '') as csvfile:
                accountreader = csv.DictReader(csvfile)
                for row in accountreader:
                    if row['name'] == temp:
                        funds = row['balance']
                        show = display()
                        show.nameField["text"] = temp
                        show.fundField["text"] = funds

 
        except ValueError:
            self.messageBox(title = "ERROR", message = "Input existing user")

    def addAccount(self):
        name = self.prompterBox(title = "Add Account", promptString = "Enter full name:")
        money = self.prompterBox(title = "Account balance", promptString = "Add account balance:")

        try:
            float(money)
            with open('data.csv', 'w') as csvfile:
                fieldnames = ['name', 'balance']
                accountwriter = csv.DictWriter(csvfile, fieldnames = fieldnames)
                accountwriter.writerow({'name': name, 'balance': money})
            
            self.searchInput.setText(name)
            self.searchAccount()
        except ValueError:
            self.messageBox(title = "ERROR", message = "Input valid account balance.")

class display(EasyFrame):
    def __init__(self):
        EasyFrame.__init__(self, title = "Account Details")
        self.addLabel(text = "Name", row = 0, column = 0)
        self.nameField = self.addLabel(text = "", row = 0, column = 1)
        self.addLabel(text = "Balance", row = 1, column = 0)
        self.fundField = self.addLabel(text = '', row = 1, column = 1)
        self.addButton(text = "Withdraw", row = 2, column = 0, command = self.withdraw)
        self.addButton(text = "Deposit", row = 2, column = 1, command = self.deposit)
        self.addButton(text = "Exit", row = 2, column = 2, command = self.exit)

    def withdraw(self):
        amount = self.prompterBox(title = "Withdraw", promptString = "Withdraw amount:")
        try:
            stuff = float(amount)
            if float(amount) > float(self.fundField['text']):
                self.messageBox(title = 'ERROR', message = "Withdraw greater than account balance.")
            else:
                tempfile = NamedTemporaryFile('w+t', newline = '', delete = False)
                with open('data.csv', newline = '') as csvfile, tempfile:
                    fieldnames = ['name', 'balance']
                    fundWriter = csv.DictWriter(tempfile, fieldnames = fieldnames)
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
                fieldnames = ['name', 'balance']
                fundWriter = csv.DictWriter(tempfile, fieldnames = fieldnames)
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

    def exit(self):
        self.quit()

    def update(self):
        with open('data.csv', newline = '') as csvfile:
            fieldnames = ['name', 'balance']
            accountReader = csv.DictReader(csvfile, fieldnames = fieldnames)
            for row in accountReader:
                if row['name'] == self.nameField['text']:
                    self.fundField['text'] = row['balance']



def main():
    window().mainloop()

if __name__ == "__main__":
    main()
