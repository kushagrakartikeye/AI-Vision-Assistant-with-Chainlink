# AI Vision Assistant with Chainlink Integration

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Chainlink](https://img.shields.io/badge/Chainlink-VRF-green)
![Ethereum](https://img.shields.io/badge/Ethereum-Sepolia-purple)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8-orange)
![Stability AI](https://img.shields.io/badge/Stability%20AI-SD3-lightgrey)

An advanced AI assistant combining computer vision, facial recognition, blockchain technology, and conversational AI. Features real-time crypto data feeds via Chainlink and verifiably random NFT generation using Chainlink VRF.

---

## ✨ What It Can Do

Here’s every major feature and capability of this project:

- **Real-time Face Recognition with YOLOv8**: Instantly recognizes and identifies faces from your webcam.
- **Object Detection**: Detects and labels objects in the camera feed using YOLOv8.
- **Face Registration with Blockchain Storage**: Registers new users by capturing their face and storing a unique hash on the Ethereum blockchain.
- **Auto-Sketch Generation (Pencil and Pixel Art)**: Automatically converts detected faces into artistic sketches.
- **AI Art Generation using Stability AI**: Generates images from text prompts using state-of-the-art AI models.
- **Chainlink VRF Integration for Verifiable Randomness in NFT Minting**: Ensures NFT minting is provably random using Chainlink VRF.
- **IPFS Storage for Decentralized NFT Metadata**: Stores NFT images and metadata on IPFS via Pinata for true decentralization.
- **Voice Interaction with Speech Recognition and Text-to-Speech**: Lets you interact by voice—both speaking and listening.
- **Contextual Chatbot powered by OpenRouter AI**: Answers your questions, provides context-aware responses, and assists with commands.
- **Real-time Cryptocurrency Price Display via Chainlink Data Feeds**: Shows live ETH and BTC prices directly from Chainlink.
- **NFT Minting with Chainlink VRF on Ethereum Sepolia Testnet**: Mints unique NFTs with verifiable randomness, all on testnet for safe experimentation.
- **User-friendly GUI with Tkinter**: Easy-to-use graphical interface for all features.
- **Manual and Automatic Face Registration**: Register faces either manually or automatically when new faces are detected.
- **Sketch and AI Art Display in Separate Windows**: View generated sketches and AI art in dedicated windows for better user experience.
- **Integration with Alchemy Ethereum RPC**: Connects seamlessly to the Ethereum network for blockchain operations.
- **Secure Key Management via Environment Variables**: Keeps your API keys and private data safe using `.env` files.
- **Modular Code Structure for Maintainability**: Well-organized codebase for easy updates and collaboration.
- **Performance Optimizations for Real-time Processing**: Efficient algorithms for smooth, real-time operation.

---

## 📂 Project Structure

AI-Vision-Assistant-with-Chainlink/
├── src/ # All source code and contract ABI
├── screenshots/ # screenshots for demo
├── requirements.txt # Python dependencies
├── .env.example # Environment variable template
├── .gitignore # Files/directories to ignore
└── README.md # Project documentation


---

## 🚀 Quick Start

1. **Clone repository**
git clone https://github.com/kushagrakartikeye/AI-Vision-Assistant-with-Chainlink.git
cd AI-Vision-Assistant-with-Chainlink

text

2. **Install dependencies**
pip install -r requirements.txt

text

3. **Download model** (place in project root)
- [yolov8n.pt](https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt)

4. **Setup environment**
- Copy `.env.example` to `.env`
- Add your API keys

5. **Run application**
python main.py

text

---

## 🔗 Blockchain Details

- **Contract**: `0xE04C1491d38C4e9C4611E2D7AB1FB23422898735`
- **Network**: Ethereum Sepolia Testnet
- **VRF Subscription**: `823483...7559`

---

## 📸 Demo

Screenshot	Description
![Interface](https://github.com/user-attachments/assets/f26734b1-8337-42c7-a932-b1d52976929a)(screenshots Main Interface: The application's main dashboard, showing the AI Vision Assistant GUI with live camera feed, chat window, and controls.

![art![art_generation_prompt](https://github.com/user-attachments/assets/e1fba6b3-b3de-439f-aa87-fff0299bd5a7)(screenshots/art_generation AI Art Generation Prompt: User entering a text prompt to generate AI art using Stability AI.	

![![chatbot_description](https://github.com/user-attachments/assets/fb08cad8-c03d-4282-a9ea-2f7e47bcaf96)(screenshots/chatbot_description:** The chatbot interface, demonstrating contextual AI conversation and assistant capabilities.	

![chatbot_uniqueness](https://github.com/user-attachments/assets/30499b78-ad96-46ae-a43e-664ec68b4d8a)(screenshots/chatbot_uni Chatbot Uniqueness: Highlights the chatbot's unique, context-aware responses and integration with vision features.	

![enviorment_description](https://github.com/user-attachments/assets/c40a391e-bbf6-492a-9bf6-859fe72a377b)(screenshots/enviorment_description:** Shows how the assistant can describe the user's environment and detected objects.	\

![generated_art1](https://github.com/user-attachments/assets/1109aebb-230e-4d5d-86e2-de25138089ee)(screenshots Generated AI Art #1: Example output from the AI art generator, demonstrating creative image synthesis.	

![generated_art2](https://github.com/user-attachments/assets/b30a545e-412f-4db0-ab05-9d7062304f05)(screenshots Generated AI Art #2: Another example of AI-generated artwork, showing the diversity of styles possible.	

![generation_success](https://github.com/user-attachments/assets/eac3ce48-157f-4e5d-a010-2a1b33ca7936)(screenshots/generation_success Success:** Confirmation message after successful AI art or sketch generation.	

![new_register](https://github.com/user-attachments/assets/b98a55d4-7c48-4232-9e38-2a62fb26ff12)(screenshots New Face Registration: The process of registering a new user’s face in the system, with blockchain integration.	

![object_detection](https://github.com/user-attachments/assets/fe8867d9-c94a-45cf-afd4-f076d771d435)(screenshots/object_detection.jpg:** Live detection and labeling of objects in the camera feed using YOLOv8.	

![object_recogniton_animal](https://github.com/user-attachments/assets/ff25391b-3e72-472a-880c-02a44103a854)(screenshots/object_recogn Object Recognition (Animal): The system detects and recognizes animals in the camera frame.	

![pinata_dashboard](https://github.com/user-attachments/assets/2b6df916-de78-4c0a-9e68-b388bf7fe095)(screenshots/pinata_dashboard.jpg:** Shows the Pinata IPFS dashboard where NFT images and metadata are stored.	

![registered_faces](https://github.com/user-attachments/assets/15532e64-d5dd-407d-8af0-8a680703ec03)(screenshots/registered_faces.jpg:** List of users whose faces are registered and recognized by the assistant.	

![sketch_generation](https://github.com/user-attachments/assets/99ef6262-cdaa-4d85-b770-b1cd7aeb6978)(screenshots/sketch_generation:** Example of a pencil or pixel sketch generated from a detected face.

---

## 🏆 Hackathon Submission

This project demonstrates:
- ✅ Chainlink VRF integration for verifiable randomness
- ✅ Chainlink Data Feeds for real-time price data
- ✅ Full-stack dApp with AI integration
- ✅ IPFS decentralized storage
- ✅ Modern Python GUI with blockchain backend

Built for **Chainlink Chromium Hackathon**.
