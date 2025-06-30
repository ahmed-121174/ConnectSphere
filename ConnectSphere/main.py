import tkinter as tk
from ui.login_window import LoginWindow
def main():
    root = tk.Tk()
    root.title("ConnectSphere Login")
    LoginWindow(root)
    root.mainloop()
if __name__ == "__main__":
    main()