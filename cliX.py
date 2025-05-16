import tkinter as tk
from tkinter import simpledialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import subprocess
import os

# File to store aliases and commands
FILE_NAME = "aliases_commands.txt"

# Function to load aliases and commands from file
def load_aliases_commands():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, 'r') as file:
        lines = file.readlines()
    return [line.strip().split('=', 1) for line in lines]

# Function to save aliases and commands to file
def save_aliases_commands(aliases_commands):
    with open(FILE_NAME, 'w') as file:
        for alias, command in aliases_commands:
            file.write(f"{alias}={command}\n")

# Function to execute a command
def execute_command(command):
    print("\nExecuting alias: " + command[0] + " with command: " + command[1])
    strCommand = command[1]

    try:
        # Check if the command requires sudo
        if strCommand[:4] == "sudo":
            password = simpledialog.askstring("Password", "Enter sudo password:", show='*')
            if password:
                strCommand = f"echo {password} | sudo -S {strCommand[5:]}"
            else:
                return

        # Execute the command
        subprocess.run(strCommand, shell=True)
    except Exception as e:
        print(f"Failed to execute command: {str(e)}")
    print("Finished!!")

# Function to add a new alias and command
def add_alias_command():
    alias = simpledialog.askstring("Alias", "Enter alias:")
    command = simpledialog.askstring("Command", "Enter command:")
    if alias and command:
        aliases_commands.append((alias, command))
        save_aliases_commands(aliases_commands)
        update_grid()
    else:
        messagebox.showwarning("Input Error", "Alias and Command cannot be empty.")

# Function to edit an existing alias and command
def edit_alias_command():
    selected_item = grid.selection()
    index = grid.index(selected_item)
    if selected_item:
        item = grid.item(selected_item)
        alias, command = item["values"]
        new_alias = simpledialog.askstring("Edit Alias", "Enter new alias:", initialvalue=alias)
        new_command = simpledialog.askstring("Edit Command", "Enter new command:", initialvalue=command)
        if new_alias and new_command:
            aliases_commands[index] = (new_alias, new_command)
            save_aliases_commands(aliases_commands)
            update_grid()
        else:
            messagebox.showwarning("Input Error", "Alias and Command cannot be empty.")
    else:
        messagebox.showwarning("Selection Error", "No item selected.")

# Function to delete an existing alias and command
def delete_alias_command():
    selected_item = grid.selection()
    index = grid.index(selected_item)
    if selected_item:
        del aliases_commands[index]
        save_aliases_commands(aliases_commands)
        update_grid()
    else:
        messagebox.showwarning("Selection Error", "No item selected.")

# Function to update the grid with aliases and commands
def update_grid(filter_text=""):
    for row in grid.get_children():
        grid.delete(row)
    for alias, command in aliases_commands:
        if filter_text.lower() in alias.lower():
            grid.insert("", "end", values=(alias, command))

# Function to sort the grid by alias
def sort_by_alias():
    global aliases_commands
    aliases_commands.sort(key=lambda x: x)
    update_grid(filter_entry.get())

# Function to change theme
def change_theme(event=None):
    selected_theme = theme_selector.get()
    root.style.theme_use(selected_theme)

# Create the main window with TTKBootstrap theme
root = ttk.Window(themename="cyborg")
root.title("Alias Command Manager")
root.geometry("1100x600")

# Create a frame for theme selection
theme_frame = ttk.Frame(root)
theme_frame.pack(pady=5, padx=10, fill=tk.X)

# Theme selector label
ttk.Label(theme_frame, text="Theme:").pack(side=tk.LEFT, padx=(550, 5))

# Theme selector dropdown
theme_selector = ttk.Combobox(
    theme_frame,
    values=sorted(root.style.theme_names()),
    state="readonly"
)
theme_selector.pack(side=tk.LEFT, fill=tk.X, expand=True)
theme_selector.set("cosmo")  # Set default theme
theme_selector.bind("<<ComboboxSelected>>", change_theme)

# Create a frame for the buttons
button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

# Create buttons with different styles
add_button = ttk.Button(
    button_frame,
    text="Add Alias Command",
    command=add_alias_command,
    bootstyle=SUCCESS,
    padding=10
)
add_button.pack(side=tk.LEFT, padx=5)

edit_button = ttk.Button(
    button_frame,
    text="Edit Alias Command",
    command=edit_alias_command,
    bootstyle=WARNING,
    padding=10
)
edit_button.pack(side=tk.LEFT, padx=5)

delete_button = ttk.Button(
    button_frame,
    text="Delete Alias Command",
    command=delete_alias_command,
    bootstyle=DANGER,
    padding=10
)
delete_button.pack(side=tk.LEFT, padx=5)

refresh_button = ttk.Button(
    button_frame,
    text="Refresh",
    command=lambda: update_grid(filter_entry.get()),
    bootstyle=INFO,
    padding=10
)
refresh_button.pack(side=tk.LEFT, padx=5)

# Create a frame for the filter
filter_frame = ttk.Frame(root)
filter_frame.pack(pady=(10, 0), padx=10, fill=tk.X)

# Filter widgets
filter_entry = ttk.Entry(filter_frame, font=("Arial", 12))
filter_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

filter_button = ttk.Button(
    filter_frame,
    text="Filter",
    command=lambda: update_grid(filter_entry.get()),
    bootstyle=INFO,
    padding=10
)
filter_button.pack(side=tk.LEFT)

# Create the grid (Treeview)
grid = ttk.Treeview(
    root,
    columns=("Alias", "Command"),
    show="headings",
    bootstyle=PRIMARY
)
grid.heading("Alias", text="Alias", command=sort_by_alias)
grid.heading("Command", text="Command")
grid.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Configure column widths
grid.column("Alias", width=200, anchor=tk.W)
grid.column("Command", width=800, anchor=tk.W)

# Add scrollbar
scrollbar = ttk.Scrollbar(
    grid,
    orient=tk.VERTICAL,
    command=grid.yview,
    bootstyle=PRIMARY
)
# Create and configure a custom dark gray scrollbar style
style = ttk.Style()
style.configure("Dark.Vertical.TScrollbar",
                background="#000000",  # Dark gray thumb
                troughcolor="#888888",  # Slightly lighter track
                bordercolor="#222222",
                arrowcolor="#AAAAAA",   # Arrow color (if visible)
                gripcount=0)            # Remove grip lines

# Apply the custom style
scrollbar.configure(style="Dark.Vertical.TScrollbar")


grid.configure(yscroll=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Load aliases and commands
aliases_commands = load_aliases_commands()
update_grid()

# Bind double-click event
grid.bind("<Double-1>", lambda event: execute_command(grid.item(grid.selection())["values"]))

# Run the application
root.mainloop()