import json
import os
from datetime import datetime
import uuid

class SocialSystem:
    def __init__(self):
        self.social_file = "social_data.json"
        self.social_data = self._load_social_data()

    def _load_social_data(self):
        """Load social data from JSON file"""
        if os.path.exists(self.social_file):
            with open(self.social_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "challenges": {},
            "groups": {},
            "posts": {},
            "friends": {},
            "comments": {}
        }

    def _save_social_data(self):
        """Save social data to JSON file"""
        with open(self.social_file, 'w', encoding='utf-8') as f:
            json.dump(self.social_data, f, ensure_ascii=False, indent=4)

    def create_challenge(self, creator_id, title, description, duration_days, goal_type, target):
        """Create a new challenge"""
        challenge_id = str(uuid.uuid4())
        challenge = {
            "id": challenge_id,
            "creator_id": creator_id,
            "title": title,
            "description": description,
            "duration_days": duration_days,
            "goal_type": goal_type,
            "target": target,
            "start_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "end_date": None,
            "participants": [creator_id],
            "progress": {creator_id: 0},
            "status": "active"
        }
        
        self.social_data["challenges"][challenge_id] = challenge
        self._save_social_data()
        return challenge_id

    def join_challenge(self, user_id, challenge_id):
        """Join an existing challenge"""
        if challenge_id in self.social_data["challenges"]:
            challenge = self.social_data["challenges"][challenge_id]
            if challenge["status"] == "active" and user_id not in challenge["participants"]:
                challenge["participants"].append(user_id)
                challenge["progress"][user_id] = 0
                self._save_social_data()
                return True
        return False

    def update_challenge_progress(self, user_id, challenge_id, progress):
        """Update user's progress in a challenge"""
        if challenge_id in self.social_data["challenges"]:
            challenge = self.social_data["challenges"][challenge_id]
            if user_id in challenge["participants"]:
                challenge["progress"][user_id] = progress
                self._save_social_data()
                return True
        return False

    def create_group(self, creator_id, name, description):
        """Create a new group"""
        group_id = str(uuid.uuid4())
        group = {
            "id": group_id,
            "creator_id": creator_id,
            "name": name,
            "description": description,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "members": [creator_id],
            "admins": [creator_id]
        }
        
        self.social_data["groups"][group_id] = group
        self._save_social_data()
        return group_id

    def join_group(self, user_id, group_id):
        """Join an existing group"""
        if group_id in self.social_data["groups"]:
            group = self.social_data["groups"][group_id]
            if user_id not in group["members"]:
                group["members"].append(user_id)
                self._save_social_data()
                return True
        return False

    def create_post(self, user_id, content, media_url=None, visibility="public"):
        """Create a new post"""
        post_id = str(uuid.uuid4())
        post = {
            "id": post_id,
            "user_id": user_id,
            "content": content,
            "media_url": media_url,
            "visibility": visibility,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "likes": [],
            "comments": []
        }
        
        self.social_data["posts"][post_id] = post
        self._save_social_data()
        return post_id

    def add_comment(self, user_id, post_id, content):
        """Add a comment to a post"""
        if post_id in self.social_data["posts"]:
            comment_id = str(uuid.uuid4())
            comment = {
                "id": comment_id,
                "user_id": user_id,
                "content": content,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "likes": []
            }
            
            self.social_data["posts"][post_id]["comments"].append(comment)
            self._save_social_data()
            return comment_id
        return None

    def like_post(self, user_id, post_id):
        """Like a post"""
        if post_id in self.social_data["posts"]:
            post = self.social_data["posts"][post_id]
            if user_id not in post["likes"]:
                post["likes"].append(user_id)
                self._save_social_data()
                return True
        return False

    def add_friend(self, user_id, friend_id):
        """Add a friend"""
        if user_id not in self.social_data["friends"]:
            self.social_data["friends"][user_id] = []
        if friend_id not in self.social_data["friends"]:
            self.social_data["friends"][friend_id] = []
        
        if friend_id not in self.social_data["friends"][user_id]:
            self.social_data["friends"][user_id].append(friend_id)
            self.social_data["friends"][friend_id].append(user_id)
            self._save_social_data()
            return True
        return False

    def get_friends(self, user_id):
        """Get user's friends"""
        return self.social_data["friends"].get(user_id, [])

    def get_user_posts(self, user_id):
        """Get all posts by a user"""
        return [post for post in self.social_data["posts"].values() if post["user_id"] == user_id]

    def get_feed(self, user_id):
        """Get user's social feed"""
        friends = self.get_friends(user_id)
        feed = []
        
        for post in self.social_data["posts"].values():
            if (post["user_id"] in friends or post["visibility"] == "public"):
                feed.append(post)
        
        return sorted(feed, key=lambda x: x["created_at"], reverse=True)

    def get_active_challenges(self):
        """Get all active challenges"""
        return [challenge for challenge in self.social_data["challenges"].values() 
                if challenge["status"] == "active"]

    def get_user_challenges(self, user_id):
        """Get all challenges a user is participating in"""
        return [challenge for challenge in self.social_data["challenges"].values() 
                if user_id in challenge["participants"]]

    def get_group_members(self, group_id):
        """Get all members of a group"""
        if group_id in self.social_data["groups"]:
            return self.social_data["groups"][group_id]["members"]
        return []

    def get_user_groups(self, user_id):
        """Get all groups a user is a member of"""
        return [group for group in self.social_data["groups"].values() 
                if user_id in group["members"]] 