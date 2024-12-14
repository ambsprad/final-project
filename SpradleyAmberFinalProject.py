"""
Author: Amber Spradley
Title: Pawn Shop GUI

The purpose of this GUI is to simplify the completion of a pawn transaction 
and a sale transaction for pawn shops.  The main window opens with three button
options: pawn, sale, and exit.  The pawn button opens a pawn transaction window, the sale button
opens a sale transaction, and the exit button exits the program.

Pawn Transaction Window
Users enter the requested information.  The process button will display the entered information
for the pawn and caluclate the pawn fee and redeem amount.  The close button will close the pawn
transaction window.

Sale Transaction Window
Users enter the requested information.  At least one item number and price has to be entered.  The
process button will display the entered transaction information and calcuate the sales tax and total
sale amount.  The close button will close the sale transaction window.
"""

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk, Image

def exitButton():
    """ Closes the main window. """
    root.destroy()
    
def checkIsNumber(input):
    """Checks the input in the Entry widget for valid numeric entry.
        If the entry is valid it returns True else False."""
    if input.isdigit():
        return True
    elif input == "":
        return True
    elif input == ".":
        return True
    else:
        return False
    
def checkIsLetter(input):
    """Checks the input in the Entry widget for valid entry.
        If the entry is valid it returns True else False."""
    if input.isalpha():
        return True
    elif input == "":
        return True
    else:
        return False

##########################################################################################################################################################################

def pawnButton():
    """ Opens the secondary Pawn Transaction Window. """
    pawnWindow = Toplevel(root)
    pawnWindow.title("Pawn Transaction")
    pawnWindow.resizable(0,0)

    def pawnProcessButton():
        """ Displays the transaction information and the calculated pawn fee and redeem amount. """
        global pawnFee
        global redeemAmount
        
        def pawnErrorChecking():
            """Checks for errors in the user's input."""
            noErrors = True # Control variable - True if no errors were found in the user input. False if errors were found
            
            if (firstNameEntry.get() == "" or lastNameEntry.get() == "" or phoneNumberEntry.get() == ""): # Checks for required customer information
                messagebox.showwarning("Warning", "Important customer information is missing.")
                noErrors = False
            elif (dobMonth.get() == "February") and (dobDay.get() == "29") and (int(dobYear.get())%4 != 0): # Checks for a valid birthday for February
                messagebox.showerror("Error", "Invlaid birthday entered.")
                noErrors = False
            elif len(phoneNumberEntry.get()) != 10: # Checks for a valid phone number
                messagebox.showwarning("Warning", "A valid phone number was not entered.")
                noErrors = False
            elif len(descriptEntry.get("1.0", "end-1c")) == 0 or descriptEntry.get("1.0", "1.0") == "\t": # Checks for an empty description box
                messagebox.showerror("Error", "A description must be entered.")
                noErrors = False
            elif loanEntry.get() == "": # Checks for a loan amount entered
                messagebox.showerror("Error", "A loan amount must be entered.")
                noErrors = False    
                
            return noErrors
        
        pawnCanContinue = pawnErrorChecking()
        
        if pawnCanContinue: # Only the process the the transaction if there were no errors in the input
            
            # Perform the calculations 
            loanAmount = float(loanEntry.get())
            pawnFee = 0.23 * loanAmount
            redeemAmount = pawnFee + loanAmount

            # Disable process button to prevent double-processing.
            processButton["state"]="disabled"
            
            # Re-enable the output text box to allow for input
            outputText["state"] = "normal"
            outputText.insert(END, "Completed Pawn For: \n" + firstNameEntry.get() + " " + lastNameEntry.get()+
                          "\nDOB: " +dobMonth.get()+"-"+dobDay.get()+"-"+dobYear.get()+"\nPhone Number: " + phoneNumberEntry.get() + "\nItems "
                          + descriptEntry.get("1.0", "end-1c") + "\nPawn Amount: $%0.2f" % loanAmount + "\nPawn Fee: $%0.2f" % pawnFee +
                          "\nRedeem Amount $%0.2f" % redeemAmount + "\nYour due date is 30 days from the day it was \nwritten. Your item will be forfeited if not"
                            + "\nredeemed or extended by the due date.")
            # Disable the output textbox after the text is displayed
            outputText["state"] = "disabled"
            
    def update(event):
        """Updates the DOB Day combobox based on the month selected."""
        dobDay["values"] = months[dobMonth.get()]
        dobDay.set("1")

    # Register the callback functions for entry  validation
    pawnRegNum = pawnWindow.register(checkIsNumber)
    pawnRegLetter = pawnWindow.register(checkIsLetter)

    # Lists for the number of days in each month 
    d29 = list(range(1, 30))
    d30 = list(range(1, 31))
    d31 = list(range(1, 32))

    # Create a disctionary of months for the DOB comboboxes
    months = dict(
        January=d31,
        February=d29,
        March=d31,
        April=d30,
        May=d31,
        June=d30,
        July=d31,
        August=d31,
        September=d30,
        October=d31,
        November=d30,
        December=d31)
    
    # Create the labels for the pawn window
    firstNameLabel = Label(pawnWindow, text="First Name")
    lastNameLabel = Label(pawnWindow, text="Last Name")
    dobLabel = Label(pawnWindow, text="DOB - MMDDYY")
    phoneNumberLabel = Label(pawnWindow, text="Phone Number")
    descriptLabel = Label(pawnWindow, text="Item Description")
    loanLabel = Label(pawnWindow, text="Total Loan Amount")

    # Set the label positions for the pawn window
    firstNameLabel.grid(row=0, column=0)
    lastNameLabel.grid(row=1, column=0)
    dobLabel.grid(row=2, column=0)
    phoneNumberLabel.grid(row=3, column=0)
    descriptLabel.grid(row=4, column=0)
    loanLabel.grid(row=10, column=0)

    # Create the text entry fields for the pawn window
    firstNameEntry = Entry(pawnWindow)
    lastNameEntry = Entry(pawnWindow)
    #dobEntry = Entry(pawnWindow)
    phoneNumberEntry = Entry(pawnWindow)
    descriptEntry = Text(pawnWindow, height=5, width=30)
    loanEntry = Entry(pawnWindow)
    outputText = Text(pawnWindow, height = 20, width=50)
    
    # Create the DOB comboboxes
    dobDay = ttk.Combobox(pawnWindow, width = 5, values=months["January"])
    dobDay.set("1")
    dobMonth = ttk.Combobox(pawnWindow, width = 5, values=[*months])
    dobMonth.bind('<<ComboboxSelected>>', update) 
    dobMonth.set("January")
    dobYear = ttk.Combobox(pawnWindow, width = 5, values=list(range(1925, 2007)))
    dobYear.set("1990")

    # Position the comboboxes on the window
    dobMonth.grid(row=2, column=1)
    dobDay.grid(row=2, column=2)
    dobYear.grid(row=2, column=3)
    
    # Set the entry field positions for the pawn window
    firstNameEntry.grid(row=0, column=1, columnspan=2)
    lastNameEntry.grid(row=1, column=1, columnspan=2)
    phoneNumberEntry.grid(row=3, column=1, columnspan=2)
    descriptEntry.grid(row=4, column=1, columnspan=2)
    loanEntry.grid(row=10, column=1, columnspan=2)
    outputText.grid(row=12, column=0, columnspan=5)

    # Disable the output box
    outputText["state"] = "disabled"

    # Ensure only letters are entered in the name fields
    firstNameEntry.config(validate="key", validatecommand = (pawnRegLetter, '%P'))
    lastNameEntry.config(validate="key", validatecommand = (pawnRegLetter, '%P'))

    # Ensure only numbers can be input in these fields
    phoneNumberEntry.config(validate="key", validatecommand = (pawnRegNum, '%P'))
    
    # Create the buttons for the pawn window
    cancelButton = Button(pawnWindow, text="Close", command=pawnWindow.destroy)
    processButton = Button(pawnWindow, text="Process", command=pawnProcessButton)

    # Set the positions for the buttons on the pawn window
    cancelButton.grid(row=13, column=0, columnspan=2)
    processButton.grid(row=13, column=1, columnspan=2)

##########################################################################################################################################################################

def saleButton():
    """ Opens the sale transaction window. """
    saleWindow = Toplevel(root)
    saleWindow.title("Sale Transaction")
    saleWindow.resizable(0,0)


    def saleProcessButton():
        """ Displays the transaction info and the calcualted sales tax and the total sale amount. """
        global SALES_TAX 
        global taxAmount
        global totalSale
        
        def errorChecking():
            """ Checks for errors in the user's input."""
            noErrors = True # Control variable - True if no errors were found in the user input. False if errors were found
            
            if (firstNameEntry.get() == "" or lastNameEntry.get() == "" or phoneNumberEntry.get() == ""): #Chcek fo empty customer information
                messagebox.showwarning("Warning", "Important customer information is missing.")
                noErrors = False
            elif (dobMonthSale.get() == "February") and (dobDaySale.get() == "29") and (int(dobYearSale.get())%4 != 0): # Checks if Feb. 29 is valid for the selected year
                messagebox.showerror("Error", "Invlaid birthday entered.")
                noErrors = False
            elif len(phoneNumberEntry.get()) != 10: # Check for valid phone number length
                messagebox.showwarning("Warning", "A valid phone number was not entered.")
                noErrors = False
            elif (len(skuEntry2.get()) > 0 and priceEntry2.get() == "") or (len(skuEntry3.get()) > 0 and priceEntry3.get() == ""): # Checks if an item number is entered without a price
                messagebox.showwarning("Warning", "A price is missing for an item.")
                noErrors = False
            elif skuEntry.get() == "" or (len(priceEntry2.get()) > 0 and skuEntry2.get() == "") or (len(priceEntry3.get()) > 0 and skuEntry3.get() == ""): # Checks if a price is missing an item number
                messagebox.showwarning("Warning", "An item number is missing.")
                noErrors = False
            elif (len(skuEntry.get()) != 5) or (skuEntry2.get() != "" and len(skuEntry2.get()) != 5) or (skuEntry3.get() != "" and len(skuEntry3.get()) !=5): # Checks for a 5 digit item number
                messagebox.showwarning("Warning", "Enter a valid 5 digit item number.")
                noErrors = False
            elif priceEntry.get() == "" or priceEntry.get() != "": # Checks if a price is entered in the first price entry box and that its a valid price
                try:
                    holderVal = float(priceEntry.get())
                except ValueError:
                    messagebox.showerror("Error", "A valid price must be entered")
                    noErrors = False
                    
            if len(priceEntry2.get()) > 0: # Check that a number is entered into price box 2
                try:
                    holderVal2 = float(priceEntry2.get())
                except ValueError:
                    messagebox.showerror("Error", "A valid price must be entered")
                    noErrors = False
            if priceEntry3.get() != "": # Check that a number is enterd into price box 3
                try:
                    holderVal3 = float(priceEntry3.get())
                except ValueError:
                    messagebox.showerror("Error", "A valid price must be entered")
                    noErrors = False
    
            return noErrors

        canContinue = errorChecking() # Only process the transaction if there are no errors in the input       
        SALES_TAX = 0.07

        if canContinue:
            price1 = float(priceEntry.get())

            # Set the values of the optional additional prices
            if priceEntry2.get() == "":
                price2 = 0.00
            else:
                price2 = float(priceEntry2.get())

            if priceEntry3.get() == "":
                price3 = 0.00
            else:
                price3 = float(priceEntry3.get())

            # Perform the calculations
            saleAmount = price1 + price2 + price3
            taxAmount = SALES_TAX * saleAmount
            totalSale = (1 + SALES_TAX) * saleAmount

            # Disable the process button to prevent double-processing
            processButton["state"]="disabled"
  
            # Re-enable the output text box to allow for input
            outputText["state"] = "normal"

            # Display the output in the textbox
            outputText.insert(END, "Completed Sale For: \n" + firstNameEntry.get() + " " + lastNameEntry.get()+
                          "\nDOB: " +dobMonthSale.get()+"-"+dobDaySale.get()+"-"+dobYearSale.get()+"\nPhone Number: " + phoneNumberEntry.get() + "\nSold Items: "
                          +"\nItem " + skuEntry.get() + "   Price: $ %0.2f" % price1 + "\nItem " + skuEntry2.get() +
                          "    Price: $ %0.2f" % price2 + "\nItem " + skuEntry3.get() + "    Price: $ %0.2f" % price3
                          + "\nSale Amount: $ %0.2f" % saleAmount + "\nTaxes: $ %0.2f" % taxAmount + "\nTotal Sale Amount: $ %0.2f" % totalSale)
        
            # Disable the output textbox after the text is displayed
            outputText["state"] = "disabled"
            
    def saleUpdate(event):
        """Updates the DOB Day combobox based on the month selected."""
        dobDaySale["values"] = monthsSale[dobMonthSale.get()]
        dobDaySale.set("1")
    
    # Lists for the number of days in each month
    d29 = list(range(1, 30))
    d30 = list(range(1, 31))
    d31 = list(range(1, 32))

    # Dictionary for months for the comboboxes
    monthsSale = dict(
        January=d31,
        February=d29,
        March=d31,
        April=d30,
        May=d31,
        June=d30,
        July=d31,
        August=d31,
        September=d30,
        October=d31,
        November=d30,
        December=d31)
            
    # Register the callback functions for entry  validation                     
    regNum = saleWindow.register(checkIsNumber)
    regLetter = saleWindow.register(checkIsLetter)
    
    # Create labels
    firstNameLabel = Label(saleWindow, text="First Name")
    lastNameLabel = Label(saleWindow, text="Last Name")
    dobLabel = Label(saleWindow, text="DOB - MMDDYY")
    phoneNumberLabel = Label(saleWindow, text="Phone Number")
    skuLabel = Label(saleWindow, text="5 Digit Item Number")
    priceLabel = Label(saleWindow, text="Price")
    skuLabel2 = Label(saleWindow, text="5 Digit Item Number")
    priceLabel2 = Label(saleWindow, text="Price")
    skuLabel3 = Label(saleWindow, text="5 Digit Item Number")
    priceLabel3 = Label(saleWindow, text="Price")
    outputText = Text(saleWindow, height = 20, width=50)

    # Set the label positions
    firstNameLabel.grid(row=0, column=0)
    lastNameLabel.grid(row=1, column=0)
    dobLabel.grid(row=2, column=0)
    phoneNumberLabel.grid(row=3, column=0)
    skuLabel.grid(row=4, column=0)
    priceLabel.grid(row=5, column=0)
    skuLabel2.grid(row=6, column=0)
    priceLabel2.grid(row=7, column=0)
    skuLabel3.grid(row=8, column=0)
    priceLabel3.grid(row=9, column=0)
    outputText.grid(row=12, column=0, columnspan=5)

    # Create DOB comboboxes
    dobDaySale = ttk.Combobox(saleWindow, width = 5, values=monthsSale["January"])
    dobDaySale.set("1")
    dobMonthSale = ttk.Combobox(saleWindow, width = 5, values=[*monthsSale])
    dobMonthSale.bind('<<ComboboxSelected>>', saleUpdate) 
    dobMonthSale.set("January")
    dobYearSale = ttk.Combobox(saleWindow, width = 5, values=list(range(1925, 2007)))
    dobYearSale.set("1990")

    # Position the DOB Comboboxes
    dobMonthSale.grid(row=2, column=1)
    dobDaySale.grid(row=2, column=2)
    dobYearSale.grid(row=2, column=3)

    # Disable the output box
    outputText["state"] = "disabled"
    
    # Create the text entry fields
    firstNameEntry = Entry(saleWindow)
    lastNameEntry = Entry(saleWindow)
    phoneNumberEntry = Entry(saleWindow)
    skuEntry = Entry(saleWindow)
    priceEntry = Entry(saleWindow)
    skuEntry2 = Entry(saleWindow)
    priceEntry2 = Entry(saleWindow)
    skuEntry3 = Entry(saleWindow)
    priceEntry3 = Entry(saleWindow)

    # Set the entry field positions
    firstNameEntry.grid(row=0, column=1, columnspan=2)
    lastNameEntry.grid(row=1, column=1, columnspan=2)
    phoneNumberEntry.grid(row=3, column=1, columnspan=2)
    skuEntry.grid(row=4, column=1, columnspan=2)
    priceEntry.grid(row=5, column=1, columnspan=2)
    skuEntry2.grid(row=6, column=1, columnspan=2)
    priceEntry2.grid(row=7, column=1, columnspan=2)
    skuEntry3.grid(row=8, column=1, columnspan=2)
    priceEntry3.grid(row=9, column=1, columnspan=2)

    # Ensure only letters are entered in the name fields
    firstNameEntry.config(validate="key", validatecommand = (regLetter, '%P'))
    lastNameEntry.config(validate="key", validatecommand = (regLetter, '%P'))

    # Ensure only numbers can be input in these fields
    phoneNumberEntry.config(validate="key", validatecommand = (regNum, '%P'))
    skuEntry.config(validate="key", validatecommand = (regNum, '%P'))
    skuEntry2.config(validate="key", validatecommand = (regNum, '%P'))
    skuEntry3.config(validate="key", validatecommand = (regNum, '%P'))   

    # Create buttons
    cancelButton = Button(saleWindow, text="Close", command=saleWindow.destroy)
    processButton = Button(saleWindow, text="Process", command=saleProcessButton) 

    # Set the button positions
    cancelButton.grid(row=14, column=0, columnspan=2)
    processButton.grid(row=14, column=1, columnspan=2)
################################################################################################################################################################################# 

# Creates the main window, sets the title, and make it un-resizable  
root = Tk()
root.title("Amber's Pawn Shop GUI")
root.resizable(0,0)

# Create the labels, images, and buttons
greetingLabel = Label(root, text="Welcome to Amber's Pawn Shop GUI")

pawnImg = ImageTk.PhotoImage(Image.open("pawn.png"))
pawnImgLabel = Label(image=pawnImg)

saleImg = ImageTk.PhotoImage(Image.open("sale.png"))
saleImgLabel = Label(image=saleImg)

pawnButton = Button(root, text="Pawn", command=pawnButton)
saleButton = Button(root, text="Sale", command=saleButton)
exitButton = Button(root, text="Exit", command=exitButton)

# Set the positions on the screen
greetingLabel.grid(row=0, column=0, columnspan=3)
pawnImgLabel.grid(row=1, column=0)
saleImgLabel.grid(row=1, column=2)
pawnButton.grid(row=2, column=0)
saleButton.grid(row=2, column=1)
exitButton.grid(row=2, column=2)

# Runs the main window
root.mainloop()
