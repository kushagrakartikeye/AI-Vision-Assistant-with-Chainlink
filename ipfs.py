import cv2
import requests
from constants import IPFS_PROJECT_ID, IPFS_SECRET

class IPFSManager:
    def __init__(self, message_callback=None):
        self.message_callback = message_callback or print
    
    def upload_image_to_ipfs(self, image):
        try:
            _, buffer = cv2.imencode('.png', image)
            file_bytes = buffer.tobytes()
            
            url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
            files = {'file': ('sketch.png', file_bytes, 'image/png')}
            headers = {
                'pinata_api_key': IPFS_PROJECT_ID,
                'pinata_secret_api_key': IPFS_SECRET
            }
            
            response = requests.post(url, files=files, headers=headers)
            
            if response.status_code == 200:
                ipfs_hash = response.json()['IpfsHash']
                self.message_callback(f"📁 Image uploaded to IPFS: {ipfs_hash}")
                return ipfs_hash
            else:
                self.message_callback(f"❌ IPFS upload failed: {response.status_code}")
                return None
                
        except Exception as e:
            self.message_callback(f"❌ IPFS upload error: {str(e)}")
            return None
    
    def upload_metadata_to_ipfs(self, metadata):
        try:
            url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
            headers = {
                'Content-Type': 'application/json',
                'pinata_api_key': IPFS_PROJECT_ID,
                'pinata_secret_api_key': IPFS_SECRET
            }
            
            response = requests.post(url, json=metadata, headers=headers)
            
            if response.status_code == 200:
                ipfs_hash = response.json()['IpfsHash']
                self.message_callback(f"📝 Metadata uploaded to IPFS: {ipfs_hash}")
                return ipfs_hash
            else:
                self.message_callback(f"❌ Metadata upload failed: {response.status_code}")
                return None
                
        except Exception as e:
            self.message_callback(f"❌ Metadata upload error: {str(e)}")
            return None
