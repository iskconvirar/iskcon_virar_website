# iskconapp/storage_backends.py
import os
from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from django.utils.deconstruct import deconstructible
from supabase import create_client, Client
import uuid

@deconstructible
class SupabaseStorage(Storage):
    def __init__(self):
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_ANON_KEY')
        self.bucket_name = os.getenv('SUPABASE_BUCKET', 'images')
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set")
        
        self.client: Client = create_client(self.supabase_url, self.supabase_key)
    
    def _save(self, name, content):
        # Generate unique filename to avoid conflicts
        file_extension = name.split('.')[-1] if '.' in name else ''
        unique_name = f"{uuid.uuid4()}.{file_extension}" if file_extension else str(uuid.uuid4())
        
        try:
            # Read file content
            content.seek(0)
            file_data = content.read()
            
            # Upload to Supabase Storage
            response = self.client.storage.from_(self.bucket_name).upload(
                unique_name, 
                file_data,
                file_options={
                    "cache-control": "3600",
                    "upsert": "false"
                }
            )
            
            if response.status_code == 200:
                return unique_name
            else:
                raise Exception(f"Upload failed: {response}")
                
        except Exception as e:
            raise Exception(f"Failed to upload file: {str(e)}")
    
    def _open(self, name, mode='rb'):
        try:
            response = self.client.storage.from_(self.bucket_name).download(name)
            return ContentFile(response, name=name)
        except Exception as e:
            raise Exception(f"Failed to open file: {str(e)}")
    
    def delete(self, name):
        try:
            response = self.client.storage.from_(self.bucket_name).remove([name])
            return response.status_code == 200
        except Exception:
            return False
    
    def exists(self, name):
        try:
            response = self.client.storage.from_(self.bucket_name).list(
                path="", 
                search=name
            )
            return len(response) > 0
        except Exception:
            return False
    
    def url(self, name):
        try:
            response = self.client.storage.from_(self.bucket_name).get_public_url(name)
            return response
        except Exception:
            return None
    
    def size(self, name):
        # Supabase doesn't provide direct size info easily
        # You might need to implement this based on your needs
        return 0