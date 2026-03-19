import json

# Load contacts from file
def load_contacts():
    try:
        with open("contacts.json", "r") as file:
            return json.load(file)
    except:
        return []

# Save contacts to file
def save_contacts(contacts):
    with open("contacts.json", "w") as file:
        json.dump(contacts, file, indent=4)

contacts = load_contacts()

# Menu display
def show_menu():
    print("\n--- Contact Manager ---")
    print("1. Add Contact")
    print("2. View Contacts")
    print("3. Edit Contact")
    print("4. Delete Contact")
    print("5. Exit")

# Main loop
while True:
    show_menu()
    choice = input("Enter your choice: ")

    # ADD CONTACT
    if choice == "1":
        name = input("Enter name: ")
        phone = input("Enter phone: ")
        email = input("Enter email: ")

        if not name or not phone:
            print("Name and phone are required!")
            continue

        contact = {
            "name": name,
            "phone": phone,
            "email": email
        }

        contacts.append(contact)
        save_contacts(contacts)

        print("Contact added successfully!")

    # VIEW CONTACTS
    elif choice == "2":
        if not contacts:
            print("No contacts found.")
        else:
            print("\n--- Contact List ---")
            for i, contact in enumerate(contacts, start=1):
                print(f"{i}. Name: {contact['name']}, Phone: {contact['phone']}, Email: {contact['email']}")

    # EDIT CONTACT
    elif choice == "3":
        if not contacts:
            print("No contacts to edit.")
        else:
            print("\n--- Contact List ---")
            for i, contact in enumerate(contacts, start=1):
                print(f"{i}. {contact['name']}")

            try:
                num = int(input("Enter contact number to edit: "))
                if 1 <= num <= len(contacts):
                    contact = contacts[num - 1]

                    new_name = input("Enter new name (leave blank to keep same): ")
                    new_phone = input("Enter new phone (leave blank to keep same): ")
                    new_email = input("Enter new email (leave blank to keep same): ")

                    if new_name:
                        contact["name"] = new_name
                    if new_phone:
                        contact["phone"] = new_phone
                    if new_email:
                        contact["email"] = new_email

                    save_contacts(contacts)
                    print("Contact updated successfully!")
                else:
                    print("Invalid number.")
            except ValueError:
                print("Enter a valid number.")

    # DELETE CONTACT
    elif choice == "4":
        if not contacts:
            print("No contacts to delete.")
        else:
            print("\n--- Contact List ---")
            for i, contact in enumerate(contacts, start=1):
                print(f"{i}. {contact['name']}")

            try:
                num = int(input("Enter contact number to delete: "))
                if 1 <= num <= len(contacts):
                    deleted = contacts.pop(num - 1)
                    save_contacts(contacts)
                    print(f"{deleted['name']} deleted successfully!")
                else:
                    print("Invalid number.")
            except ValueError:
                print("Enter a valid number.")

    # EXIT
    elif choice == "5":
        print("Exiting...")
        break

    # INVALID INPUT
    else:
        print("Invalid choice. Try again.")