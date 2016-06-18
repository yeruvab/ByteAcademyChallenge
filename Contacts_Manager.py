

import sqlite3
from sqlite3 import Error


def main():
    inpt = header_input()

    try:
        conn = sqlite3.connect('contacts_manager.db')  
        cursor = conn.cursor()

        while inpt == 'a' or inpt == 'A' or 'r' or inpt == 'R' or inpt == 'l' or inpt == 'L' or 'e' or inpt == 'E' or 'x' or inpt == 'X':
        
            if inpt == 'a' or inpt == 'A':
                uname, cname, cphone, cemail = add_contact()


                query = """SELECT uid FROM users
                        WHERE uname="{}"
                        """.format(uname)
                cursor.execute(query)
                
                userid = cursor.fetchone()

                if userid == None: #First creates the user and then creates contact when user doesn't exist
                    
                    
                    cursor.execute('''INSERT INTO users(uname)
                            VALUES('{}')
                            '''.format(uname))

                    conn.commit()

                    query = """SELECT uid FROM users
                            WHERE uname="{}"
                            """.format(uname)
                    cursor.execute(query)
                    userid = cursor.fetchone()
                    

                    userid = int(userid[0])

                    query = """INSERT INTO contacts(uid,cname,cphone,cemail)
                            VALUES('{}','{}','{}','{}')""".format(userid,cname,cphone,cemail)
                    

                    cursor.execute(query)

                    conn.commit()

                    print('\n\nContact added.')

                
                elif type(userid[0]) == int: #Directly creates contact when the user already exists
                    userid = int(userid[0])
                    
                    query = """INSERT INTO contacts(uid,cname,cphone,cemail)
                            VALUES('{}','{}','{}','{}')
                            """.format(userid,cname,cphone,cemail)

                    cursor.execute(query)

                    conn.commit()

                    print('\nContact added.')

            #needs changes in WHERE clause
            elif inpt == 'r' or inpt == 'R':
                uname,cname = edit_contact()

                query = """SELECT uid FROM users
                        WHERE uname="{}"
                        """.format(uname)
                cursor.execute(query)
                userid = cursor.fetchone()

                if userid == None:
                    print('\n'+uname, "doesn't have any contacts.")

                else:
                    userid = int(userid[0])

                    query = "DELETE FROM contacts WHERE uid = {} and cname = '{}'".format(str(userid),cname)

                    cursor.execute(query)
                    conn.commit()

                    print('\nContact removed.')

            elif inpt == 'l' or inpt == 'L':
                uname = list_contact()

                query = """SELECT uid FROM users
                        WHERE uname="{}"
                        """.format(uname)
                cursor.execute(query)
                userid = cursor.fetchone()
                
                if userid != None: 
                    userid = int(userid[0])
                    print("\n\n"+uname+"'s contacts:")
                
                    query = """SELECT cname,cphone,cemail
                            FROM contacts
                            WHERE uid={}
                            ORDER BY cname ASC""".format(str(userid))
                    cursor.execute(query)
                    rows = cursor.fetchall()

                    print("\nList Of All Contacts:")
                    for row in rows:
                        print('\nName:',row[0])
                        
                        phones = row[1].split(' ')
                        print('\nPhone(s):')
                        for num in phones:
                            print(num)
                            
                        emails = row[2].split(' ')
                        print('\nEmail(s):')
                        for email in emails:
                            print(email)

                else:
                    print(uname, "doesn't have any contacts.")

            elif inpt == 'e' or inpt == 'E':
                uname,cname = edit_contact()
                query = """SELECT uid FROM users
                        WHERE uname="{}"
                        """.format(uname)
                cursor.execute(query)
                userid = cursor.fetchone()

                if userid != None: 
                    userid = int(userid[0])
                
                    query = """SELECT cname, cphone, cemail FROM contacts
                            WHERE uid = {} and cname="{}"
                            """.format(str(userid),cname)
                    cursor.execute(query)
                    row = cursor.fetchone()

                    print('\nCurrent Contact:')
                    print('\nName: ', row[0])
                    print('\nPhone(s): ',row[1])
                    print('\nEmail(s): ',row[2])

                    temp = userid
                    temp_cname = input('\nEnter new name: ')
                    cphone = input("\nEnter new phone (If there's more than 1, enter them seperated by a space): ")
                    cemail = input("\nEnter new email (If there's more than 1, enter them seperated by a space): ")


                    
                    query = "DELETE FROM contacts WHERE uid={} and cname='{}'".format(str(temp),cname)
                    cursor.execute(query)
                    conn.commit()

                    query = """INSERT INTO contacts(uid,cname,cphone,cemail)
                            VALUES({},'{}','{}','{}')""".format(str(temp),temp_cname,cphone,cemail)
                    cursor.execute(query)

                    conn.commit()

                    print('\nContact updated!')

                else:
                    print(uname, "doesn't have any contacts.")

            else:
                print('\nExiting app...')
                break

            inpt = header_input()

        else:
            print("It's not a valid option. Try again!")
            
    except Error as e:
        print("Error:",e)
 
    finally:
        cursor.close()
        conn.close()

def header_input():
    print('\n\n\n************CONTACTS MANAGER************')
    print('\n\nOPTIONS:')
    print('\nEnter (A) to Add a contact')
    print('\nEnter (R) to Remove a contact')
    print('\nEnter (E) to Edit a contact')
    print('\nEnter (L) to List all contacts')
    print('\nEnter (X) to Exit application \n')

    return input()


def add_contact():
    uname = input("\nEnter user name? ")
    cname = input("\nEnter contact name: ")
    cphone = input("\nEnter contact phone (If there's more than 1, enter them seperated by a space): ")
    cemail = input("\nEnter contact email (If there's more than 1, enter them seperated by a space): ")
    return uname, cname, cphone, cemail


def list_contact():
    uname = input("\nEnter whose contacts are to be displayed: ")
    return uname

def edit_contact():
    uname = input("\nEnter user name whose contact is to be edited/removed: ")
    cname = input("\nEnter name of the contact to be edited/removed: ")
    return uname,cname
    

if __name__ == '__main__':
    main()
