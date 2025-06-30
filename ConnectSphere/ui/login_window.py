import tkinter as tk
from tkinter import messagebox
from app_logic.session_manager import start_session
from ui.dashboard_window import DashboardWindow
from ui.register_window import RegisterWindow



class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("400x600")
        self.root.resizable(False, False)  #prevent resizing

        self.add_background_using_canvas()

        #add the login form widget
        self.create_widgets()

    def add_background_using_canvas(self):
        """add background using Canvas widget"""
        canvas = tk.Canvas(self.root, width=1000, height=1000)
        canvas.pack(fill="both", expand=True)

        #add the image to the canvas
        bg_image = tk.PhotoImage(file="background.png")
        canvas.create_image(1, 0, image=bg_image, anchor="nw")
        self.root.bg_image = bg_image
        canvas.create_text(
            200, 50,
            text="ConnectSphere",
            font=("Helvetica", 30, "bold"),
            fill="white",
        )


    def create_widgets(self):
        """add widget on top of background"""
        #frame for login widget
        self.frame = tk.Frame(self.root, bg="#f4f4f4", bd=2)

        self.frame.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.7)

        #heading label
        tk.Label(
            self.frame,
            text="Login",
            font=("Helvetica", 24, "bold"),
            bg="#f4f4f4",
            fg="#1DA1F2",
        ).pack(pady=10)

        #username entry
        tk.Label(self.frame, text="Username", font=("Helvetica", 12), bg="#f4f4f4").pack(pady=5)
        self.username_entry = tk.Entry(self.frame, font=("Helvetica", 12))
        self.username_entry.pack(pady=10)

        #password entry
        tk.Label(self.frame, text="Password", font=("Helvetica", 12), bg="#f4f4f4").pack(pady=5)
        self.password_entry = tk.Entry(self.frame, font=("Helvetica", 12), show="*")
        self.password_entry.pack(pady=10)

        #login button
        tk.Button(
            self.frame,
            text="Login",
            command=self.login_user,
            bg="#1DA1F2",
            fg="white",
            font=("Helvetica", 14, "bold"),
        ).pack(pady=10)

        #register button
        tk.Button(
            self.frame,
            text="Create Account",
            command=self.open_register_window,
            bg="white",
            fg="#1DA1F2",
            font=("Helvetica", 12),
        ).pack(pady=5)

    def login_user(self):
        """authenticate user and navigate to dashboard if successful"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Warning", "Please enter both username and password.")
            return

        if start_session(username, password):
            self.root.destroy()  #destroy login window
            dashboard_root = tk.Tk()  #create new window for the dashboard
            DashboardWindow(dashboard_root, username)  #open the dashboard window
            dashboard_root.mainloop()
        else:
            messagebox.showerror("Error", "Invalid login credentials!")

    def open_register_window(self):
        """open registration window"""
        self.root.destroy()  #destroy the login window
        register_root = tk.Tk()  #create new window for registration
        RegisterWindow(register_root)  #open the register window
        register_root.mainloop()

#test the Login window independently
if __name__ == "__main__":
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()
