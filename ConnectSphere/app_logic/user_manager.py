import os
import glob
USER_DATA_DIR = "user_data"
FOLLOW_FILE_SUFFIX = "_follow.txt"
PASSWORD_FILE_SUFFIX = ".txt"
BIO_FILE_SUFFIX = "_bio.txt"


def validate_current_password(username, current_password):
    """
    validate the current password for a user from the user data directory

    :param username: Username of the account.
    :param current_password: Current password to validate.
    :return: Boolean indicating if the current password is valid.
    """
    user_file = f"{USER_DATA_DIR}/{username}{PASSWORD_FILE_SUFFIX}"

    #check if the user file exists
    if not os.path.exists(user_file):
        return False

    #read and validate the current password
    with open(user_file, "r") as file:
        stored_password = file.readline().strip()
        return stored_password == current_password


def create_user(username, password):
    """create a new user with the given username and password"""
    user_file = f"{USER_DATA_DIR}/{username}{PASSWORD_FILE_SUFFIX}"
    if not os.path.exists(user_file):
        os.makedirs(USER_DATA_DIR, exist_ok=True)
        with open(user_file, "w") as file:
            file.write(password + "\n")
        with open(f"{USER_DATA_DIR}/{username}{BIO_FILE_SUFFIX}", "w") as bio_file:
            bio_file.write("")  #empty bio initially
        return True
    return False


def authenticate_user(username, password):
    """Authenticate a user based on username and password."""
    user_file = f"{USER_DATA_DIR}/{username}{PASSWORD_FILE_SUFFIX}"
    if os.path.exists(user_file):
        with open(user_file, "r") as file:
            stored_password = file.readline().strip()
            return stored_password == password
    return False


def get_all_users():
    """Retrieve all users from the data directory."""
    user_files = glob.glob(f"{USER_DATA_DIR}/*{PASSWORD_FILE_SUFFIX}")
    users = []
    for user_file in user_files:
        username = os.path.basename(user_file).replace(PASSWORD_FILE_SUFFIX, "")
        bio = get_user_bio(username)
        users.append({"username": username, "bio": bio})
    return users


def search_users(search_term, exclude_user=None):
    """Search for users by username or bio containing the search term."""
    all_users = get_all_users()
    filtered_users = [
        user for user in all_users
        if search_term.lower() in user["username"].lower() or search_term.lower() in user["bio"].lower()
    ]

    # Exclude the current user from the results
    if exclude_user:
        filtered_users = [user for user in filtered_users if user["username"] != exclude_user]

    return filtered_users


def follow_user(username, user_to_follow):
    """Follow a user."""
    follow_file = f"{USER_DATA_DIR}/{username}{FOLLOW_FILE_SUFFIX}"

    if os.path.exists(follow_file):
        with open(follow_file, "a") as file:
            file.write(user_to_follow + "\n")
        return True
    return False


def unfollow_user(username, user_to_unfollow):
    """Unfollow a user."""
    follow_file = f"{USER_DATA_DIR}/{username}{FOLLOW_FILE_SUFFIX}"

    if os.path.exists(follow_file):
        with open(follow_file, "r") as file:
            followed_users = file.readlines()

        followed_users = [user.strip() for user in followed_users]

        if user_to_unfollow in followed_users:
            followed_users.remove(user_to_unfollow)

            with open(follow_file, "w") as file:
                for user in followed_users:
                    file.write(user + "\n")
            return True
    return False


def is_following(username, user_to_check):
    """Check if the user is following another user."""
    follow_file = f"{USER_DATA_DIR}/{username}{FOLLOW_FILE_SUFFIX}"

    if os.path.exists(follow_file):
        with open(follow_file, "r") as file:
            followed_users = [line.strip() for line in file.readlines()]
            return user_to_check in followed_users
    return False


def get_user_bio(username):
    """Retrieve the bio of a specified user."""
    bio_file = f"{USER_DATA_DIR}/{username}{BIO_FILE_SUFFIX}"
    if os.path.exists(bio_file):
        with open(bio_file, "r") as file:
            return file.read().strip()
    return ""


def get_followed_users(username):
    """Retrieve the list of users that the given user follows."""
    follow_file = f"{USER_DATA_DIR}/{username}{FOLLOW_FILE_SUFFIX}"
    if os.path.exists(follow_file):
        with open(follow_file, "r") as file:
            return [line.strip() for line in file.readlines()]
    return []


def update_user_bio(username, new_bio):
    """Update the bio for the specified user."""
    bio_file = f"{USER_DATA_DIR}/{username}{BIO_FILE_SUFFIX}"
    if os.path.exists(bio_file):
        with open(bio_file, "w") as file:
            file.write(new_bio)
        return True
    return False


def change_password(username, new_password):
    """Change the password for the specified user."""
    user_file = f"{USER_DATA_DIR}/{username}{PASSWORD_FILE_SUFFIX}"
    if os.path.exists(user_file):
        with open(user_file, "w") as file:
            file.write(new_password + "\n")
        return True
    return False



def get_followers(username):
    """
    Get the list of users who are following the given username.
    """
    followers = []
    user_files = glob.glob(f"{USER_DATA_DIR}/*{FOLLOW_FILE_SUFFIX}")
    for follow_file in user_files:
        with open(follow_file, "r") as file:
            followed_users = [line.strip() for line in file.readlines()]
            if username in followed_users:
                follower_username = os.path.basename(follow_file).replace(FOLLOW_FILE_SUFFIX, "")
                bio = get_user_bio(follower_username)
                followers.append({"username": follower_username, "bio": bio})
    return followers
