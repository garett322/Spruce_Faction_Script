import tkinter as tk
from updater import update_data

def update_button_click():
    update_data()
    result_label.config(text="Data updated successfully.")

# Create the main window
root = tk.Tk()
root.title("Torn Faction Revive Data Updater")

# Create and place a label for instructions
instructions_label = tk.Label(root, text="Click the 'Update' button to update the data.", padx=10, pady=10)
instructions_label.pack()

# Create and place the Update button
update_button = tk.Button(root, text="Update", command=update_button_click)
update_button.pack()

# Create and place a label to display the update result
result_label = tk.Label(root, text="", fg="green")
result_label.pack()

# Start the main event loop
root.mainloop()
