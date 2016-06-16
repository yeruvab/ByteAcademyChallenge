
import mysql.connector
from mysql.connector import MySQLConnection, Error



def main():
    inpt = header_input()

    try:
        conn = mysql.connector.connect(host='localhost',
                                       database='contacts_manager',
                                       user='root',
                                       password='Powerstar1')

        cursor = conn.cursor()

        while inpt == 'a' or inpt == 'A' or 'r' or inpt == 'R' or inpt == 'l' or inpt == 'L' or 'e' or inpt == 'E' or 'x' or inpt == 'X':
        
            if inpt == 'a' or inpt == 'A':
                cname, cphone, cemail = add_contact()
                query = "INSERT INTO contacts(cname,cphone,cemail) " \
                        "VALUES(%s,%s,%s)"
                args = (cname,cphone,cemail)

                cursor.execute(query,args)

                conn.commit()

                print('\nContact added.')

            elif inpt == 'r' or inpt == 'R':
                cname = rem_contact()
                query = "DELETE FROM contacts WHERE cname = %s"

                cursor.execute(query, (cname,))

                conn.commit()

                print('\nContact removed.')

            elif inpt == 'l' or inpt == 'L':
                query = "SELECT * FROM contacts " \
                        "ORDER BY cname"
                cursor.execute(query)
                rows = cursor.fetchall()

                print("\n\nList Of All Contacts:")
                for row in rows:
                    print('\nName:',row[0])
                    
                    phones = row[1].split(' ')
                    print('Phone(s):')
                    for num in phones:
                        print(num)
                        
                    emails = row[2].split(' ')
                    print('Email(s):')
                    for email in emails:
                        print(email)

            elif inpt == 'e' or inpt == 'E':
                cname = edit_contact()
                query = "SELECT cname, cphone, cemail FROM contacts " \
                        "WHERE cname = %s"
                cursor.execute(query, (cname,))
                row = cursor.fetchone()

                print('Current Contact:', row[0], row[1], row[2])

                temp = cname
                cname = input('Enter new name: ')
                cphone = input('Enter new phone: ')
                cemail = input('Enter new email: ')

                query = "UPDATE contacts " \
                        "SET cname=%s, cphone=%s, cemail=%s" \
                        "WHERE cname=%s"
                
                cursor.execute(query, (cname,cphone,cemail,temp,))

                conn.commit()

                print('\nContact updated!')

            else:
                print('\nExiting app...')
                break

            inpt = header_input()

        else:
            print("It's not a valid option. Try again!")
            
    except Error as e:
        print(e)
 
    finally:
        cursor.close()
        conn.close()

def header_input():
    print('\n\n\n************CONTACT MANAGER************')
    print('OPTIONS:')
    print('Enter (A) to Add a contact')
    print('Enter (R) to Remove a contact')
    print('Enter (E) to Edit a contact')
    print('Enter (L) to List all contacts')
    print('Enter (X) to Exit application \n')

    return input()


def add_contact():
    print("Enter contact name: ")
    cname = input()
    print("Enter contact phone(s) (If there's more than 1 enter them seperated by a space): ")
    cphone = input()
    print("Enter contact email(s) (If there's more than 1 enter them seperated by a space): ")
    cemail = input()
    return cname, cphone, cemail


def rem_contact():
    print("Enter the contact name to be removed")
    cname = input()
    return cname


def edit_contact():
    name = input("Enter the name of the contact to be edited: ")
    return name
    

if __name__ == '__main__':
    main()
