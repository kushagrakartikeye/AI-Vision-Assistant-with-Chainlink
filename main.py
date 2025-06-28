import os
import cv2
import threading
import time
import requests
import io
from datetime import datetime
from tkinter import simpledialog, messagebox, filedialog
import numpy as np
import hashlib
import json

# Import custom modules
from constants import *
from blockchain import BlockchainManager
from ipfs import IPFSManager
from vision_processing import VisionProcessor
from speech import SpeechProcessor
from art_generation import ArtGenerator
from gui import AppGUI

# Set up environment
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

class FullAIVisionAssistant:
    def __init__(self):
        import tkinter as tk
        self.root = tk.Tk()
        
        # Initialize GUI first
        self.gui = AppGUI(self.root, self.add_message)
        
        # Create system message callback
        def system_callback(msg):
            self.add_message("System", msg)
        
        # Initialize all components with wrapped callback
        self.blockchain = BlockchainManager(system_callback)
        self.ipfs = IPFSManager(system_callback)
        self.vision = VisionProcessor(system_callback)
        self.speech = SpeechProcessor(system_callback)
        self.art = ArtGenerator(system_callback)
        
        # Video capture
        self.cap = None
        self.video_running = False
        self.frame_lock = threading.Lock()
        self.last_detection_time = {}
        self.unknown_face_cooldown = {}
        
        # Bind GUI events
        self.setup_gui_events()
        
        # Start periodic updates
        self.update_crypto_prices()
        
    def setup_gui_events(self):
        self.gui.camera_btn.config(command=self.toggle_camera)
        self.gui.register_btn.config(command=self.manual_register_face)
        self.gui.user_input.bind("<Return>", self.send_message)
        self.gui.send_btn.config(command=self.send_message)
        self.gui.voice_btn.config(command=self.voice_input)
        self.gui.art_btn.config(command=self.generate_art)
        self.gui.sketch_btn.config(command=self.sketch_detected_face)
    
    def add_message(self, sender, message):
        self.gui.add_message(sender, message)
    
    def toggle_camera(self):
        if not self.video_running:
            self.cap = cv2.VideoCapture(0)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            
            if self.cap.isOpened():
                self.video_running = True
                self.gui.camera_btn.config(text="🛑 Stop Camera", bg='#e74c3c')
                self.video_thread = threading.Thread(target=self.video_loop, daemon=True)
                self.video_thread.start()
                self.add_message("System", "📹 Camera started")
        else:
            self.video_running = False
            if self.cap:
                self.cap.release()
            cv2.destroyAllWindows()
            self.gui.camera_btn.config(text="📷 Start Camera", bg='#27ae60')
            self.add_message("System", "📹 Camera stopped")
    
    def video_loop(self):
        while self.video_running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
            
            processed_frame, face_count = self.vision.process_frame(frame.copy())
            self.gui.update_video_display(processed_frame)
            
            # Auto-detect unknown faces and offer registration
            self.check_for_unknown_faces(frame, face_count)
            time.sleep(0.02)
    
    def check_for_unknown_faces(self, frame, face_count):
        """Check for unknown faces and offer registration"""
        try:
            import face_recognition
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            
            current_time = time.time()
            
            for i, (face_encoding, (top, right, bottom, left)) in enumerate(zip(face_encodings, face_locations)):
                matches = face_recognition.compare_faces(self.vision.known_face_encodings, face_encoding, tolerance=0.6)
                
                if not any(matches):  # Unknown face detected
                    face_key = f"unknown_{i}"
                    if face_key not in self.unknown_face_cooldown or current_time - self.unknown_face_cooldown[face_key] > 60:
                        self.unknown_face_cooldown[face_key] = current_time
                        face_img = frame[top:bottom, left:right]
                        threading.Thread(target=self.auto_register_unknown_face, args=(face_img,), daemon=True).start()
                else:
                    # Known face - greet if not greeted recently
                    first_match_index = matches.index(True)
                    name = self.vision.known_face_names[first_match_index]
                    if name not in self.last_detection_time or current_time - self.last_detection_time[name] > 30:
                        self.add_message("System", f"👋 Hello {name}! Welcome back!")
                        self.speech.speak(f"Hello {name}! Welcome back!")
                        self.last_detection_time[name] = current_time
                        
        except Exception as e:
            pass  # Silently handle any face detection errors
    
    def auto_register_unknown_face(self, face_img):
        try:
            def register_dialog():
                result = messagebox.askyesno(
                    "Unknown Face Detected", 
                    "I detected an unknown face. Would you like to register this person?"
                )
                if result:
                    name = simpledialog.askstring("Register Face", "Please enter the person's name:")
                    if name and name.strip():
                        success = self.vision.register_face(face_img, name.strip())
                        if success:
                            face_hash = self.vision.generate_face_hash(face_img)
                            tx_hash = self.blockchain.register_user_on_blockchain(face_hash)
                            if tx_hash:
                                self.add_message("System", f"🔗 Blockchain registration: {tx_hash}")
                            self.add_message("System", f"✅ Successfully registered {name}!")
                            self.speech.speak(f"Hello {name}! Nice to meet you. I've registered your face.")
            
            self.root.after(0, register_dialog)
        except Exception as e:
            self.add_message("System", f"❌ Auto-registration error: {str(e)}")
    
    def manual_register_face(self):
        if not self.video_running:
            messagebox.showwarning("Warning", "Please start the camera first!")
            return
            
        name = simpledialog.askstring("Register Face", "Enter the person's name:")
        if name and name.strip():
            ret, frame = self.cap.read()
            if ret:
                success = self.vision.register_face(frame, name.strip())
                if success:
                    face_hash = self.vision.generate_face_hash(frame)
                    tx_hash = self.blockchain.register_user_on_blockchain(face_hash)
                    if tx_hash:
                        self.add_message("System", f"🔗 Blockchain registration: {tx_hash}")
                    self.add_message("System", f"✅ Successfully registered {name}!")
                    self.speech.speak(f"Hello {name}! Nice to meet you. I've registered your face.")
    
    def sketch_detected_face(self):
        if not self.video_running:
            self.add_message("System", "❌ Please start the camera first!")
            return
            
        ret, frame = self.cap.read()
        if not ret:
            self.add_message("System", "❌ Failed to capture frame!")
            return
            
        import face_recognition
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        
        if not face_locations:
            self.add_message("System", "❌ No faces detected in current frame!")
            return
            
        # Ask user for art style
        style = simpledialog.askstring(
            "Select Art Style",
            "Enter art style:\n'pencil' for Pencil Sketch\n'pixel' for Pixel Art",
            parent=self.root
        )
        if not style:
            return
        style = style.strip().lower()
        
        try:
            top, right, bottom, left = face_locations[0]
            face_img = frame[top:bottom, left:right]
            
            if style == "pixel":
                sketch = self.art.pixel_art(face_img)
            else:
                sketch = self.art.pencil_sketch(face_img)
            
            if sketch is not None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                sketch_filename = f"saved_art/sketch_{timestamp}_{style}.png"
                os.makedirs("saved_art", exist_ok=True)
                cv2.imwrite(sketch_filename, sketch)
                
                # Display sketch window with callbacks
                self.gui.display_sketch_window(
                    sketch, 
                    sketch_filename,
                    nft_callback=self.mint_sketch_as_nft,
                    save_callback=self.save_sketch_to_file
                )
                
                # Update art preview
                sketch_rgb = cv2.cvtColor(sketch, cv2.COLOR_BGR2RGB)
                from PIL import Image
                img = Image.fromarray(sketch_rgb).resize((200, 200))
                from PIL import ImageTk
                self.art_image = ImageTk.PhotoImage(img)
                self.gui.art_label.config(image=self.art_image)
                self.gui.art_label.image = self.art_image
                self.add_message("System", f"✅ {style.capitalize()} art generated!")
                
        except Exception as e:
            self.add_message("System", f"❌ Sketch generation failed: {str(e)}")
    
    def save_sketch_to_file(self, sketch):
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")],
                title="Save Sketch As..."
            )
            if file_path:
                cv2.imwrite(file_path, sketch)
                self.add_message("System", f"✅ Sketch saved to {file_path}")
                messagebox.showinfo("Success", f"Sketch saved successfully!")
        except Exception as e:
            self.add_message("System", f"❌ Failed to save sketch: {str(e)}")
    
    def mint_sketch_as_nft(self, sketch, filename):
        """Mint sketch as NFT using Chainlink VRF"""
        try:
            result = messagebox.askyesno("Mint NFT with Chainlink VRF", 
                                       f"Do you want to mint this sketch as an NFT?\n\n"
                                       f"This will:\n"
                                       f"1. Upload image to IPFS\n"
                                       f"2. Create metadata\n"
                                       f"3. Use Chainlink VRF for randomness\n"
                                       f"4. Mint NFT on Sepolia testnet\n"
                                       f"5. Require test ETH for gas fees\n\n"
                                       f"Make sure your VRF subscription is funded with LINK!")
            
            if result:
                self.add_message("System", "🔗 Starting Chainlink VRF NFT minting...")
                self.gui.vrf_status_label.config(text="VRF Status: Minting...")
                threading.Thread(target=self._mint_nft_process, args=(sketch, filename), daemon=True).start()
                
        except Exception as e:
            self.add_message("System", f"❌ NFT minting failed: {str(e)}")
    
    def _mint_nft_process(self, sketch, filename):
        """Background NFT minting process"""
        try:
            # Upload to IPFS
            self.add_message("System", "📁 Uploading sketch to IPFS...")
            ipfs_hash = self.ipfs.upload_image_to_ipfs(sketch)
            
            if not ipfs_hash:
                self.gui.vrf_status_label.config(text="VRF Status: Failed")
                return
            
            # Create metadata
            self.add_message("System", "📝 Creating NFT metadata...")
            metadata = {
                "name": f"AI Vision Sketch #{int(time.time())}",
                "description": "AI-generated sketch with Chainlink VRF randomness",
                "image": f"ipfs://{ipfs_hash}",
                "attributes": [
                    {"trait_type": "Creation Method", "value": "AI Sketch Generation"},
                    {"trait_type": "Timestamp", "value": datetime.now().isoformat()},
                    {"trait_type": "Randomness Source", "value": "Chainlink VRF"},
                    {"trait_type": "Network", "value": "Ethereum Sepolia"}
                ]
            }
            
            metadata_hash = self.ipfs.upload_metadata_to_ipfs(metadata)
            if not metadata_hash:
                self.gui.vrf_status_label.config(text="VRF Status: Failed")
                return
            
            # Mint NFT
            self.add_message("System", "⛏️ Requesting Chainlink VRF for NFT minting...")
            metadata_uri = f"ipfs://{metadata_hash}"
            tx_hash = self.blockchain.request_nft_mint(metadata_uri)
            
            if tx_hash:
                self.add_message("System", f"✅ VRF NFT request sent! TX: {tx_hash}")
                self.add_message("System", f"🔍 View on Etherscan: https://sepolia.etherscan.io/tx/{tx_hash}")
                self.gui.vrf_status_label.config(text="VRF Status: Pending...")
                
                # Monitor fulfillment
                success, message = self.blockchain.monitor_vrf_fulfillment(tx_hash)
                if success:
                    self.gui.vrf_status_label.config(text="VRF Status: Complete")
                    messagebox.showinfo("Success", f"NFT minted successfully!\n{message}")
                else:
                    self.gui.vrf_status_label.config(text="VRF Status: Failed")
                    self.add_message("System", f"❌ {message}")
            else:
                self.gui.vrf_status_label.config(text="VRF Status: Failed")
                
        except Exception as e:
            self.add_message("System", f"❌ NFT minting failed: {str(e)}")
            self.gui.vrf_status_label.config(text="VRF Status: Error")
    
    def send_message(self, event=None):
        message = self.gui.user_input.get().strip()
        if message:
            self.add_message("You", message)
            self.gui.user_input.delete(0, 'end')
            context = self.get_vision_context()
            threading.Thread(target=self.process_chat_response, args=(message, context), daemon=True).start()
    
    def process_chat_response(self, message, context):
        response = self.get_chat_response(message, context)
        self.add_message("AI", response)
        self.speech.speak(response)
    
    def get_vision_context(self):
        context = []
        if self.video_running:
            context.append("Camera is active")
            if self.vision.known_face_names:
                context.append(f"Known faces: {', '.join(self.vision.known_face_names)}")
        return "; ".join(context)
    
    def get_chat_response(self, message, context):
        try:
            headers = {
                "Authorization": f"Bearer {OPENROUTER_KEY}",
                "Content-Type": "application/json"
            }
            
            system_prompt = f"""You are an AI vision assistant with face recognition, object detection, and Chainlink blockchain integration. 
            Current context: {context}. 
            You can see through the camera, recognize faces, detect objects, generate art, and mint NFTs with Chainlink VRF on Ethereum Sepolia testnet.
            Be helpful, friendly, and concise in your responses."""
            
            data = {
                "model": "mistralai/mistral-7b-instruct",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                "max_tokens": 200,
                "temperature": 0.7
            }
            
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content'].strip()
            else:
                return f"I'm having trouble connecting. Status: {response.status_code}"
                
        except Exception as e:
            return f"Sorry, I'm experiencing technical difficulties: {str(e)}"
    
    def voice_input(self):
        def listen():
            text = self.speech.listen()
            if text:
                self.add_message("You (Voice)", text)
                context = self.get_vision_context()
                response = self.get_chat_response(text, context)
                self.add_message("AI", response)
                self.speech.speak(response)
        
        threading.Thread(target=listen, daemon=True).start()
    
    def generate_art(self):
        prompt = simpledialog.askstring("AI Art Generator", "Enter your artistic prompt:")
        if prompt:
            self.add_message("You", f"🎨 Generate art: {prompt}")
            
            def create_art():
                filename, content = self.art.generate_ai_art(prompt)
                if content:
                    # Display in new window
                    self.art.display_ai_art_window(content, filename)
                    
                    # Update preview in main GUI
                    from PIL import Image
                    image = Image.open(io.BytesIO(content))
                    image = image.resize((200, 200))
                    from PIL import ImageTk
                    self.art_image = ImageTk.PhotoImage(image)
                    self.gui.art_label.config(image=self.art_image)
                    self.gui.art_label.image = self.art_image
            
        threading.Thread(target=create_art, daemon=True).start()

    
    def update_crypto_prices(self):
        """Update crypto prices every 30 seconds"""
        try:
            eth_price, btc_price = self.blockchain.get_crypto_prices()
            self.gui.update_crypto_prices(eth_price, btc_price)
        except Exception as e:
            pass
        
        # Schedule next update
        self.root.after(30000, self.update_crypto_prices)
    
    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def on_closing(self):
        self.video_running = False
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        self.root.destroy()

if __name__ == "__main__":
    # Create necessary directories
    os.makedirs(KNOWN_FACES_DIR, exist_ok=True)
    os.makedirs("saved_art", exist_ok=True)
    
    # Run the application
    app = FullAIVisionAssistant()
    app.run()
