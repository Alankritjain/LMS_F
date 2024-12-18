import customtkinter as ctk
from tkcalendar import Calendar  # For date selection
import sqlite3
import json
from tkinter import messagebox
import os
from PIL import Image

# Sets up the database to create tables
def create_tables():
    conn = sqlite3.connect("laundry_management.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner TEXT NOT NULL,
            reservation_date TEXT NOT NULL,
            reservation_time TEXT NOT NULL,
            clothes TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def add_reservation(owner, date, time, clothes):
    conn = sqlite3.connect("laundry_management.db")
    cursor = conn.cursor()
    clothes_json = json.dumps(clothes)
    cursor.execute("INSERT INTO reservations (owner, reservation_date, reservation_time, clothes) VALUES (?, ?, ?, ?)",
                   (owner, date, time, clothes_json))
    conn.commit()
    conn.close()


def fetch_reservations():
    conn = sqlite3.connect("laundry_management.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, owner, reservation_date, reservation_time, clothes FROM reservations")
    rows = cursor.fetchall()
    conn.close()
    return rows


def delete_reservation(reservation_id):
    conn = sqlite3.connect("laundry_management.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reservations WHERE id = ?", (reservation_id,))
    conn.commit()
    conn.close()


# Login Page



class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.configure(fg_color="black")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Main container to hold left and right sections
        main_frame = ctk.CTkFrame(self, fg_color="black")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Left Frame for the image
        left_frame = ctk.CTkFrame(main_frame, fg_color="black", width=600)
        left_frame.grid(row=0, column=0, sticky="nsw", padx=20, pady=20)
        print(f"Left Frame Created: {left_frame}")


        # Adding an image to the left frame
        try:
            # Dynamically generate the path
            #image_path = os.path.join("assets", "dark_aesthetic_logo(1).png")
            image_path = "C:\\Users\\alankritjain\\OneDrive - BENNETT UNIVERSITY\\Backup(LMS)\\assets\\logo.png"
            print(f"Using image path: {image_path}")  # Debugging log

            # Load the image using PIL
            pil_image = Image.open(image_path)

            # Convert to CTkImage
            
            image = ctk.CTkImage(pil_image, size=(500, 500))  # Adjust size as needed
            image_label = ctk.CTkLabel(left_frame, image=image, text="")
            image_label.pack(expand=False,padx=200, pady=100)
        except Exception as e:
            print(f"Error loading image: {e}")
            ctk.CTkLabel(
                left_frame,
                text="login page",
                font=ctk.CTkFont(size=114, weight="bold"),
                text_color="white"
            ).pack(expand=True,padx=200, pady=20)

        # Right Frame for login form
        right_frame = ctk.CTkFrame(main_frame, fg_color="#2C2C2C", corner_radius=15, width=500)
        right_frame.grid(row=0, column=1, sticky="nse", padx=20, pady=20)

        # Title Label
        title_label = ctk.CTkLabel(
            right_frame,
            text="Laundry Shop Login",
            font=ctk.CTkFont(size=40, weight="bold"),
            text_color="white"
        )
        title_label.pack(pady=40)

        # Username Entry
        self.username_entry = ctk.CTkEntry(
            right_frame,
            placeholder_text="Enter your name",
            width=400,
            height=50,
            font=ctk.CTkFont(size=18)
        )
        self.username_entry.pack(pady=20)

        # Login Button
        login_button = ctk.CTkButton(
            right_frame,
            text="Login",
            command=self.login,
            fg_color="#1E90FF",
            text_color="white",
            width=200,
            height=50,
            font=ctk.CTkFont(size=18, weight="bold")
        )
        login_button.pack(pady=30)

    def login(self):
        owner_name = self.username_entry.get().strip()
        if owner_name:
            self.controller.owner = owner_name
            self.controller.show_frame("ChecklistPage")
        else:
            ctk.messagebox.showwarning("Warning", "Please enter your name!")

# Checklist Page
class ChecklistPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.selected_clothes = {}

        self.configure(fg_color="black")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.label = ctk.CTkLabel(
            self, 
            text="Checklist", 
            font=ctk.CTkFont(size=42, weight="bold"), 
            text_color="white"
        )
        self.label.pack(pady=20)

        content_frame = ctk.CTkFrame(self, fg_color="black")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        items = ["Shirt", "T-Shirt", "Lower", "Jeans", "Shorts", "Bedsheet", "Pillow Cover", "Blanket", "Kurta"]
        self.item_entries = {}

        right_frame = ctk.CTkFrame(content_frame, fg_color="#2C2C2C", corner_radius=15)
        right_frame.pack(side="right", padx=20, pady=20, fill="both", expand=True)

        for i, item in enumerate(items):
            item_frame = ctk.CTkFrame(right_frame, fg_color="#2C2C2C")
            item_frame.pack(pady=5, padx=20, fill="x")

            label = ctk.CTkLabel(
                item_frame, 
                text=item, 
                font=ctk.CTkFont(size=16), 
                text_color="white"
            )
            label.pack(side="left", padx=10)

            item_var = ctk.StringVar(value="0")
            dropdown = ctk.CTkComboBox(
                item_frame, 
                variable=item_var, 
                values=[str(x) for x in range(21)], 
                width=80, 
                fg_color="gray", 
                button_color="white", 
                text_color="black"
            )
            dropdown.pack(side="right", padx=10)
            self.item_entries[item] = item_var

        next_button = ctk.CTkButton(
            self, 
            text="Submit", 
            command=self.save_clothes, 
            fg_color="white", 
            text_color="black"
        )
        next_button.pack(pady=20)

    def save_clothes(self):
        self.selected_clothes = {item: entry.get() for item, entry in self.item_entries.items() if entry.get() != "0"}

        if not self.selected_clothes:
            messagebox.showwarning("Warning", "No clothes selected!")
            return

        self.controller.data["clothes"] = self.selected_clothes
        self.controller.show_frame("CalendarPage")


# Calendar Page
from tkcalendar import Calendar
from tkinter import messagebox
import customtkinter as ctk


class CalendarPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Header Label
        self.label = ctk.CTkLabel(
            self,
            text="Select Date and Time",
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color="white"  # Optional: White text for visibility
        )
        self.label.pack(pady=20)

        # Frame for Calendar (Light Grey Background)
        calendar_frame = ctk.CTkFrame(self, fg_color="#313131", corner_radius=10, width=600, height=400)
        calendar_frame.pack(pady=20)

        # Calendar Widget Inside the Light Grey Frame
        self.calendar = Calendar(
            calendar_frame,
            selectmode="day",
            year=2024,  # Default year
            month=11,   # Default month
            day=24      # Default day
        )

        # Configure Calendar Styling
        self.calendar.config(
            font=("Helvetica", 16),  # Increase font size
            selectbackground="lightblue",  # Selected date background
            selectforeground="white",  # Selected date text
            background="lightgray",  # Calendar background
            borderwidth=2  # Add border width
        )
        self.calendar.place(relx=0.5, rely=0.5, anchor="center")  # Center the calendar inside the frame

        # Time Entry Field
        self.time_entry = ctk.CTkEntry(
            self, placeholder_text="Enter Time (e.g., 14:30)", font=ctk.CTkFont(size=18)
        )
        self.time_entry.pack(pady=20)

        # Submit Button
        self.submit_button = ctk.CTkButton(
            self,
            text="Submit",
            command=self.save_reservation,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="#1E90FF",  # Blue color
            text_color="white"
        )
        self.submit_button.pack(pady=10)

    def save_reservation(self):
        """Save reservation data to the database."""
        selected_date = self.calendar.get_date()
        selected_time = self.time_entry.get().strip()

        if not selected_time:
            messagebox.showwarning("Warning", "Please enter a time!")
            return

        clothes = self.controller.data.get("clothes", {})
        add_reservation(self.controller.owner, selected_date, selected_time, clothes)
        self.controller.show_frame("TrackerPage")


# Tracker Page
class TrackerPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.label = ctk.CTkLabel(self, text="Tracker", font=ctk.CTkFont(size=24, weight="bold"))
        self.label.pack(pady=20)

        self.reservations_frame = ctk.CTkFrame(self)
        self.reservations_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.refresh_button = ctk.CTkButton(self, text="Refresh", command=self.display_reservations)
        self.refresh_button.pack(pady=10)

        self.display_reservations()

    def display_reservations(self):
        for widget in self.reservations_frame.winfo_children():
            widget.destroy()

        reservations = fetch_reservations()
        for res_id, owner, date, time, clothes in reservations:
            frame = ctk.CTkFrame(self.reservations_frame)
            frame.pack(pady=10, padx=10, fill="x")
            ctk.CTkLabel(frame, text=f"Student Name: {owner}, Date: {date}, Time: {time}", font=ctk.CTkFont(size=14)).pack(anchor="w")
            clothes_dict = json.loads(clothes)
            for item, qty in clothes_dict.items():
                ctk.CTkLabel(frame, text=f"  {item}: {qty}", font=ctk.CTkFont(size=12)).pack(anchor="w")

            delete_button = ctk.CTkButton(frame, text="Delete", fg_color="#E63946",
                                          command=lambda rid=res_id: self.delete_reservation(rid))
            delete_button.pack(anchor="e")

    def delete_reservation(self, reservation_id):
        delete_reservation(reservation_id)
        self.display_reservations()


# Main Application
class LaundryManagementApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Laundry Management System")
        self.geometry("1400x900")  
        create_tables()

        self.owner = ""
        self.data = {}

        self.pages = {}
        for Page in (LoginPage, ChecklistPage, CalendarPage, TrackerPage):
            page_name = Page.__name__
            frame = Page(parent=self, controller=self)
            self.pages[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        frame = self.pages[page_name]
        frame.tkraise()


# Run Application
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = LaundryManagementApp()
    app.mainloop()
