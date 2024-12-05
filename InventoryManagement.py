import csv
from RegularItems import RegularItem, PerishableItem

class InventoryManager:
    def __init__(self, file_path="inventory.csv"):
        self.file_path = file_path
        self.sections = {}
        self.load_inventory()

    def load_inventory(self):
        try:
            with open(self.file_path, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                if reader.fieldnames is None or 'section_name' not in reader.fieldnames:
                    self.initialize_csv()
                    return

                for row in reader:
                    section_name = row['section_name']
                    item_name = row['item_name']
                    quantity = int(row['quantity'])
                    expiry_date = row['expiry_date']

                    if section_name not in self.sections:
                        self.sections[section_name] = []

                    if expiry_date:
                        item = PerishableItem(item_name, quantity, expiry_date)
                    else:
                        item = RegularItem(item_name, quantity)

                    self.sections[section_name].append(item)
        except FileNotFoundError:
            self.initialize_csv()

    def initialize_csv(self):
        headers = ['section_name', 'item_name', 'quantity', 'expiry_date']
        with open(self.file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()

    def save_inventory(self):
        with open(self.file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['section_name', 'item_name', 'quantity', 'expiry_date'])
            for section, items in self.sections.items():
                for item in items:
                    expiry_date = item.expiry_date if isinstance(item, PerishableItem) else ''
                    writer.writerow([section, item.name, item.quantity, expiry_date])

    def add_section(self, section):
        if section.name not in self.sections:
            self.sections[section.name] = []
        else:
            raise ValueError(f"Section {section.name} already exists")
        self.save_inventory()

    def add_item(self, section_name, item):
        if section_name in self.sections:
            self.sections[section_name].append(item)
        else:
            raise ValueError(f"Section {section_name} not found")
        self.save_inventory()

    def add_stock(self, section_name, item_name, amount):
        if section_name in self.sections:
            for item in self.sections[section_name]:
                if item.name == item_name:
                    item.quantity += amount
                    self.save_inventory()
                    return
            raise ValueError(f"Item {item_name} not found in section {section_name}")
        else:
            raise ValueError(f"Section {section_name} not found")

    def remove_stock(self, section_name, item_name, amount):
        if section_name in self.sections:
            for item in self.sections[section_name]:
                if item.name == item_name:
                    if item.quantity >= amount:
                        item.quantity -= amount
                        self.save_inventory()
                        return
                    else:
                        raise ValueError("Not enough stock available")
            raise ValueError(f"Item {item_name} not found in section {section_name}")
        else:
            raise ValueError(f"Section {section_name} not found")

    def move_stock(self, from_section_name, to_section_name, item_name, amount):
        if from_section_name in self.sections and to_section_name in self.sections:
            for item in self.sections[from_section_name]:
                if item.name == item_name:
                    if item.quantity >= amount:
                        item.quantity -= amount
                        self.add_item(to_section_name, RegularItem(item_name, amount) if not isinstance(item, PerishableItem) else PerishableItem(item_name, amount, item.expiry_date))
                        self.save_inventory()
                        return
                    else:
                        raise ValueError("Not enough stock available")
            raise ValueError(f"Item {item_name} not found in section {from_section_name}")
        else:
            raise ValueError(f"Section {from_section_name} or {to_section_name} not found")

    def get_inventory(self):
        inventory = []
        for section, items in self.sections.items():
            for item in items:
                inventory.append(f"{item.name}: {item.quantity} in {section}")
        return inventory
