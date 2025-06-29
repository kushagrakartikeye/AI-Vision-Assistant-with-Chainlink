import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox, Toplevel, filedialog
from PIL import Image, ImageTk
import cv2
from constants import VRF_SUBSCRIPTION_ID

class AppGUI:
    def __init__(self, root, message_callback=None):
        self.root = root
        self.message_callback = message_callback or print
        self.setup_gui()
    
    def setup_gui(self):
        self.root.title("Full AI Vision Assistant with Chainlink")
        self.root.geometry("1600x1000")
        self.root.configure(bg='#2c3e50')
        
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left panel - Video
        left_panel = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=2)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Video display
        self.video_label = tk.Label(left_panel, text="Click 'Start Camera' to begin", 
                                  bg='#34495e', fg='#ecf0f1', font=("Arial", 14))
        self.video_label.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Video controls
        video_controls = tk.Frame(left_panel, bg='#34495e')
        video_controls.pack(fill="x", padx=10, pady=10)
        
        self.camera_btn = tk.Button(video_controls, text="📷 Start Camera", 
                                  bg='#27ae60', fg='white',
                                  font=("Arial", 12, "bold"), relief='flat', padx=20, pady=8)
        self.camera_btn.pack(side="left", padx=5)
        
        self.register_btn = tk.Button(video_controls, text="👤 Register Face", 
                                    bg='#3498db', fg='white',
                                    font=("Arial", 12, "bold"), relief='flat', padx=20, pady=8)
        self.register_btn.pack(side="left", padx=5)
        
        # Status display
        self.status_label = tk.Label(video_controls, text="Ready", bg='#34495e', fg='#ecf0f1', font=("Arial", 10))
        self.status_label.pack(side="right", padx=10)
        
        # Right panel - Chat
        right_panel = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=2, width=500)
        right_panel.pack(side="right", fill="both", padx=(5, 0))
        right_panel.pack_propagate(False)
        
        # Chainlink Data Panel
        data_frame = tk.Frame(right_panel, bg='#2c3e50', relief='sunken', bd=1)
        data_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(data_frame, text="📡 Chainlink Live Data", 
                bg='#2c3e50', fg='#ecf0f1', font=("Arial", 12, "bold")).pack(anchor="w", padx=5, pady=2)
        
        # Crypto prices from Chainlink
        self.eth_price_label = tk.Label(data_frame, text="ETH/USD: Loading...", 
                                      bg='#2c3e50', fg='#ecf0f1', font=("Arial", 10))
        self.eth_price_label.pack(anchor="w", padx=5, pady=2)
        
        self.btc_price_label = tk.Label(data_frame, text="BTC/USD: Loading...", 
                                      bg='#2c3e50', fg='#ecf0f1', font=("Arial", 10))
        self.btc_price_label.pack(anchor="w", padx=5, pady=2)
        
        self.vrf_status_label = tk.Label(data_frame, text="VRF Status: Ready", 
                                       bg='#2c3e50', fg='#ecf0f1', font=("Arial", 10))
        self.vrf_status_label.pack(anchor="w", padx=5, pady=2)
        
        # Chat components
        self.chat_display = scrolledtext.ScrolledText(
            right_panel, height=25, width=65, bg='#2c3e50', fg='#ecf0f1',
            font=("Consolas", 10), insertbackground='white'
        )
        self.chat_display.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Input area
        input_frame = tk.Frame(right_panel, bg='#34495e')
        input_frame.pack(fill="x", padx=10, pady=10)
        
        self.user_input = tk.Entry(input_frame, font=("Arial", 11), bg='#2c3e50', 
                                  fg='#ecf0f1', insertbackground='white')
        self.user_input.pack(side="left", fill="x", expand=True, padx=(0, 5), ipady=5)
        
        # Buttons
        self.send_btn = tk.Button(input_frame, text="Send",
                                 bg='#3498db', fg='white', font=("Arial", 10, "bold"),
                                 relief='flat', padx=15)
        self.send_btn.pack(side="right", padx=2)
        
        self.voice_btn = tk.Button(input_frame, text="🎤",
                                  bg='#e74c3c', fg='white', font=("Arial", 12, "bold"),
                                  relief='flat', width=3)
        self.voice_btn.pack(side="right", padx=2)
        
        self.art_btn = tk.Button(input_frame, text="🎨",
                                bg='#9b59b6', fg='white', font=("Arial", 12, "bold"),
                                relief='flat', width=3)
        self.art_btn.pack(side="right", padx=2)
        
        self.sketch_btn = tk.Button(input_frame, text="✏️ Sketch",
                                   bg='#f39c12', fg='white', font=("Arial", 12, "bold"),
                                   relief='flat', width=8)
        self.sketch_btn.pack(side="right", padx=2)
        
        # Art display
        self.art_label = tk.Label(right_panel, bg='#34495e', text="Sketch Preview")
        self.art_label.pack(pady=5)
        
        self.add_message("System", "🚀 AI Vision Assistant with Chainlink Ready!")
    
    def add_message(self, sender, message):
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"[{timestamp}] {sender}: {message}\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def update_video_display(self, frame):
        try:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width = rgb_frame.shape[:2]
            max_width = 800
            max_height = 600
            
            if width > max_width or height > max_height:
                scale = min(max_width/width, max_height/height)
                new_width = int(width * scale)
                new_height = int(height * scale)
                rgb_frame = cv2.resize(rgb_frame, (new_width, new_height))
            
            img = Image.fromarray(rgb_frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.config(image=imgtk)
            self.video_label.image = imgtk
            
        except Exception as e:
            pass
    
    def update_crypto_prices(self, eth_price, btc_price):
        if eth_price and btc_price:
            self.eth_price_label.config(text=f"ETH/USD: ${eth_price:,.2f}")
            self.btc_price_label.config(text=f"BTC/USD: ${btc_price:,.2f}")
            self.vrf_status_label.config(text=f"VRF Sub ID: {VRF_SUBSCRIPTION_ID[:10]}...")
    
    def display_sketch_window(self, sketch, filename, nft_callback=None, save_callback=None):
        sketch_window = Toplevel(self.root)
        sketch_window.title("AI Generated Sketch - Ready for Chainlink VRF NFT")
        sketch_window.geometry("800x900")
        sketch_window.configure(bg='#2c3e50')
        
        sketch_rgb = cv2.cvtColor(sketch, cv2.COLOR_BGR2RGB)
        height, width = sketch_rgb.shape[:2]
        max_width = 700
        max_height = 600
        
        if width > max_width or height > max_height:
            scale = min(max_width/width, max_height/height)
            new_width = int(width * scale)
            new_height = int(height * scale)
            sketch_rgb = cv2.resize(sketch_rgb, (new_width, new_height))
        
        img = Image.fromarray(sketch_rgb)
        photo = ImageTk.PhotoImage(img)
        
        img_label = tk.Label(sketch_window, image=photo, bg='#2c3e50')
        img_label.image = photo
        img_label.pack(pady=20)
        
        btn_frame = tk.Frame(sketch_window, bg='#2c3e50')
        btn_frame.pack(pady=20)
        
        if save_callback:
            save_btn = tk.Button(btn_frame, text="💾 Save to File", 
                               command=lambda: save_callback(sketch),
                               bg='#3498db', fg='white', font=("Arial", 12, "bold"),
                               relief='flat', padx=20, pady=10)
            save_btn.pack(side="left", padx=10)
        
        if nft_callback:
            nft_btn = tk.Button(btn_frame, text="🔗 Mint NFT with Chainlink VRF", 
                              command=lambda: nft_callback(sketch, filename),
                              bg='#9b59b6', fg='white', font=("Arial", 12, "bold"),
                              relief='flat', padx=20, pady=10)
            nft_btn.pack(side="left", padx=10)
        
        close_btn = tk.Button(btn_frame, text="❌ Close", 
                            command=sketch_window.destroy,
                            bg='#e74c3c', fg='white', font=("Arial", 12, "bold"),
                            relief='flat', padx=20, pady=10)
        close_btn.pack(side="left", padx=10)
