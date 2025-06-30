import tkinter as tk
from tkinter import filedialog, messagebox, Canvas
from app_logic.post_manager import (
    get_posts,
    create_post,
    like_post,
    unlike_post,
    delete_post,
    update_post, comment_post, get_comments,
)
from app_logic.user_manager import follow_user, update_user_bio, change_password, search_users, get_followers,get_all_users,is_following,unfollow_user,validate_current_password



class DashboardWindow:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title("ConnectSphere - Social Dashboard")
        self.root.geometry("1200x700")
        self.create_layout()

    def create_layout(self):
        self.sidebar = tk.Frame(self.root, bg="#4267B2", width=250, height=700)  #blue color
        self.sidebar.pack(side="left", fill="y")

        #profile section: display user profile at the top
        profile_frame = tk.Frame(self.sidebar, bg="#4267B2", padx=10, pady=20)
        profile_frame.pack(fill="x", padx=5)
        tk.Label(profile_frame, text="Profile", font=("Arial", 18, "bold"), fg="white", bg="#4267B2").pack()

        #sidebar Buttons for navigation
        sidebar_buttons = [
            ("Home", self.setup_home),
            ("Create Post", self.setup_create_post),
            ("Follow Users", self.setup_follow_users),
            ("Check Followers", self.setup_check_followers),
            ("Update Bio", self.setup_update_bio),
            ("Change Password", self.setup_change_password),
            ("Logout", self.logout),
        ]

        for btn_text, command in sidebar_buttons:
            tk.Button(self.sidebar, text=btn_text, command=command, bg="#4B77BE", fg="white", font=("Arial", 14),
                      bd=0, relief="flat", activebackground="#3B5C8E", activeforeground="white").pack(fill="x", pady=10)

        #content area: where posts are displayed
        self.content_area = tk.Frame(self.root, bg="#f5f5f5", padx=20)
        self.content_area.pack(side="right", fill="both", expand=True)

        #initial loading of home feed
        self.setup_home()
    def logout(self):
        """handle logout and return to the login window."""
        self.root.destroy()  #close the dashboard window

        #delayed import of Login window to avoid circular import
        from ui.login_window import LoginWindow

        #open the login window
        login_root = tk.Tk()
        LoginWindow(login_root)
        login_root.mainloop()

    def setup_check_followers(self):
        """sets up the check followers section"""
        self.clear_content_area()  #clear the previous UI content
        #title
        tk.Label(
            self.content_area,
            text="Your Followers",
            font=("Arial", 16, "bold"),
            bg="#f5f5f5",
        ).pack(pady=20)

        #fetch followers using the updated function
        try:
            followers=get_followers(self.username)
        except Exception as e:
            tk.Label(
                self.content_area,
                text=f"Error fetching followers: {e}",
                font=("Arial", 12),
                fg="red",
                bg="#f5f5f5",
            ).pack(pady=20)
            return

        #scrollable bar
        canvas=tk.Canvas(self.content_area, bg="#f5f5f5", highlightthickness=0)
        scroll_y=tk.Scrollbar(self.content_area, orient="vertical", command=canvas.yview)
        scroll_frame=tk.Frame(canvas, bg="#f5f5f5")
        #bind scrolling and configure the canvas
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scroll_y.set)
        #pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")
        #display each follower
        if followers:
            for follower in followers:
                follower_frame = tk.Frame(
                    scroll_frame, bg="white", padx=10, pady=10, borderwidth=1, relief="solid"
                )
                follower_frame.pack(fill="x", pady=5)

                tk.Label(
                    follower_frame,
                    text=follower["username"],
                    font=("Arial", 14, "bold"),
                    bg="white",
                ).pack(anchor="w")
                tk.Label(
                    follower_frame,
                    text=follower["bio"] or "No bio available.",
                    font=("Arial", 12),
                    bg="white",
                ).pack(anchor="w", pady=5)
        else:
            #display No follower message
            tk.Label(
                scroll_frame,
                text="No followers found.",
                font=("Arial", 12),
                bg="#f5f5f5",
            ).pack(pady=20)

    def show_comments(self, post, post_frame):
        comments_frame = tk.Frame(post_frame, bg="#f9f9f9", padx=10, pady=5, relief="solid", borderwidth=1)
        comments_frame.pack(fill="x", pady=5)

        comments = get_comments(post['id'])  #fetch comment
        for comment in comments:
            tk.Label(comments_frame, text=f"{comment['username']}:", font=("Arial", 10, "bold"),
                     bg="#f9f9f9", anchor="w").pack(anchor="w")
            tk.Label(comments_frame, text=comment['comment'], wraplength=650, justify="left",
                     font=("Arial", 10), bg="#f9f9f9").pack(anchor="w", padx=10, pady=(0, 5))

        #comment Entry Box
        comment_entry = tk.Entry(comments_frame, font=("Arial", 10))
        comment_entry.pack(fill="x", padx=5, pady=5)

        #submit comment Button
        tk.Button(comments_frame, text="Add Comment",
                  command=lambda: self.add_comment(post['id'], comment_entry.get(), post_frame),
                  bg="#2ecc71", fg="white", font=("Arial", 10)).pack(pady=5)

    def add_comment(self, post_id, comment_text, post_frame):
        if comment_text.strip():
            if comment_post(post_id, self.username, comment_text):
                messagebox.showinfo("Success", "Comment added successfully!")
                self.show_comments({"id": post_id}, post_frame)

    def like_post(self, post):
        if like_post(post['id']):
            self.setup_home()

    def unlike_post(self, post):
        if unlike_post(post['id']):
            self.setup_home()

    def share_post(self, post):
        messagebox.showinfo("Share Post", f"Post shared: {post['title']}")

    def edit_post(self, post):
        self.clear_content_area()
        tk.Label(self.content_area, text="Edit Post", font=("Arial", 16, "bold"), bg="#f5f5f5").pack(pady=20)

        tk.Label(self.content_area, text="Title:", bg="#f5f5f5").pack(anchor="w", padx=10)
        title_entry = tk.Entry(self.content_area)
        title_entry.insert(0, post['title'])
        title_entry.pack(fill="x", padx=10, pady=5)

        tk.Label(self.content_area, text="Content:", bg="#f5f5f5").pack(anchor="w", padx=10)
        content_entry = tk.Text(self.content_area, height=5)
        content_entry.insert("1.0", post['content'])
        content_entry.pack(fill="x", padx=10, pady=5)

        tk.Button(self.content_area, text="Save", command=lambda: self.save_post(post, title_entry, content_entry)).pack(pady=20)

    def save_post(self, post, title_entry, content_entry):
        title=title_entry.get()
        content=content_entry.get("1.0", tk.END).strip()
        if update_post(post['id'], title, content):
            messagebox.showinfo("Success", "Post updated successfully!")
            self.setup_home()
        else:
            messagebox.showerror("Error", "Failed to update post.")

    def delete_post(self, post):
        if delete_post(post['id']):
            messagebox.showinfo("Success", "Post deleted successfully!")
            self.setup_home()
        else:
            messagebox.showerror("Error", "Failed to delete post.")

    def setup_create_post(self):
        self.clear_content_area()
        tk.Label(self.content_area, text="Create a Post", font=("Arial", 16, "bold"), bg="#f5f5f5").pack(pady=20)

        tk.Label(self.content_area, text="Title:", bg="#f5f5f5").pack(anchor="w", padx=10)
        self.title_entry = tk.Entry(self.content_area)
        self.title_entry.pack(fill="x", padx=10, pady=5)

        tk.Label(self.content_area, text="Content:", bg="#f5f5f5").pack(anchor="w", padx=10)
        self.content_entry = tk.Text(self.content_area, height=5)
        self.content_entry.pack(fill="x", padx=10, pady=5)

        tk.Label(self.content_area, text="Category:", bg="#f5f5f5").pack(anchor="w", padx=10)
        self.category_entry = tk.Entry(self.content_area)
        self.category_entry.pack(fill="x", padx=10, pady=5)

        tk.Button(self.content_area, text="Attach Image", command=self.attach_image).pack(pady=5)
        tk.Button(self.content_area, text="Submit", command=self.submit_post).pack(pady=10)

    def submit_post(self):
        title = self.title_entry.get()
        content = self.content_entry.get("1.0", tk.END).strip()
        category = self.category_entry.get()

        if create_post(self.username, title, content, category):
            messagebox.showinfo("Success", "Post created successfully!")
            self.setup_home()
        else:
            messagebox.showerror("Error", "Failed to create post.")

    def attach_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            messagebox.showinfo("Image Attached", f"Image successfully attached: {file_path}")

    def clear_content_area(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()

    def setup_follow_users(self):
        """set up UI for following users"""
        self.clear_content_area()  # Clear the previous content
        tk.Label(self.content_area, text="Follow Users", font=("Arial", 16, "bold"), bg="#f5f5f5").pack(pady=20)
        #search user functionality
        tk.Label(self.content_area, text="Search for Users:", bg="#f5f5f5").pack(anchor="w", padx=10)
        self.search_entry = tk.Entry(self.content_area, font=("Arial", 12))
        self.search_entry.pack(fill="x", padx=10, pady=5)

        self.search_button = tk.Button(self.content_area, text="Search", command=self.search_users, font=("Arial", 12),
                                       bg="#3498DB", fg="white")
        self.search_button.pack(pady=10)

        self.results_frame = tk.Frame(self.content_area, bg="#f5f5f5")
        self.results_frame.pack(fill="both", expand=True, pady=10)

    def search_users(self):
        """search users based on search term"""
        search_term = self.search_entry.get().strip()
        if search_term:
            #fetch user based on the search term
            users = search_users(search_term, exclude_user=self.current_user)
            self.display_user_search_results(users)
        else:
            messagebox.showerror("Error", "Please enter a search term.")

    def display_user_search_results(self, users):
        """Display search result in the UI with follow button"""
        #clear previous search results
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        if not users:
            tk.Label(self.results_frame, text="No users found.", bg="#f5f5f5", font=("Arial", 12)).pack(pady=20)
            return
        #display the result
        for user in users:
            user_frame = tk.Frame(self.results_frame, bg="white", padx=10, pady=10, borderwidth=1, relief="solid")
            user_frame.pack(fill="x", pady=5)

            tk.Label(user_frame, text=user['username'], font=("Arial", 14, "bold"), bg="white").pack(anchor="w")
            tk.Label(user_frame, text=user['bio'], font=("Arial", 12), bg="white").pack(anchor="w", pady=5)

            #check if current user is already following the user
            if is_following(self.current_user, user['username']):
                button_text = "Unfollow"
                button_color = "#e74c3c"  # Red for unfollow
                follow_command = lambda u=user: self.unfollow_user(u['username'])
            else:
                button_text = "Follow"
                button_color = "#2ecc71"  # Green for follow
                follow_command = lambda u=user: self.follow_user(u['username'])

            follow_button = tk.Button(user_frame, text=button_text, command=follow_command,
                                      font=("Arial", 10), bg=button_color, fg="white", relief="flat")
            follow_button.pack(side="right", padx=5)

    def follow_user(self, username_to_follow):
        """Follow a user"""
        success = follow_user(self.current_user, username_to_follow)
        if success:
            messagebox.showinfo("Success", f"You are now following {username_to_follow}")
            self.search_users()  # Refresh the search results
        else:
            messagebox.showerror("Error", "Failed to follow user.")

    def unfollow_user(self, username_to_unfollow):
        """Unfollow a user."""
        success = unfollow_user(self.current_user, username_to_unfollow)
        if success:
            messagebox.showinfo("Success", f"You are no longer following {username_to_unfollow}")
            self.search_users()  # Refresh the search results
        else:
            messagebox.showerror("Error", "Failed to unfollow user.")

    def fetch_users(self, search_term):
        """Fetch users based on the search term"""
        return search_users(search_term)

    def setup_update_bio(self):
        self.clear_content_area()
        tk.Label(self.content_area, text="Update Bio", font=("Arial", 16, "bold"), bg="#f5f5f5").pack(pady=20)

        tk.Label(self.content_area, text="New Bio:", bg="#f5f5f5").pack(anchor="w", padx=10)
        self.bio_entry = tk.Text(self.content_area, height=5, font=("Arial", 12))
        self.bio_entry.pack(fill="x", padx=10, pady=5)

        tk.Button(self.content_area, text="Update Bio", command=self.update_bio, font=("Arial", 12), bg="#3498DB",
                  fg="white").pack(pady=20)

    def update_bio(self):
        new_bio = self.bio_entry.get("1.0", tk.END).strip()
        if update_user_bio(self.username, new_bio):
            messagebox.showinfo("Success", "Bio updated successfully!")
        else:
            messagebox.showerror("Error", "Failed to update bio.")

    def setup_change_password(self):
        self.clear_content_area()
        tk.Label(self.content_area, text="Change Password", font=("Arial", 16, "bold"), bg="#f5f5f5").pack(pady=20)

        #current password field
        tk.Label(self.content_area, text="Current Password:", bg="#f5f5f5").pack(anchor="w", padx=10)
        self.current_password_entry = tk.Entry(self.content_area, show="*", font=("Arial", 12))
        self.current_password_entry.pack(fill="x", padx=10, pady=5)

        #new password field
        tk.Label(self.content_area, text="New Password:", bg="#f5f5f5").pack(anchor="w", padx=10)
        self.new_password_entry = tk.Entry(self.content_area, show="*", font=("Arial", 12))
        self.new_password_entry.pack(fill="x", padx=10, pady=5)

        #confirm password field
        tk.Label(self.content_area, text="Confirm Password:", bg="#f5f5f5").pack(anchor="w", padx=10)
        self.confirm_password_entry = tk.Entry(self.content_area, show="*", font=("Arial", 12))
        self.confirm_password_entry.pack(fill="x", padx=10, pady=5)

        tk.Button(self.content_area, text="Change Password", command=self.change_password, font=("Arial", 12),
                  bg="#3498DB", fg="white").pack(pady=20)

    def change_password(self):
        current_password = self.current_password_entry.get().strip()
        new_password = self.new_password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()

        #validate current password
        if not validate_current_password(self.username, current_password):
            messagebox.showerror("Error", "Current password is incorrect!")
            return

        #check if new password matches the confirm password field
        if new_password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        #ensure new password meets security requirements
        if len(new_password) < 8:
            messagebox.showerror("Error", "New password must be at least 8 characters long!")
            return

        #attempt to change the password
        if change_password(self.username, new_password):
            messagebox.showinfo("Success", "Password changed successfully!")
        else:
            messagebox.showerror("Error", "Failed to change password.")

    def setup_home(self):
        self.clear_content_area()
        tk.Label(self.content_area, text="News Feed", font=("Arial", 20, "bold"), bg="#f5f5f5").pack(pady=20)

        #scrolling through posts
        canvas = Canvas(self.content_area, bg="#f5f5f5")
        scroll_y = tk.Scrollbar(self.content_area, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="#f5f5f5")
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="n")
        canvas.configure(yscrollcommand=scroll_y.set)

        canvas.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")

        posts = get_posts()  #fetch posts
        for post in posts:
            post_frame = tk.Frame(scroll_frame, bg="white", borderwidth=1, relief="flat", padx=15, pady=10)
            post_frame.pack(fill="x", padx=10, pady=10, anchor="center")  # Center-align the post

            #post header
            tk.Label(post_frame, text=f"{post['username']} | 2 hours ago", font=("Arial", 10, "bold"), fg="#4C4C4C",
                     anchor="center", bg="white").pack()

            #post title
            tk.Label(post_frame, text=post['title'], font=("Arial", 14, "bold"), anchor="center", bg="white").pack()

            #post content
            tk.Label(post_frame, text=post['content'], wraplength=650, justify="center", font=("Arial", 12),
                     bg="white").pack(pady=(5, 10))

            #post options
            options_frame = tk.Frame(post_frame, bg="white")
            options_frame.pack(pady=5)

            tk.Button(options_frame, text="Edit Post", command=lambda p=post: self.edit_post(p),
                      font=("Arial", 10), bg="#f39c12", fg="white", relief="flat").pack(side="left", padx=5)
            tk.Button(options_frame, text="Delete Post", command=lambda p=post: self.delete_post(p),
                      font=("Arial", 10), bg="#e74c3c", fg="white", relief="flat").pack(side="left", padx=5)
            tk.Button(options_frame, text="Share Post", command=lambda p=post: self.share_post(p),
                      font=("Arial", 10), bg="#3498DB", fg="white", relief="flat").pack(side="left", padx=5)

            #like and comment buttons
            button_frame = tk.Frame(post_frame, bg="white")
            button_frame.pack(pady=5)

            like_btn = tk.Button(button_frame, text=f"Like ({post['likes']})", command=lambda p=post: self.like_post(p),
                                 font=("Arial", 10), bg="#4267B2", fg="white", relief="flat", width=12)
            like_btn.pack(side="left", padx=5)

            comment_btn = tk.Button(button_frame, text="Comment",
                                    command=lambda p=post: self.show_comments(p, post_frame),
                                    font=("Arial", 10), bg="#3498DB", fg="white", relief="flat", width=12)
            comment_btn.pack(side="left", padx=5)

            #display comments section
            self.show_comments(post, post_frame)

    def show_comments(self, post, post_frame):
        comments_frame = tk.Frame(post_frame, bg="#f9f9f9", padx=10, pady=5, relief="solid", borderwidth=1)
        comments_frame.pack(fill="x", pady=5, anchor="center")

        comments = get_comments(post['id'])  # Fetch comments
        for comment in comments:
            comment_frame = tk.Frame(comments_frame, bg="#f9f9f9", pady=5)
            comment_frame.pack(fill="x", anchor="center")

            tk.Label(comment_frame, text=f"{comment['username']}:", font=("Arial", 10, "bold"),
                     bg="#f9f9f9", anchor="w").pack(anchor="w")
            tk.Label(comment_frame, text=comment['comment'], wraplength=650, justify="center",
                     font=("Arial", 10), bg="#f9f9f9").pack(anchor="center", padx=10, pady=(0, 5))

            #comment option
            options_frame = tk.Frame(comment_frame, bg="#f9f9f9")
            options_frame.pack(fill="x", pady=2)

            tk.Button(options_frame, text="Edit", font=("Arial", 8), bg="#f39c12", fg="white",
                      command=lambda c=comment: self.edit_comment(post, c)).pack(side="left", padx=5)
            tk.Button(options_frame, text="Delete", font=("Arial", 8), bg="#e74c3c", fg="white",
                      command=lambda c=comment: self.delete_comment(post, c)).pack(side="left", padx=5)

        #comment entry box
        comment_entry = tk.Entry(comments_frame, font=("Arial", 10))
        comment_entry.pack(fill="x", padx=5, pady=5)

        tk.Button(comments_frame, text="Add Comment",
                  command=lambda: self.add_comment(post['id'], comment_entry.get(), post_frame),
                  bg="#2ecc71", fg="white", font=("Arial", 10)).pack(pady=5)
    def follow_user_by_search(current_user, search_term):
        """
        search for user by username and allow the current user to follow them,
        excluding the current users own username from the result
        """
        matched_users = search_users(search_term, exclude_user=current_user)

        if not matched_users:
            return False, f"No users found matching '{search_term}'."

        #assume user want to follow the first matched user
        user_to_follow = matched_users[0]["username"]

        success, message = follow_user(current_user, user_to_follow)
        return success, message
