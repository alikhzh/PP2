from connect import connect


def show_all():
    conn = connect()
    if conn is None:
        return

    cur = conn.cursor()
    cur.execute("SELECT * FROM contacts ORDER BY id;")
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def search():
    pattern = input("Enter search pattern: ")
    conn = connect()
    if conn is None:
        return

    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s);", (pattern,))
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def add_or_update():
    name = input("Name: ")
    phone = input("Phone: ")

    conn = connect()
    if conn is None:
        return

    cur = conn.cursor()

    cur.execute("CALL upsert_contact(%s,%s);", (name, phone))

    conn.commit()

    cur.close()
    conn.close()

    print("Done!")


def delete_contact():
    value = input("Enter name or phone to delete: ")

    conn = connect()
    if conn is None:
        return

    cur = conn.cursor()

    cur.execute("CALL delete_contact(%s);", (value,))

    conn.commit()

    cur.close()
    conn.close()

    print("Deleted if existed!")


def main():
    while True:
        print("\nPHONEBOOK MENU")
        print("1. Show all contacts")
        print("2. Search contacts")
        print("3. Add or update contact")
        print("4. Delete contact")
        print("5. Exit")

        choice = input("Choose: ")

        if choice == '1':
            show_all()

        elif choice == '2':
            search()

        elif choice == '3':
            add_or_update()

        elif choice == '4':
            delete_contact()

        elif choice == '5':
            print("Goodbye!")
            break

        else:
            print("Invalid option")


if __name__ == "__main__":
    main()
