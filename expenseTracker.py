import os
import csv
from tkinter import *


'''
This function takes personal expenses as input
and adds them to expenses dictionary
'''
# ExpensesList tracks all the expenses in a list with each entry as a dictionary
expensesList = []
#beforeSaveExpensesList = []
fileOpened = False
saveFile = None
columns = ['Date', 'Category', 'Amount', 'Description']
file_name = 'expenses.csv'
root = Tk()
root.title('Expenses Tracker')



def loadExpensesFromcsv():
    #print("Entered loadExpenses()")
    file_exists = os.path.isfile(file_name)
    if file_exists:
        with open(file_name,"r") as expenseFile:
            # get a handle to file reader
            reader = csv.DictReader(expenseFile)
            fileOpened = True
            #Skip header row
            #header = next(reader)
            #print(f'Header row: {header}')
            # navigate through actual data rows
            #print(f"Expenses Count: {len(expensesList)}")
            for row in reader:
                expenseDate = row.get('Date')
                expenseCategory = row.get('Category')
                expenseAmount = float(row.get('Amount'))
                expenseDescription = row.get('Description')
                isSaved = 0
                expensesList.append(row)
        print(f"Exited loadExpenses() {len(expensesList)}")

loadExpensesFromcsv()

def addExpense():
    global saveFile
    print('Please enter your expenses below\n')
    expenseDate = input('Enter the date of the expense in the format YYYY-MM-DD: ')
    expenseCategory = input('Enter the category of the expense: ')
    expenseAmount = float(input('Enter the expense amount $: '))
    expenseDescription = input('Enter the description of the expense: ')
    expenseDict = {
        'Date': expenseDate,
        'Category': expenseCategory,
        'Amount': expenseAmount,
        'Description': expenseDescription,
        'isSaved': 0 #to track if an expense needs to be saved to file when saveExpenses menu option is clicked
    }
    #beforeSaveExpensesList.append(expenseDict)
    #print(len(beforeSaveExpensesList))
    expensesList.append(expenseDict)
    saveFile = True

'''
This function loops through all the expenses and displays each entry.
It validates the data for missing details in an entry and notifies the user that 
the task is incomplete
'''
def viewExpenses():
    #print("unsaved rows: " + str(len(beforeSaveExpensesList)))
    #expensesList.extend(beforeSaveExpensesList)
    if not expensesList:
        print("No expenses Saved so far")

    for expense in expensesList:
        ''' 
        validate each entry to make sure all values are entered
        If a value is not entered, warn the user that it is incomplete
        '''
        if not expense['Date'] or not expense['Category'] or not expense['Amount'] or not expense['Description']:
            print("Below expense entry is incomplete, update to complete it\n")
        print(expense)

'''
This functiona lets user set monthly budgets and track expenses against the budget
'''
def trackBudget():
    total_expense = 0.00
    monthly_budget = input('Enter the budget for the month')
    monthly_budget = float(monthly_budget)
    print("Monthly budget enetered: " + str(monthly_budget))
    total_expense = __calculateTotalExpensesForMonth()
    print("Total expense: " + str(total_expense))
    if total_expense > monthly_budget:
        print(f'You have exceeded the monthly budget by {total_expense - monthly_budget}\n')
    elif total_expense < monthly_budget:
         print(f'You have ${monthly_budget - total_expense} left for the month\n')
    else:
        print(f'Your expenses for the month matched the monthly budget\n')

# Fetch all expenses and add them up
def __calculateTotalExpensesForMonth():
    global saveFile
    totalExpenses = 0.00
    print("In calculate " + str(totalExpenses))
    for expense in expensesList:
        if not expense['Amount']:
            continue;
        totalExpenses += float(expense['Amount'])
    print(str(totalExpenses))
    return totalExpenses

def saveExpenses():
    global saveFile
    # 1. Check if file exists BEFORE opening
    file_exists = os.path.isfile(file_name)


    # 2. Open in Append mode
    with open(file_name, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=columns)

        # 3. Only write header if the file didn't exist
        if not file_exists:
            writer.writeheader()
            print("Header written (New file created).")

        # 4. Write the data
        for expense in expensesList:
            expenseDate = expense.get('Date')
            expenseCategory = expense.get('Category')
            expenseAmount = expense.get('Amount')
            expenseDesciption = expense.get('Description')
            isSaved = expense.get('isSaved')
            print(f'details: {expenseDate} {expenseCategory} {expenseAmount} {expenseDesciption} {isSaved}')
            if isSaved is None:
                continue
            if isSaved == 1:
                print("Is Saved in if is " + str(isSaved))
                continue
            else:
                print("Is Saved in else is " + str(isSaved))
                expenseDict = {'Date': expenseDate, 'Category': expenseCategory, 'Amount': expenseAmount, 'Description': expenseDesciption}
                writer.writerow(expenseDict)
                expense['isSaved'] = 1
                #expensesList.append(expenseDict)
                print("Is Saved in else before exit is " + str(expense['isSaved']))

    saveFile = False


# This function saves the unsaved expenses and exits the tkinter window
def exit():
    #global saveFile
    #if saveFile is not None and True:
    #print("Saving in exit()")
    print("In Exit before save")
    saveExpenses()
    print("In Exit after save")
    root.destroy()

# This function creates a menu with 5 options
def displayMenu():
    main_menu = Menu(root)
    root.config(menu=main_menu)
    # Create a submenu
    submenu = Menu(main_menu)
    main_menu.add_cascade(menu=submenu, label="Expense Tracker")

    submenu.add_command(label="Add expense", command=addExpense)
    submenu.add_command(label="View expenses", command=viewExpenses)
    submenu.add_command(label="Track budget", command=trackBudget)
    submenu.add_command(label="Save expenses", command=saveExpenses)
    submenu.add_command(label = "Exit", command=exit)



displayMenu()


root.mainloop()