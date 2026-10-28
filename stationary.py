import tkinter as tk
from tkinter import ttk, messagebox
import os

class RestrauntOrderManageMent:
    def __init__(self, root):
        self.root = root
        self.root.title("Stationary Billing System")
        self.root.geometry("800x600")
        self.root.resizable(False, False) # Keep it locked so layout doesn't break
        
        self.menu_items = {
            "PENCIL PACK OF 10": 1,
            "GEL PEN PACK": 2,
            "RULER": 0.2,
            "2 LINED NOTEBOOK": 0.5,
            "MARKERS": 0.75,
            "5 ERASERS AND SHARPENERS": 1,
        }
        self.exchange_rate = 95
        
        # 1. Setup the Background Canvas
        self.setup_background(root)

    def setup_background(self, root):
        bg_width, bg_height = 800, 600
        
        # Create canvas that fills the whole screen
        self.canvas = tk.Canvas(root, width=bg_width, height=bg_height, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # The exact image path you provided
        img_path = "/Users/Amit/Desktop/Python/Tkinter/RESTRAUNTMANAGEMENTSYSTEM/school-stationery-isolated-white-background.jpg"
        
        # Safe-check if the file actually exists on your Mac
        if os.path.exists(img_path):
            try:
                original_image = tk.PhotoImage(file=img_path)
                
                # Prevent dividing by zero if image matches or is smaller than 800x600
                sub_x = max(1, original_image.width() // bg_width)
                sub_y = max(1, original_image.height() // bg_height)
                
                self.background_image = original_image.subsample(sub_x, sub_y)
                self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)
            except Exception as e:
                print(f"Error rendering image: {e}")
        else:
            # Fallback color if the file path is broken
            print(f"Image NOT found at path: {img_path}. Using fallback background color.")
            self.canvas.config(bg="#f0f4f8") 

        # 2. Build the UI Frame inside the Canvas so it layers perfectly on top
        self.build_ui()

    def build_ui(self):
        # Create a frame with a slightly transparent or flat color background
        # 'style' ensures it blends nice or stays readable over the image
        frame = ttk.Frame(self.root)
        
        # This attaches the frame directly to the middle of the Canvas space!
        self.canvas.create_window(400, 300, window=frame, anchor=tk.CENTER)
        
        ttk.Label(frame, text="Stationary Order Management", font=("Arial", 20, "bold")).grid(row=0, columnspan=3, padx=10, pady=10)
        
        self.menu_labels = {}
        self.menu_quantities = {}
        
        for i, (item, price) in enumerate(self.menu_items.items(), start=1):
            label = ttk.Label(frame, text=f"{item} (${price})", font=("Arial", 12))
            label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
            self.menu_labels[item] = label
            
            quantity_entry = ttk.Entry(frame, width=5)
            quantity_entry.grid(row=i, column=1, padx=10, pady=5)
            self.menu_quantities[item] = quantity_entry
            
        self.currency_var = tk.StringVar()
        ttk.Label(frame, text="Currency:", font=("Arial", 12)).grid(row=len(self.menu_items) + 1, column=0, padx=10, pady=5)
        
        currency_dropdown = ttk.Combobox(frame, textvariable=self.currency_var, state="readonly", width=18, values=("USD", "INR"))
        currency_dropdown.grid(row=len(self.menu_items) + 1, column=1, padx=10, pady=5)
        currency_dropdown.current(0) 
        
        self.currency_var.trace_add("write", self.update_menu_prices)
        
        order_button = ttk.Button(frame, text="Place Order", command=self.place_order)
        order_button.grid(row=len(self.menu_items) + 2, columnspan=3, padx=10, pady=10)

    def update_menu_prices(self, *args):
        currency = self.currency_var.get()
        symbol = "₹" if currency == "INR" else "$"
        rate = self.exchange_rate if currency == "INR" else 1
        
        for item, label in self.menu_labels.items():
            price = self.menu_items[item] * rate
            label.config(text=f"{item} ({symbol}{price}): ")

    def place_order(self):
        total_cost = 0
        order_summary = "Order Summary:\n"
        currency = self.currency_var.get()
        symbol = "₹" if currency == "INR" else "$"
        rate = self.exchange_rate if currency == "INR" else 1
        
        for item, entry in self.menu_quantities.items():
            quantity = entry.get()
            if quantity.isdigit():
                quantity = int(quantity)
                price = self.menu_items[item] * rate
                cost = quantity * price
                total_cost += cost
                if quantity > 0:
                    order_summary += f"{item}: {quantity} x {symbol}{price} = {symbol}{cost}\n"
                    
        if total_cost > 0:
            order_summary += f"\nTotal Cost: {symbol}{total_cost}"
            messagebox.showinfo("Order Placed", order_summary)
        else:
            messagebox.showerror("Error", "Please order at least one item.")

if __name__ == "__main__":
    root = tk.Tk()
    app = RestrauntOrderManageMent(root)
    root.mainloop()
