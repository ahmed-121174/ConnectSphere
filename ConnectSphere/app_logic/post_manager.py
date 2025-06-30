import os
from datetime import datetime

POSTS_FILE = "posts.txt"

def get_posts():
    """retrieve all posts from post file"""
    posts = []
    if os.path.exists(POSTS_FILE):#check if file containing posts exist
        with open(POSTS_FILE, "r") as file:#open the file in read mode (with) statement ensure the file is properly closed after its block is executed even if an exception occurs.
            for index, line in enumerate(file.readlines()):#(enumerate) provides both the line index (starting from 0) and the line content
                post_data = line.strip().split("|")
                posts.append({#dictionary representing a post to the (posts) list
                    "id": index,
                    "username": post_data[0],
                    "title": post_data[1],
                    "content": post_data[2],
                    "timestamp": post_data[3],
                    "likes": int(post_data[4]),
                    "comments": post_data[5].split(",") if post_data[5] else [],
                    "category": post_data[6],
                    "image": post_data[7] if len(post_data) > 7 else ""
                })
    return posts

def create_post(username, title, content, category, image=""):
    """create a new post"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(POSTS_FILE, "a") as file:
        file.write(f"{username}|{title}|{content}|{timestamp}|0||{category}|{image}\n")
    return True

def like_post(post_id):
    """increment like count for a post"""
    posts = get_posts()
    if 0 <= post_id < len(posts):
        posts[post_id]['likes'] += 1
        save_posts(posts)
        return True
    return False

def unlike_post(post_id):
    """decrement the like count for a post, ensuring it does not go below zero"""
    posts = get_posts()
    if 0 <= post_id < len(posts) and posts[post_id]['likes'] > 0:
        posts[post_id]['likes'] -= 1
        save_posts(posts)
        return True
    return False

def delete_post(post_id):
    """delete a post based on its ID"""
    posts = get_posts()
    if 0 <= post_id < len(posts):
        del posts[post_id]
        save_posts(posts)
        return True
    return False

def update_post(post_id, title, content):
    """update the title and content of a post"""
    posts = get_posts()
    if 0 <= post_id < len(posts):
        posts[post_id]['title'] = title
        posts[post_id]['content'] = content
        save_posts(posts)
        return True
    return False

def save_posts(posts):
    """save updated list of posts back to posts file"""
    with open(POSTS_FILE, "w") as file:
        for post in posts:
            file.write(f"{post['username']}|{post['title']}|{post['content']}|{post['timestamp']}|"
                       f"{post['likes']}|{','.join(post['comments'])}|{post['category']}|{post['image']}\n")

def get_post_by_id(post_id):
    """retrieve single post by its ID"""
    posts = get_posts()
    if 0 <= post_id < len(posts):
        return posts[post_id]
    return None

def share_post(post_id):
    """simulate sharing post"""
    post = get_post_by_id(post_id)
    if post:
        #sharing implemented here
        return f"Post shared: {post['title']}"
    return None

def comment_post(post_id, username, comment_text):
    """add comment to post"""
    posts = get_posts()
    if 0 <= post_id < len(posts):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        comment = f"{username}:{comment_text}:{timestamp}"  #format as username:comment:timestamp
        posts[post_id]["comments"].append(comment)
        save_posts(posts)
        return True
    return False

def get_comments(post_id):
    """retrieve comments for post"""
    posts = get_posts()
    if 0 <= post_id < len(posts):
        comments = posts[post_id]["comments"]
        formatted_comments = []
        for comment in comments:
            parts = comment.split(":")
            if len(parts) == 3:
                formatted_comments.append({
                    "username": parts[0],
                    "comment": parts[1],
                    "time": parts[2]
                })
        return formatted_comments
    return []