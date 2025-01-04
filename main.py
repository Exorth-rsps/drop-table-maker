import sys
import os
import re
import tkinter as tk
from tkinter import ttk
from tkinter import IntVar

class Application(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Exorth - Drop Table Maker by Pixel - modified by Eikenb00m")

        # Parse the items from Items.kt
        self.item_names = self.parse_items()

        # Create widgets for controls (Total Slots, Add Item, Generate)
        controls_frame = ttk.Frame(self.master)
        controls_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

        ttk.Label(controls_frame, text="Total Slots").grid(row=0, column=0, sticky="w", padx=5)
        self.total_slots = ttk.Combobox(controls_frame, values=["256", "1", "8", "32", "128", "256", "512", "1024", "2048", "4096", "10240"], width=10)
        self.total_slots.set("256")
        self.total_slots.grid(row=0, column=1, padx=5)

        self.add_item = ttk.Button(controls_frame, text="Add Item", command=self.add_item_row)
        self.add_item.grid(row=0, column=2, padx=5)

        self.generate = ttk.Button(controls_frame, text="Generate", command=self.generate_code)
        self.generate.grid(row=0, column=3, padx=5)

        # Create a canvas for the item list
        self.canvas = tk.Canvas(self.master, width=727, height=350, bg='#999999', highlightthickness=0)
        self.canvas.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

        # Create a vertical scrollbar and associate it with the canvas
        self.scrollbar = tk.Scrollbar(self.master, orient="vertical", command=self.canvas.yview)
        self.scrollbar.grid(row=1, column=1, sticky='ns')
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create a frame within the canvas to hold other widgets
        self.inner_frame = ttk.Frame(self.canvas, borderwidth=2, relief="solid", width=690)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor='nw')

        # Configure the canvas to update the scroll region as the size of the inner_frame changes
        self.inner_frame.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Text box to display the generated code
        self.output_text = tk.Text(self.master, wrap="word", height=10, bg="white", fg="black", state="normal")
        self.output_text.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)
        self.output_text.insert("1.0", "Generated code will appear here...")
        self.output_text.configure(state="disabled")  # Make read-only by default

        # Configure row/column weights for resizing
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self.items = []
        for _ in range(1):  # Add items by default
            self.add_item_row()

    def parse_items(self):
        """Parse item names from Items.kt."""
        items_file_path = "Items.kt"  # Path to Items.kt
        item_names = []
        try:
            with open(items_file_path, 'r') as f:
                content = f.read()
                # Extract item names using regex
                item_names = re.findall(r"const val (\w+)\s*=", content)
        except FileNotFoundError:
            print("Items.kt not found. Ensure it is in the same directory as this script.")
        return item_names if item_names else ["BONES"]

    def add_item_row(self):
        row_num = len(self.items) + 1
        frame = ttk.Frame(self.inner_frame)
        frame.grid(row=row_num, columnspan=4)

        ttk.Label(frame, text="Item Name").grid(row=row_num, column=0)

        name_entry = ttk.Combobox(frame, values=self.item_names)
        name_entry.set("BONES")  # Set the default value
        name_entry.grid(row=row_num, column=1)

        def update_combobox(event):
            current_text = name_entry.get()
            filtered_items = [item for item in self.item_names if current_text.lower() in item.lower()]
            name_entry['values'] = filtered_items

        name_entry.bind('<KeyRelease>', update_combobox)

        ttk.Label(frame, text="Quantity").grid(row=row_num, column=2)
        quantity_entry = ttk.Entry(frame)
        quantity_entry.insert(0, "1")  # Set the default value
        quantity_entry.grid(row=row_num, column=3)

        probability_entry = ttk.Combobox(frame, values=["1/8", "1/32", "1/128", "1/256", "1/512", "1/5000", "1/10000"])
        probability_entry.set("1/28")  # Set the default value
        guaranteed = IntVar()
        chk = ttk.Checkbutton(frame, variable=guaranteed)
        ttk.Label(frame, text="Guaranteed Drop").grid(row=row_num, column=6)
        chk.grid(row=row_num, column=7)

        if not guaranteed.get():
            ttk.Label(frame, text="Probability").grid(row=row_num, column=4)
            probability_entry.grid(row=row_num, column=5)

        remove_button = ttk.Button(frame, text=" x ", width=2, command=lambda: self.remove_item((name_entry, quantity_entry, probability_entry, guaranteed, frame)))
        remove_button.grid(row=row_num, column=8)

        self.items.append((name_entry, quantity_entry, probability_entry, guaranteed, frame))

    def remove_item(self, item):
        self.items.remove(item)
        item[-1].destroy()

    def calculate_slots(self, probability):
        total = int(self.total_slots.get())
        if '/' in probability:
            numerator, denominator = map(int, probability.split('/'))
            probability = numerator / denominator
        else:
            probability = float(probability)
        return int(total * probability)

    def generate_code(self):
        total_slots = self.total_slots.get()
        guaranteed_code = f'    guaranteed {{\n'
        main_code = f'    main {{\n'
        main_code += f'        total({total_slots})\n'

        for item in self.items:
            name = item[0].get() if item[0].get() != "" else "BONES"
            quantity = item[1].get() if item[1].get() != "" else "1"
            probability = item[2].get() if item[2].get() != "" else "1/28"

            if "-" in quantity:
                range_start, range_end = quantity.split('-')
                quantity_kotlin = f"{range_start}..{range_end}"
                quantity_param = f"quantityRange = {quantity_kotlin}"
            else:
                quantity_param = f"quantity = {quantity}"

            if item[3].get():
                guaranteed_code += f'        obj(Items.{name.upper()}, {quantity_param})\n'
            else:
                slots = self.calculate_slots(probability)
                main_code += f'        obj(Items.{name.upper()}, {quantity_param}, slots = {slots})\n'

        guaranteed_code += '    }\n'
        main_code += '    }\n'

        code = 'val table = DropTableFactory.build {\n'
        code += guaranteed_code
        code += main_code
        code += '}\n\n'

        self.display_code(code)

    def display_code(self, code):
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", code)
        self.output_text.configure(state="disabled")

root = tk.Tk()
root.geometry("800x700")
root.resizable(True, True)

app = Application(master=root)
app.mainloop()
