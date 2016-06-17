
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
                uname, cname, cphone, cemail = add_contact()

                query = "SELECT uid FROM users " \
                        "WHERE uname=%s"
                cursor.execute(query, (uname,))
                userid = cursor.fetchone()
                
                
                if userid != None: #Directly creates contact when the user already exists
                    userid = int(userid[0])
                
                    query = "INSERT INTO contacts(uid,cname,cphone,cemail) " \
                            "VALUES(%s,%s,%s,%s)"
                    args = (userid,cname,cphone,cemail)

                    cursor.execute(query,args)

                    conn.commit()

                    print('\nContact added.')

                else: #First creates the user and then creates contact when user doesn't exist
                    query = "INSERT INTO users(uname) " \
                            "VALUES(%s)"
                    
                    cursor.execute(query,(uname,))

                    conn.commit()

                    query = "SELECT uid FROM users " \
                        "WHERE uname=%s"
                    cursor.execute(query, (uname,))
                    userid = cursor.fetchone()

                    userid = int(userid[0])

                    query = "INSERT INTO contacts(uid,cname,cphone,cemail) " \
                            "VALUES(%s,%s,%s,%s)"
                    args = (userid,cname,cphone,cemail)

                    cursor.execute(query,args)

                    conn.commit()

                    print('\nContact added.')

            #needs changes in WHERE clause
            elif inpt == 'r' or inpt == 'R':
                uid,cname = edit_contact()
                query = "DELETE FROM contacts WHERE cname = %s"

                cursor.execute(query, (cname,))
                conn.commit()

                print('\nContact removed.')

            elif inpt == 'l' or inpt == 'L':
                uname = list_contact()

                query = "SELECT uid FROM users " \
                        "WHERE uname=%s"
                cursor.execute(query, (uname,))
                userid = cursor.fetchone()
                
                if userid != None: 
                    userid = int(userid[0])
                    #print(userid)
                    print(uname+"'s contacts:")
                
                    query = """SELECT cname,cphone,cemail
                            FROM contacts
                            WHERE uid=%s
                            ORDER BY cname ASC"""
                    cursor.execute(query,(userid,))
                    rows = cursor.fetchall()
                    print('hi')

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

                else:
                    print(uname, "doesn't have any contacts.")

            elif inpt == 'e' or inpt == 'E':
                uname,cname = edit_contact()
                query = """SELECT uid FROM users
                        WHERE uname=%s"""
                cursor.execute(query, (uname,))
                userid = cursor.fetchone()

                if userid != None: 
                    userid = int(userid[0])
                
                    query = """SELECT cname, cphone, cemail FROM contacts
                            WHERE uid = %s and cname=%s"""
                    cursor.execute(query, (userid,cname,))
                    row = cursor.fetchone()

                    print('Current Contact:', row[0],row[1],row[2])

                    temp = userid
                    print(temp)
                    temp_cname = input('Enter new name: ')
                    cphone = input('Enter new phone: ')
                    cemail = input('Enter new email: ')


                    print(temp_cname,cphone,cemail,str(temp),cname)
                    
##                    query = """UPDATE contacts
##                            SET cname={}, cphone={}, cemail={}
##                            WHERE uid={} and cname={}""".format(temp_cname,cphone,cemail,str(temp),cname)
##                
##                    cursor.execute(query)

                    query = "DELETE FROM contacts WHERE uid=%s and cname=%s"
                    cursor.execute(query,(str(temp),cname))
                    conn.commit()

                    query = """INSERT INTO contacts(uid,cname,cphone,cemail)
                            VALUES(%s,%s,%s,%s)"""
                    cursor.execute(query,(str(temp),temp_cname,cphone,cemail))

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
    uname = input("Who's the user?")
    cname = input("Enter contact name: ")
    cphone = input("Enter contact phone(s) (If there's more than 1 enter them seperated by a space): ")
    cemail = input("Enter contact email(s) (If there's more than 1 enter them seperated by a space): ")
    return uname, cname, cphone, cemail


def list_contact():
    uname = input("Enter whose contacts are to be displayed")
    return uname

def edit_contact():
    uname = input("Enter user name whose contact is to be edited: ")
    cname = input("Enter name of the contact to be edited: ")
    return uname,cname
    

if __name__ == '__main__':
    main()
