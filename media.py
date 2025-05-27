import os
import json
import uuid
from datetime import datetime
from PIL import Image
import cv2
import numpy as np

class MediaManager:
    def __init__(self):
        self.media_dir = "media"
        self.media_data_file = "media_data.json"
        self.allowed_image_types = ['.jpg', '.jpeg', '.png', '.gif']
        self.allowed_video_types = ['.mp4', '.avi', '.mov']
        self.max_image_size = (1920, 1080)  # Maximum dimensions for images
        self.max_video_size = 100 * 1024 * 1024  # 100MB maximum video size
        
        # Create necessary directories
        if not os.path.exists(self.media_dir):
            os.makedirs(self.media_dir)
        for subdir in ['images', 'videos', 'thumbnails']:
            path = os.path.join(self.media_dir, subdir)
            if not os.path.exists(path):
                os.makedirs(path)
        
        self.media_data = self._load_media_data()

    def _load_media_data(self):
        """Load media data from JSON file"""
        if os.path.exists(self.media_data_file):
            with open(self.media_data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"images": {}, "videos": {}}

    def _save_media_data(self):
        """Save media data to JSON file"""
        with open(self.media_data_file, 'w', encoding='utf-8') as f:
            json.dump(self.media_data, f, ensure_ascii=False, indent=4)

    def upload_image(self, user_id, image_path, description=None, tags=None):
        """Upload and process an image"""
        try:
            # Check file type
            ext = os.path.splitext(image_path)[1].lower()
            if ext not in self.allowed_image_types:
                return None, "Invalid file type"

            # Generate unique filename
            filename = f"{uuid.uuid4()}{ext}"
            target_path = os.path.join(self.media_dir, 'images', filename)

            # Process and save image
            with Image.open(image_path) as img:
                # Resize if necessary
                if img.size[0] > self.max_image_size[0] or img.size[1] > self.max_image_size[1]:
                    img.thumbnail(self.max_image_size)
                
                # Save processed image
                img.save(target_path, quality=85, optimize=True)

            # Create thumbnail
            thumbnail_path = os.path.join(self.media_dir, 'thumbnails', f"thumb_{filename}")
            with Image.open(target_path) as img:
                img.thumbnail((300, 300))
                img.save(thumbnail_path, quality=85, optimize=True)

            # Save metadata
            image_id = str(uuid.uuid4())
            self.media_data["images"][image_id] = {
                "id": image_id,
                "user_id": user_id,
                "filename": filename,
                "thumbnail": f"thumb_{filename}",
                "description": description,
                "tags": tags or [],
                "upload_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "type": "image"
            }
            self._save_media_data()

            return image_id, "Success"
        except Exception as e:
            return None, str(e)

    def upload_video(self, user_id, video_path, description=None, tags=None):
        """Upload and process a video"""
        try:
            # Check file type
            ext = os.path.splitext(video_path)[1].lower()
            if ext not in self.allowed_video_types:
                return None, "Invalid file type"

            # Check file size
            if os.path.getsize(video_path) > self.max_video_size:
                return None, "File too large"

            # Generate unique filename
            filename = f"{uuid.uuid4()}{ext}"
            target_path = os.path.join(self.media_dir, 'videos', filename)

            # Process video
            cap = cv2.VideoCapture(video_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = frame_count / fps

            # Save video
            os.rename(video_path, target_path)

            # Generate thumbnail
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count // 2)
            ret, frame = cap.read()
            if ret:
                thumbnail_path = os.path.join(self.media_dir, 'thumbnails', f"thumb_{filename}.jpg")
                cv2.imwrite(thumbnail_path, frame)
            cap.release()

            # Save metadata
            video_id = str(uuid.uuid4())
            self.media_data["videos"][video_id] = {
                "id": video_id,
                "user_id": user_id,
                "filename": filename,
                "thumbnail": f"thumb_{filename}.jpg",
                "description": description,
                "tags": tags or [],
                "upload_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "duration": duration,
                "fps": fps,
                "type": "video"
            }
            self._save_media_data()

            return video_id, "Success"
        except Exception as e:
            return None, str(e)

    def get_media_info(self, media_id):
        """Get information about a media file"""
        if media_id in self.media_data["images"]:
            return self.media_data["images"][media_id]
        elif media_id in self.media_data["videos"]:
            return self.media_data["videos"][media_id]
        return None

    def get_user_media(self, user_id, media_type=None):
        """Get all media files uploaded by a user"""
        media = []
        if media_type is None or media_type == "image":
            media.extend([m for m in self.media_data["images"].values() if m["user_id"] == user_id])
        if media_type is None or media_type == "video":
            media.extend([m for m in self.media_data["videos"].values() if m["user_id"] == user_id])
        return sorted(media, key=lambda x: x["upload_date"], reverse=True)

    def delete_media(self, media_id):
        """Delete a media file and its metadata"""
        media_info = self.get_media_info(media_id)
        if media_info:
            # Delete files
            if media_info["type"] == "image":
                os.remove(os.path.join(self.media_dir, 'images', media_info["filename"]))
                os.remove(os.path.join(self.media_dir, 'thumbnails', media_info["thumbnail"]))
                del self.media_data["images"][media_id]
            elif media_info["type"] == "video":
                os.remove(os.path.join(self.media_dir, 'videos', media_info["filename"]))
                os.remove(os.path.join(self.media_dir, 'thumbnails', media_info["thumbnail"]))
                del self.media_data["videos"][media_id]
            
            self._save_media_data()
            return True
        return False

    def search_media(self, query, media_type=None):
        """Search for media files by tags or description"""
        results = []
        
        if media_type is None or media_type == "image":
            for media in self.media_data["images"].values():
                if (query.lower() in media["description"].lower() if media["description"] else False or
                    any(query.lower() in tag.lower() for tag in media["tags"])):
                    results.append(media)
        
        if media_type is None or media_type == "video":
            for media in self.media_data["videos"].values():
                if (query.lower() in media["description"].lower() if media["description"] else False or
                    any(query.lower() in tag.lower() for tag in media["tags"])):
                    results.append(media)
        
        return sorted(results, key=lambda x: x["upload_date"], reverse=True)

    def get_media_url(self, media_id):
        """Get the URL for a media file"""
        media_info = self.get_media_info(media_id)
        if media_info:
            if media_info["type"] == "image":
                return os.path.join(self.media_dir, 'images', media_info["filename"])
            elif media_info["type"] == "video":
                return os.path.join(self.media_dir, 'videos', media_info["filename"])
        return None

    def get_thumbnail_url(self, media_id):
        """Get the URL for a media thumbnail"""
        media_info = self.get_media_info(media_id)
        if media_info:
            return os.path.join(self.media_dir, 'thumbnails', media_info["thumbnail"])
        return None 