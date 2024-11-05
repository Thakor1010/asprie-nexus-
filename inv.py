import sqlite3
from tkinter import *
from tkinter import messagebox

# Create database connection
conn = sqlite3.connect('inventory.db')
c = conn.cursor()

# Create Product table
c.execute('''CREATE TABLE IF NOT EXISTS Product (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT NOT NULL,
                supplier_name TEXT NOT NULL,
                stock_level INTEGER NOT NULL,
                reorder_point INTEGER NOT NULL
            )''')
conn.commit()

# Product class to represent products
class Product:
    def __init__(self, name, supplier, stock, reorder_point):
        self.name = name
        self.supplier = supplier
        self.stock = stock
        self.reorder_point = reorder_point

# Inventory class to handle inventory operations
class Inventory:
    def __init__(self):
        pass

    # Add product to inventory
    def add_product(self, product):
        with conn:
            c.execute("INSERT INTO Product (product_name, supplier_name, stock_level, reorder_point) VALUES (?, ?, ?, ?)",
                      (product.name, product.supplier, product.stock, product.reorder_point))
            messagebox.showinfo("Success", f"Product '{product.name}' added to inventory", icon='info')

    # Update stock levels
    def update_stock(self, product_id, stock_level):
        with conn:
            c.execute("UPDATE Product SET stock_level = ? WHERE product_id = ?", (stock_level, product_id))
            messagebox.showinfo("Success", f"Stock updated for product ID {product_id}")

    # View all products
    def view_inventory(self):
        c.execute("SELECT * FROM Product")
        products = c.fetchall()
        return products

    # Generate reports on inventory and reorder points
    def generate_report(self):
        c.execute("SELECT product_name, stock_level, reorder_point FROM Product")
        report_data = c.fetchall()
        return report_data

    # Place order when stock is below reorder point
    def place_order(self):
        c.execute("SELECT product_name FROM Product WHERE stock_level < reorder_point")
        low_stock_products = c.fetchall()
        if low_stock_products:
            order_list = "\n".join([f"{product[0]}" for product in low_stock_products])
            messagebox.showwarning("Reorder Alert", f"Place order for the following products:\n{order_list}")
        else:
            messagebox.showinfo("Inventory OK", "All products have sufficient stock.")

# GUI application using Tkinter
class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("500x400")
        self.root.configure(bg='#f2f2f2')

        # Inventory object
        self.inventory = Inventory()

        # Labels for product entry
        Label(root, text="Product Name", font=('Arial', 10, 'bold'), bg='#f2f2f2').grid(row=0, column=0)
        self.product_name_entry = Entry(root, width=30)
        self.product_name_entry.grid(row=0, column=1, padx=10, pady=5)

        Label(root, text="Supplier Name", font=('Arial', 10, 'bold'), bg='#f2f2f2').grid(row=1, column=0)
        self.supplier_name_entry = Entry(root, width=30)
        self.supplier_name_entry.grid(row=1, column=1, padx=10, pady=5)

        Label(root, text="Stock Level", font=('Arial', 10, 'bold'), bg='#f2f2f2').grid(row=2, column=0)
        self.stock_entry = Entry(root, width=30)
        self.stock_entry.grid(row=2, column=1, padx=10, pady=5)

        Label(root, text="Reorder Point", font=('Arial', 10, 'bold'), bg='#f2f2f2').grid(row=3, column=0)
        self.reorder_point_entry = Entry(root, width=30)
        self.reorder_point_entry.grid(row=3, column=1, padx=10, pady=5)

        # Buttons for adding product
        Button(root, text="Add Product", command=self.add_product, bg='#4CAF50', fg='white', font=('Arial', 10, 'bold')).grid(row=4, column=1, pady=5)

        # Labels for updating stock
        Label(root, text="Update Stock (Product ID)", font=('Arial', 10, 'bold'), bg='#f2f2f2').grid(row=5, column=0)
        self.product_id_entry = Entry(root, width=30)
        self.product_id_entry.grid(row=5, column=1, padx=10, pady=5)

        Label(root, text="New Stock Level", font=('Arial', 10, 'bold'), bg='#f2f2f2').grid(row=6, column=0)
        self.new_stock_entry = Entry(root, width=30)
        self.new_stock_entry.grid(row=6, column=1, padx=10, pady=5)

        # Buttons for updating stock
        Button(root, text="Update Stock", command=self.update_stock, bg='#4CAF50', fg='white', font=('Arial', 10, 'bold')).grid(row=7, column=1, pady=5)

        # Buttons for viewing inventory and generating reports
        Button(root, text="View Inventory", command=self.view_inventory, bg='#008CBA', fg='white', font=('Arial', 10, 'bold')).grid(row=8, column=1, pady=5)
        Button(root, text="Generate Report", command=self.generate_report, bg='#FF9800', fg='white', font=('Arial', 10, 'bold')).grid(row=9, column=1, pady=5)
        Button(root, text="Place Order", command=self.place_order, bg='#F44336', fg='white', font=('Arial', 10, 'bold')).grid(row=10, column=1, pady=5)

    # Add product handler
    def add_product(self):
        name = self.product_name_entry.get()
        supplier = self.supplier_name_entry.get()
        stock = self.stock_entry.get()
        reorder_point = self.reorder_point_entry.get()

        # Validate that stock and reorder point are integers
        if not stock.isdigit() or not reorder_point.isdigit():
            messagebox.showerror("Invalid Input", "Stock Level and Reorder Point must be numeric values.")
            return

        stock = int(stock)
        reorder_point = int(reorder_point)

        new_product = Product(name, supplier, stock, reorder_point)
        self.inventory.add_product(new_product)

    # Update stock handler
    def update_stock(self):
        product_id = self.product_id_entry.get()
        new_stock = self.new_stock_entry.get()

        # Validate that product_id and new_stock are integers
        if not product_id.isdigit() or not new_stock.isdigit():
            messagebox.showerror("Invalid Input", "Product ID and Stock Level must be numeric values.")
            return

        product_id = int(product_id)
        new_stock = int(new_stock)
        self.inventory.update_stock(product_id, new_stock)

    # View inventory handler
    def view_inventory(self):
        products = self.inventory.view_inventory()
        inventory_window = Toplevel(self.root)
        inventory_window.title("Inventory")
        inventory_window.configure(bg='#f2f2f2')
        for i, product in enumerate(products):
            Label(inventory_window, text=f"ID: {product[0]}, Name: {product[1]}, Stock: {product[3]}", 
                  bg='#f2f2f2', fg='black').grid(row=i, column=0, padx=10, pady=5)

    # Generate report handler
    def generate_report(self):
        report = self.inventory.generate_report()
        report_window = Toplevel(self.root)
        report_window.title("Inventory Report")
        report_window.configure(bg='#f2f2f2')
        for i, item in enumerate(report):
            Label(report_window, text=f"Product: {item[0]}, Stock: {item[1]}, Reorder Point: {item[2]}",
                  bg='#f2f2f2', fg='black').grid(row=i, column=0, padx=10, pady=5)

    # Place order handler
    def place_order(self):
        self.inventory.place_order()

# Main application loop
if __name__ == "__main__":
    root = Tk()
    app = InventoryApp(root)
    root.mainloop()
