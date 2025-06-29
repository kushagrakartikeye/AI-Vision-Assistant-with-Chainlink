import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Directory Configuration
KNOWN_FACES_DIR = "known_faces"
YOLO_MODEL_PATH = "yolov8n.pt"

# API Configuration
OPENROUTER_KEY = os.getenv('OPENROUTER_KEY')
STABILITY_KEY = os.getenv('STABILITY_KEY')

# Blockchain Configuration (Updated for Sepolia)
ALCHEMY_API_KEY = os.getenv('ALCHEMY_API_KEY')
BLOCKCHAIN_RPC = f"https://eth-sepolia.g.alchemy.com/v2/{ALCHEMY_API_KEY}"  # Changed to Sepolia
NFT_CONTRACT_ADDRESS = "0xE04C1491d38C4e9C4611E2D7AB1FB23422898735"
PRIVATE_KEY = os.getenv('PRIVATE_KEY')

# Chainlink Configuration (Sepolia Testnet)
VRF_COORDINATOR = "0x9DdfaCa8183c41ad55329BdeeD9F6A8d53168B1B"
VRF_SUBSCRIPTION_ID = "82348361337016412546914523271585046779368243734304033559659474398417319807559"

# Chainlink Data Feeds (Sepolia Testnet)
CHAINLINK_ETH_USD_ADDRESS = "0x694AA1769357215DE4FAC081bf1f309aDC325306"  # Sepolia ETH/USD
CHAINLINK_BTC_USD_ADDRESS = "0x1b44F3514812d835EB1BDB0acB33d3fA3351Ee43"  # Sepolia BTC/USD

# IPFS Configuration
IPFS_PROJECT_ID = os.getenv('IPFS_PROJECT_ID')
IPFS_SECRET = os.getenv('IPFS_SECRET')
