def startOptions():
    print("Welcome: Select one option below:")
    print("\n★ ‧₊˚ MAIN MENU ‧₊˚ ★")
    print("------------------------------------------------")
    print("  [1] View / Query Data")
    print("  [2] Insert Data")
    print("  [3] Delete Data")
    print("  [4] Update Data")
    print("  [5] Quit")
    print("------------------------------------------------")

    while True:
        user_input = input("\nNumber Selection: ")

        try:
            choice = int(user_input)
        except ValueError:
            print("Invalid input — enter a number 1–5.")
            continue  # ask again

        if choice < 1 or choice > 5:
            print("Invalid input — enter a number 1–5.")
            continue  


        return choice


def viewTableMenu():
    while True:
        table = input(
            "\n✦ Select a Table ✦\n"
            "[1] Vendors\n"
            "[2] Assembly Parts\n"
            "[3] Piece Parts\n"
            "[4] Usages\n"
            "[5] Parts\n"
            "[6] Return to Main Menu\n> "
        )
        try:
            table_num = int(table)
        except ValueError:
            print("Invalid input — enter a number 1–6.")
            continue
        # Validate range
        if table_num < 1 or table_num > 6:
            print("Invalid input — enter a number 1–6.")
            continue
        # Option 6 exits
        if table_num == 6:
            return
        # Otherwise return a valid choice
        return table_num

    

def opTableMenu():
    while True:
        try:
            table = int(input(
                "\n✦ Select a Table ✦\n"
                "[1] Vendors\n"
                "[2] Assembly Parts\n"
                "[3] Piece Parts\n"
                "[4] Usages\n"
                "[5] Return to Main Menu\n> "
            ))
        except ValueError:
            print("Invalid input — enter a number 1–5.")
            continue
        if table < 1 or table > 5:
            print("Invalid input — enter a number 1–5.")
            continue
        if table == 5:
            return None   

        return table



