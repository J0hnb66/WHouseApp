import tkinter as tk
from tkinter import messagebox, simpledialog

from InventoryManagement import InventoryManager
from Sections import InventorySection
from RegularItems import RegularItem, PerishableItem


class WarehouseApp(tk.Tk):
    def __init__(self, inventory_manager):
        super().__init__()
        self.inventory_manager = inventory_manager
        self.title("Warehouse Management System")
        self.configure(bg="#f2f2f2")

        self.create_widgets()
        self.update_section_menu()
        self.update_inventory()

    def create_widgets(self):
        # Title Label
        title_label = tk.Label(self, text="Warehouse Management System", font=("Helvetica", 16, "bold"), bg="#f2f2f2")
        title_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Section Frame
        section_frame = tk.Frame(self, bg="#ffffff", bd=2, relief="groove", padx=10, pady=10)
        section_frame.grid(row=1, column=0, columnspan=3, pady=10, padx=10, sticky="ew")

        tk.Label(section_frame, text="Select Section", font=("Helvetica", 12), bg="#ffffff").grid(row=0, column=0,
                                                                                                  sticky="w")
        self.section_var = tk.StringVar(self)
        self.section_menu = tk.OptionMenu(section_frame, self.section_var, *self.inventory_manager.sections.keys())
        self.section_menu.grid(row=0, column=1, sticky="ew")

        # Add Section button
        self.add_section_button = tk.Button(section_frame, text="Add New Section", command=self.add_section,
                                            bg="#4CAF50", fg="green", font=("Helvetica", 12))
        self.add_section_button.grid(row=0, column=2, sticky="ew")

        # Item Frame
        item_frame = tk.Frame(self, bg="#ffffff", bd=2, relief="groove", padx=10, pady=10)
        item_frame.grid(row=2, column=0, columnspan=3, pady=10, padx=10, sticky="ew")

        tk.Label(item_frame, text="Item Name", font=("Helvetica", 12), bg="#ffffff").grid(row=0, column=0, sticky="w")
        self.add_item_name = tk.Entry(item_frame)
        self.add_item_name.grid(row=0, column=1, sticky="ew")

        tk.Label(item_frame, text="Item Quantity", font=("Helvetica", 12), bg="#ffffff").grid(row=1, column=0,
                                                                                              sticky="w")
        self.add_item_quantity = tk.Entry(item_frame)
        self.add_item_quantity.grid(row=1, column=1, sticky="ew")

        tk.Label(item_frame, text="Expiry Date (Optional, DD/MM/YYYY)", font=("Helvetica", 12), bg="#ffffff").grid(
            row=2, column=0, sticky="w")
        self.add_item_expiry = tk.Entry(item_frame)
        self.add_item_expiry.grid(row=2, column=1, sticky="ew")

        self.add_item_button = tk.Button(item_frame, text="Add New Item", command=self.add_item, bg="#2196F3",
                                         fg="green", font=("Helvetica", 12))
        self.add_item_button.grid(row=3, column=0, columnspan=2, pady=5, sticky="ew")

        # Stock Management Frame
        stock_frame = tk.Frame(self, bg="#ffffff", bd=2, relief="groove", padx=10, pady=10)
        stock_frame.grid(row=3, column=0, columnspan=3, pady=10, padx=10, sticky="ew")

        tk.Label(stock_frame, text="Stock Amount", font=("Helvetica", 12), bg="#ffffff").grid(row=0, column=0,
                                                                                              sticky="w")
        self.stock_amount = tk.Entry(stock_frame)
        self.stock_amount.grid(row=0, column=1, sticky="ew")

        self.add_stock_button = tk.Button(stock_frame, text="Increase Stock", command=self.add_stock, bg="#FF9800",
                                          fg="green", font=("Helvetica", 12))
        self.add_stock_button.grid(row=1, column=0, pady=5, sticky="ew")

        self.remove_stock_button = tk.Button(stock_frame, text="Decrease Stock", command=self.remove_stock,
                                             bg="#F44336", fg="green", font=("Helvetica", 12))
        self.remove_stock_button.grid(row=1, column=1, pady=5, sticky="ew")

        # Moving Stock Frame
        move_frame = tk.Frame(self, bg="#ffffff", bd=2, relief="groove", padx=10, pady=10)
        move_frame.grid(row=4, column=0, columnspan=3, pady=10, padx=10, sticky="ew")

        tk.Label(move_frame, text="Source Section", font=("Helvetica", 12), bg="#ffffff").grid(row=0, column=0,
                                                                                               sticky="w")
        self.from_section_var = tk.StringVar(self)
        self.from_section_menu = tk.OptionMenu(move_frame, self.from_section_var,
                                               *self.inventory_manager.sections.keys())
        self.from_section_menu.grid(row=0, column=1, sticky="ew")

        tk.Label(move_frame, text="Destination Section", font=("Helvetica", 12), bg="#ffffff").grid(row=1, column=0,
                                                                                                    sticky="w")
        self.move_to_var = tk.StringVar(self)
        self.move_to_section = tk.OptionMenu(move_frame, self.move_to_var, *self.inventory_manager.sections.keys())
        self.move_to_section.grid(row=1, column=1, sticky="ew")

        tk.Label(move_frame, text="Item to Move", font=("Helvetica", 12), bg="#ffffff").grid(row=2, column=0,
                                                                                             sticky="w")
        self.move_item_name = tk.Entry(move_frame)
        self.move_item_name.grid(row=2, column=1, sticky="ew")

        tk.Label(move_frame, text="Quantity to Move", font=("Helvetica", 12), bg="#ffffff").grid(row=3, column=0,
                                                                                                 sticky="w")
        self.move_amount = tk.Entry(move_frame)
        self.move_amount.grid(row=3, column=1, sticky="ew")

        self.confirm_move_button = tk.Button(move_frame, text="Confirm Move", command=self.move_stock, bg="#9C27B0",
                                             fg="green", font=("Helvetica", 12))
        self.confirm_move_button.grid(row=4, column=0, columnspan=2, pady=5, sticky="ew")

        # Inventory display
        self.inventory_text = tk.Text(self, height=15, width=50, bg="#e0e0e0")
        self.inventory_text.grid(row=5, column=0, columnspan=3, pady=10, padx=10, sticky="ew")

    def add_section(self):
        section_name = simpledialog.askstring("Input", "Enter the name of the new section:")
        if section_name:
            try:
                new_section = InventorySection(section_name)
                self.inventory_manager.add_section(new_section)
                self.update_section_menu()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def update_section_menu(self):
        menu = self.section_menu["menu"]
        menu.delete(0, "end")
        for section in self.inventory_manager.sections.keys():
            menu.add_command(label=section, command=tk._setit(self.section_var, section))

        from_menu = self.from_section_menu["menu"]
        from_menu.delete(0, "end")
        for section in self.inventory_manager.sections.keys():
            from_menu.add_command(label=section, command=tk._setit(self.from_section_var, section))

        move_menu = self.move_to_section["menu"]
        move_menu.delete(0, "end")
        for section in self.inventory_manager.sections.keys():
            move_menu.add_command(label=section, command=tk._setit(self.move_to_var, section))

    def add_item(self):
        section_name = self.section_var.get()
        name = self.add_item_name.get()
        quantity = self.add_item_quantity.get()
        if section_name and name and quantity.isdigit() and int(quantity) >= 0:
            quantity = int(quantity)
            if self.add_item_expiry.get():
                item = PerishableItem(name, quantity, self.add_item_expiry.get())
            else:
                item = RegularItem(name, quantity)
            self.inventory_manager.add_item(section_name, item)
            self.update_inventory()
        else:
            messagebox.showerror("Error",
                                 "Please fill out all fields correctly and ensure quantity is a positive integer.")

    def add_stock(self):
        section_name = self.section_var.get()
        name = self.add_item_name.get()
        amount = self.stock_amount.get()
        if section_name and name and amount.isdigit() and int(amount) >= 0:
            amount = int(amount)
            try:
                self.inventory_manager.add_stock(section_name, name, amount)
                self.update_inventory()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Please ensure all fields are correctly filled.")

    def remove_stock(self):
        section_name = self.section_var.get()
        name = self.add_item_name.get()
        amount = self.stock_amount.get()
        if section_name and name and amount.isdigit() and int(amount) >= 0:
            amount = int(amount)
            try:
                self.inventory_manager.remove_stock(section_name, name, amount)
                self.update_inventory()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Please ensure all fields are correctly filled.")

    def move_stock(self):
        from_section_name = self.from_section_var.get()
        to_section_name = self.move_to_var.get()
        item_name = self.move_item_name.get()
        amount = self.move_amount.get()
        if from_section_name and to_section_name and item_name and amount.isdigit() and int(amount) >= 0:
            amount = int(amount)
            try:
                self.inventory_manager.move_stock(from_section_name, to_section_name, item_name, amount)
                self.update_inventory()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Please ensure all fields are correctly filled.")

    def update_inventory(self):
        self.inventory_text.delete(1.0, tk.END)
        inventory = self.inventory_manager.get_inventory()
        for item in inventory:
            self.inventory_text.insert(tk.END, item + '\n')

# Initialise and run the application
if __name__ == "__main__":
    inventory_manager = InventoryManager()

    # Check if the section exists before adding
    if "Electronics" not in inventory_manager.sections:
        inventory_manager.add_section(InventorySection("Electronics"))
    if "Automotive" not in inventory_manager.sections:
        inventory_manager.add_section(InventorySection("Automotive"))

    app = WarehouseApp(inventory_manager)
    app.mainloop()
