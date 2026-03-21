import json
import csv
from datetime import datetime

FILE_NAME = "contacts.json"


# -------- LOAD --------
def load_contacts():
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except:
        return []


# -------- SAVE --------
def save_contacts(contacts):
    with open(FILE_NAME, "w") as file:
        json.dump(contacts, file, indent=4)


# -------- MENU --------
def show_menu():
    print("\n===== Contact Manager =====")
    print("1. Add Contact")
    print("2. View Contacts")
    print("3. Edit Contact")
    print("4. Delete Contact")
    print("5. Search Contact")
    print("6. Sort Contacts")
    print("7. Mark Favorite")
    print("8. View Favorites")
    print("9. Export to CSV")
    print("10. Exit")


contacts = load_contacts()


# -------- MAIN LOOP --------
while True:
    show_menu()
    choice = input("Enter your choice: ")

    # ADD CONTACT
    if choice == "1":
        name = input("Name: ").strip()

        if not name:
            print("❌ Name cannot be empty")
            continue

        name = name.title()
        phone = input("Phone: ").strip()
        email = input("Email: ").strip()

        if not phone.isdigit() or len(phone) != 10:
            print("❌ Invalid phone number")
            continue

        if "@" not in email or "." not in email:
            print("❌ Invalid email")
            continue

        if any(c.get("phone") == phone for c in contacts):
            print("❌ Contact already exists")
            continue

        contact = {
            "name": name,
            "phone": phone,
            "email": email,
            "is_favorite": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
        }

        contacts.append(contact)
        save_contacts(contacts)
        print("✅ Contact added")

    # VIEW CONTACTS
    elif choice == "2":
        if not contacts:
            print("No contacts found")
        else:
            print(f"\nTotal Contacts: {len(contacts)}")
            print("\n--- Contact List ---")
            for i, c in enumerate(contacts, 1):
                fav = "⭐" if c.get("is_favorite") else ""
                print(f"{i}. {c['name']} {fav} | {c['phone']} | {c['email']}")

    # EDIT CONTACT
    elif choice == "3":
        if not contacts:
            print("No contacts to edit")
            continue

        for i, c in enumerate(contacts, 1):
            print(f"{i}. {c['name']}")

        try:
            idx = int(input("Select number: ")) - 1
            contact = contacts[idx]

            name = input("New name: ").strip() or contact["name"]
            phone = input("New phone: ").strip() or contact["phone"]
            email = input("New email: ").strip() or contact["email"]

            if not phone.isdigit() or len(phone) != 10:
                print("❌ Invalid phone")
                continue

            if "@" not in email or "." not in email:
                print("❌ Invalid email")
                continue

            contact["name"] = name.title()
            contact["phone"] = phone
            contact["email"] = email

            save_contacts(contacts)
            print("✅ Updated")

        except:
            print("Invalid input")

    # DELETE CONTACT
    elif choice == "4":
        if not contacts:
            print("No contacts to delete")
            continue

        for i, c in enumerate(contacts, 1):
            print(f"{i}. {c['name']}")

        try:
            idx = int(input("Select number: ")) - 1

            confirm = input("Are you sure? (y/n): ").lower()
            if confirm == "y":
                removed = contacts.pop(idx)
                save_contacts(contacts)
                print(f"🗑 Deleted {removed['name']}")
            else:
                print("Cancelled")

        except:
            print("Invalid input")

    # SEARCH CONTACT
    elif choice == "5":
        query = input("Search (name/phone/email): ").lower()
        results = [
            c for c in contacts
            if query in c["name"].lower()
            or query in c["phone"]
            or query in c["email"].lower()
        ]

        if results:
            print("\n--- Results ---")
            for c in results:
                print(f"\nName  : {c['name']}")
                print(f"Phone : {c['phone']}")
                print(f"Email : {c['email']}")
        else:
            print("No results found")

    # SORT CONTACTS
    elif choice == "6":
        contacts.sort(key=lambda x: x["name"].lower())
        save_contacts(contacts)
        print("✅ Contacts sorted")

    # MARK FAVORITE
    elif choice == "7":
        if not contacts:
            print("No contacts available")
            continue

        for i, c in enumerate(contacts, 1):
            print(f"{i}. {c['name']}")

        try:
            idx = int(input("Select number: ")) - 1
            contacts[idx]["is_favorite"] = True
            save_contacts(contacts)
            print("⭐ Marked as favorite")
        except:
            print("Invalid input")

    # VIEW FAVORITES
    elif choice == "8":
        favs = [c for c in contacts if c.get("is_favorite", False)]

        if not favs:
            print("No favorite contacts")
        else:
            print("\n--- Favorite Contacts ---")
            for c in favs:
                print(f"⭐ {c['name']} | {c['phone']}")

    # EXPORT CSV
    elif choice == "9":
        with open("contacts.csv", "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["name", "phone", "email"])
            writer.writeheader()
            writer.writerows(contacts)

        print("📁 Exported to contacts.csv")

    # EXIT
    elif choice == "10":
        print("Exiting...")
        break

    else:
        print("Invalid choice")