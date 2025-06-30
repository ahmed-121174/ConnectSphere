import tkinter as tk
from tkinter import messagebox
from app_logic.user_manager import create_user
from PIL import Image, ImageTk  #importing pillow for image processing


class RegisterWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Register")
        self.root.geometry("400x600")
        self.root.resizable(False, False)

        #add the background image
        self.add_background_using_canvas()

        #create a frame for the register box
        self.register_box = tk.Frame(self.root, bg="white", bd=2, relief="solid")
        self.register_box.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

        self.create_widgets()
    def add_background_using_canvas(self):
        """Method 2: Add background using a Canvas widget."""
        canvas = tk.Canvas(self.root, width=400, height=500)
        canvas.pack(fill="both", expand=True)

        #add the image to the canvas
        bg_image = tk.PhotoImage(file="background.png")  # PNG or GIF format
        canvas.create_image(0, 0, image=bg_image, anchor="nw")
        self.root.bg_image = bg_image  #keep a reference to avoid garbage
        self.root.bg_image = bg_image
        canvas.create_text(
            200, 50,
            text="ConnectSphere",
            font=("Helvetica", 30, "bold"),
            fill="white",
        )

    def create_widgets(self):
        #heading Label
        tk.Label(
            self.register_box,
            text="Create Account",
            font=("Helvetica", 24, "bold"),
            bg="white",
            fg="#1DA1F2",
        ).pack(pady=20)

        #username Entry
        tk.Label(
            self.register_box,
            text="Username",
            font=("Helvetica", 14),
            bg="white",
            fg="#333",
        ).pack(pady=5)
        self.username_entry = tk.Entry(
            self.register_box, font=("Helvetica", 14), bd=2, relief="solid", width=25
        )
        self.username_entry.pack(pady=10)

        #password entry
        tk.Label(
            self.register_box,
            text="Password",
            font=("Helvetica", 14),
            bg="white",
            fg="#333",
        ).pack(pady=5)
        self.password_entry = tk.Entry(
            self.register_box,
            font=("Helvetica", 14),
            bd=2,
            relief="solid",
            width=25,
            show="*",
        )
        self.password_entry.pack(pady=10)

        #confirm password entry
        tk.Label(
            self.register_box,
            text="Confirm Password",
            font=("Helvetica", 14),
            bg="white",
            fg="#333",
        ).pack(pady=5)
        self.confirm_password_entry = tk.Entry(
            self.register_box,
            font=("Helvetica", 14),
            bd=2,
            relief="solid",
            width=25,
            show="*",
        )
        self.confirm_password_entry.pack(pady=10)

        #register button
        tk.Button(
            self.register_box,
            text="Register",
            command=self.register_user,
            bg="#1DA1F2",
            fg="white",
            font=("Helvetica", 14, "bold"),
            relief="flat",
            width=20,
        ).pack(pady=20)

        #go back button
        tk.Button(
            self.register_box,
            text="Go Back to Login",
            command=self.go_back_to_login,
            bg="white",
            fg="#1DA1F2",
            font=("Helvetica", 12),
            relief="flat",
            width=20,
        ).pack(pady=10)

    def register_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        if not username or not password or confirm_password:
            messagebox.showwarning("Warning", "Fill all fields.")
            return

        if password == confirm_password:
            if create_user(username, password):
                messagebox.showinfo("Success", "User registered successfully!")
                self.root.quit()
                self.root.destroy()  # Properly close the register window
            else:
                messagebox.showerror("Error", "Username already exists!")
        else:
            messagebox.showerror("Error", "Passwords do not match!")
        from ui.login_window import LoginWindow
        self.root.quit()
        self.root.destroy()
        #open the login window
        login_root = tk.Tk()
        LoginWindow(login_root)
        login_root.mainloop()

    def go_back_to_login(self):
        self.root.quit()
        self.root.destroy()  #close the register window and return to login window
        from ui.login_window import LoginWindow

        #open the login window
        login_root = tk.Tk()
        LoginWindow(login_root)
        login_root.mainloop()