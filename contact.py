import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3

class ContactBookApp:
    def __init__(self, master):
        self.master = master
        master.title("Modern Contact Book")

        self.create_database()

        self.name_label = tk.Label(master, text="Name:")
        self.name_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.name_entry = tk.Entry(master)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        self.phone_label = tk.Label(master, text="Phone:")
        self.phone_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.phone_entry = tk.Entry(master)
        self.phone_entry.grid(row=1, column=1, padx=10, pady=5)

        self.email_label = tk.Label(master, text="Email:")
        self.email_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.email_entry = tk.Entry(master)
        self.email_entry.grid(row=2, column=1, padx=10, pady=5)

        self.address_label = tk.Label(master, text="Address:")
        self.address_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.address_entry = tk.Entry(master)
        self.address_entry.grid(row=3, column=1, padx=10, pady=5)

        self.add_button = tk.Button(master, text="Add Contact", command=self.add_contact)
        self.add_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.view_button = tk.Button(master, text="View Contacts", command=self.view_contacts)
        self.view_button.grid(row=5, column=0, columnspan=2, pady=5)

        self.search_button = tk.Button(master, text="Search Contact", command=self.search_contact)
        self.search_button.grid(row=6, column=0, columnspan=2, pady=5)

        self.delete_button = tk.Button(master, text="Delete Contact", command=self.delete_contact)
        self.delete_button.grid(row=7, column=0, columnspan=2, pady=5)

        self.contacts_listbox = tk.Listbox(master, width=50, height=15)
        self.contacts_listbox.grid(row=8, column=0, columnspan=2, padx=10, pady=5)

    def create_database(self):
        self.conn = sqlite3.connect("contacts.db")
        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS contacts (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            phone TEXT,
                            email TEXT,
                            address TEXT
                            )""")
        self.conn.commit()

    def add_contact(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        address = self.address_entry.get()

        if name.strip() == "":
            messagebox.showerror("Error", "Name cannot be empty.")
            return

        self.c.execute("INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)", (name, phone, email, address))
        self.conn.commit()

        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)

    def view_contacts(self):
        self.contacts_listbox.delete(0, tk.END)
        self.c.execute("SELECT * FROM contacts")
        contacts = self.c.fetchall()
        for contact in contacts:
            self.contacts_listbox.insert(tk.END, f"{contact[1]} - {contact[2]}")

    def search_contact(self):
        query = simpledialog.askstring("Search Contact", "Enter name or phone number:")
        if query:
            self.contacts_listbox.delete(0, tk.END)
            self.c.execute("SELECT * FROM contacts WHERE name LIKE ? OR phone LIKE ?", ('%' + query + '%', '%' + query + '%'))
            contacts = self.c.fetchall()
            for contact in contacts:
                self.contacts_listbox.insert(tk.END, f"{contact[1]} - {contact[2]}")

    def delete_contact(self):
        selected_contact = self.contacts_listbox.curselection()
        if selected_contact:
            confirmation = messagebox.askyesno("Delete Contact", "Are you sure you want to delete this contact?")
            if confirmation:
                contact_index = selected_contact[0]
                contact_name = self.contacts_listbox.get(contact_index).split(" - ")[0]
                self.c.execute("DELETE FROM contacts WHERE name=?", (contact_name,))
                self.conn.commit()
                self.contacts_listbox.delete(contact_index)
                messagebox.showinfo("Delete Contact", "Contact deleted successfully.")
        else:
            messagebox.showerror("Error", "Please select a contact to delete.")

def main():
    root = tk.Tk()
    app = ContactBookApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
