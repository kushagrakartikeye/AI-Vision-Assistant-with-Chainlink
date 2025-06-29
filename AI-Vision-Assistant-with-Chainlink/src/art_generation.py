import cv2
import numpy as np
import requests
import io
import os
from datetime import datetime
from PIL import Image as PILImage
from tkinter import Toplevel, Button, Frame, Label
from constants import STABILITY_KEY

class ArtGenerator:
    def __init__(self, message_callback=None, display_callback=None):
        self.message_callback = message_callback or print
        self.display_callback = display_callback or (lambda image, filename: None)
    
    def pencil_sketch(self, face_img):
        """Generate high-quality pencil sketch"""
        try:
            face_img = cv2.resize(face_img, (400, 400))
            gray = cv2.c極vtColor(face_img, cv2.COLOR_BGR2GRAY)
            inverted = 255 - gray
            blurred = cv2.GaussianBlur(inverted, (21, 21), 0)
            
            def dodge(front, back):
                result = front * 255 / (255 - back)
                result[result > 255] = 255
                result[back == 255] = 255
                return result.astype('uint8')
            
            pencil = dodge(gray, blurred)
            pencil = cv2.convertScaleAbs(pencil, alpha=1.2, beta=15)
            pencil = cv2.bilateralFilter(pencil, 9, 75, 75)
            
            return cv2.cvtColor(pencil, cv2.COLOR_GRAY2BGR)
        except Exception as e:
            self.message_callback(f"❌ Pencil sketch error: {str(e)}")
            return None
    
    def pixel_art(self, face_img, pixel_size=16, palette=16):
        """Generate pixel art from face image"""
        try:
            small = cv2.resize(face_img, (pixel_size, pixel_size), interpolation=cv2.INTER_LINEAR)
            pixel_art = cv2.resize(small, (400, 400), interpolation=cv2.INTER_NEAREST)
            pil_img = PILImage.fromarray(cv2.cvtColor(pixel_art, cv2.COLOR_BGR2RGB))
            pil_img = pil_img.convert("P", palette=PILImage.ADAPTIVE, colors=palette)
            return cv2.cvtColor(np.array(pil_img.convert("RGB")), cv2.COLOR_RGB2BGR)
        except Exception as e:
            self.message_callback(f"❌ Pixel art error: {str(e)}")
            return None
    
    def generate_ai_art(self, prompt):
        """Generate AI art using Stability AI"""
        try:
            self.message_callback("🎨 Generating art... Please wait...")
            
            response = requests.post(
                "https://api.stability.ai/v2beta/stable-image/generate/sd3",
                headers={
                    "Authorization": f"Bearer {STABILITY_KEY}",
                    "Accept": "image/*"
                },
                files={"none": ''},
                data={
                    "prompt": prompt,
                    "output_format": "png",
                    "model": "sd3-medium"
                },
                timeout=120
            )
            
            if response.status_code == 200:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"saved_art/ai_art_{timestamp}.png"
                os.makedirs("saved_art", exist_ok=True)
                
                with open(filename, 'wb') as f:
                    f.write(response.content)
                
                self.message_callback(f"✅ Art generated and saved as {filename}!")
                return filename, response.content
            else:
                self.message_callback(f"❌ Art generation failed. Status: {response.status_code}")
                return None, None
                
        except Exception as e:
            self.message_callback(f"❌ Art generation error: {str(e)}")
            return None, None
    
    def display_ai_art_window(self, image_data, filename):
        """Display AI art in a new window with save option"""
        try:
            # Convert bytes to PIL Image
            image = PILImage.open(io.BytesIO(image_data))
            
            # Create a new window
            art_window = Toplevel()
            art_window.title("AI Generated Art")
            art_window.geometry("800x900")
            art_window.configure(bg='#2c3e50')
            
            # Display image
            width, height = image.size
            max_width = 700
            max_height = 600
            
            if width > max_width or height > max_height:
                scale = min(max_width/width, max_height/height)
                new_width = int(width * scale)
                new_height = int(height * scale)
                image = image.resize((new_width, new_height))
            
            photo = ImageTk.PhotoImage(image)
            
            img_label = Label(art_window, image=photo, bg='#2c3e50')
            img_label.image = photo
            img_label.pack(pady=20)
            
            # Add controls
            btn_frame = Frame(art_window, bg='#2c3e50')
            btn_frame.pack(pady=20)
            
            save_btn = Button(btn_frame, text="💾 Save to File", 
                            command=lambda: self.save_ai_art(image_data, filename),
                            bg='#3498db', fg='white', font=("Arial", 12, "bold"),
                            relief='flat', padx=20, pady=10)
            save_btn.pack(side="left", padx=10)
            
            close_btn = Button(btn_frame, text="❌ Close", 
                             command=art_window.destroy,
                             bg='#e74c3c', fg='white', font=("Arial", 12, "bold"),
                             relief='flat', padx=20, pady=10)
            close_btn.pack(side="left", padx=10)
            
        except Exception as e:
            self.message_callback(f"❌ Failed to display art: {str(e)}")
    
    def save_ai_art(self, image_data, filename):
        """Save AI art to file"""
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")],
                title="Save AI Art As..."
            )
            if file_path:
                with open(file_path, 'wb') as f:
                    f.write(image_data)
                self.message_callback(f"✅ AI art saved to {file_path}")
        except Exception as e:
            self.message_callback(f"❌ Failed to save AI art: {str(e)}")
