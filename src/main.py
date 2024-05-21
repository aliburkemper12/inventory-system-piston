import inventory

# creates database and table
inventory.create_db()

conn = inventory.conn

print('what would you like to do?\n')
print('E - for new entry\n')
print('L - for look up of item\n')

# #creates database and table
# inventory.create_db()
# conn = inventory.conn
# data = inventory.print_items()
# inventory.conn.close()

inp = input()
print()

if(inp == 'L'):
    print('Enter name of item to find\n')
    name = input()
    print()
    inventory.find(conn, name)
    print('Would you like to edit this item?\nY for yes N for no')
    ans = input()
    if ans == 'Y':
        print('Would you like to change quantity, name, description, or delete item?\n')
        print('1 for quantity, 2 for name, 3 for description, 4 for delete')
        change = input()
        if change == '1':
            print('Enter new quantity:')
            quantity = input()
            inventory.update_quantity(conn, quantity, name)
        if change == '2':
            print('Enter new name:')
            new_name = input()
            inventory.update_name(conn, name, new_name)
        if change == '3':
            print('Enter new description:')
            description = input()
            inventory.update_description(conn, name, description)
        if change == '4':
            print('Are you sure you want to delete?\nY for yes, N for no\n')
            ans = input()
            if ans == 'Y':
                inventory.delete_item(conn, name)
            if ans == 'N':
                print('aborting')
                exit()

if(inp == 'E'):
    print('Enter name of item to enter\n')
    name = input()
    print()

    print('Enter quantity of item to enter\n')
    quantity = input()
    print()
    
    print('Enter description of item to enter\n')
    description = input()
    print()

    inventory.insert_command(conn, name, quantity, description)
    inventory.print_items()

inventory.conn.close()


# inventory.insert_command(conn, 'hdmi', 1)

# inventory.print_items()


