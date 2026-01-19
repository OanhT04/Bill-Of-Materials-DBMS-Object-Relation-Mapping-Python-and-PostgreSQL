
from operations import *
from menu import *

#main 
def main():
    print("Database created: bom_simple.db")

    while True:
        option = startOptions()
        if option == 1:
            queryOperations()
            continue
        elif option == 2:
            insertOperations()
            continue           
        elif option == 3:
            deleteOperations()
        elif option == 4:
            updateOperations()
        elif option == 5:
            print("exiting.....Goodbye!‧₊˚ ★")
            break
        
        print("\nReturning to main menu...\n")


if __name__ == "__main__":
    main()
