import json
import time
from web3 import Web3
from constants import (
    BLOCKCHAIN_RPC, NFT_CONTRACT_ADDRESS, PRIVATE_KEY, 
    CHAINLINK_ETH_USD_ADDRESS, CHAINLINK_BTC_USD_ADDRESS
)

class BlockchainManager:
    def __init__(self, message_callback=None):
        self.w3 = None
        self.account = None
        self.nft_contract = None
        self.eth_usd_feed = None
        self.btc_usd_feed = None
        self.message_callback = message_callback
        self.setup_blockchain()
    
    def setup_blockchain(self):
        try:
            self.w3 = Web3(Web3.HTTPProvider(BLOCKCHAIN_RPC))
            if not self.w3.is_connected():
                if self.message_callback:
                    self.message_callback("⚠️ Failed to connect to Ethereum Sepolia via Alchemy")
                return False
                
            self.account = self.w3.eth.account.from_key(PRIVATE_KEY)
            
            # Load NFT Contract ABI
            with open('nft_contract_abi.json', 'r') as f:
                nft_abi = json.load(f)
            
            self.nft_contract = self.w3.eth.contract(
                address=NFT_CONTRACT_ADDRESS,
                abi=nft_abi
            )
            
            # Setup Chainlink Data Feeds
            chainlink_abi = self.get_chainlink_abi()
            self.eth_usd_feed = self.w3.eth.contract(
                address=CHAINLINK_ETH_USD_ADDRESS,
                abi=chainlink_abi
            )
            
            self.btc_usd_feed = self.w3.eth.contract(
                address=CHAINLINK_BTC_USD_ADDRESS,
                abi=chainlink_abi
            )
            
            if self.message_callback:
                self.message_callback("🔗 Blockchain connected to Sepolia testnet")
            return True
            
        except Exception as e:
            if self.message_callback:
                self.message_callback(f"⚠️ Blockchain connection failed: {str(e)}")
            return False
    
    def get_chainlink_abi(self):
        return [
            {
                "inputs": [],
                "name": "latestRoundData",
                "outputs": [
                    {"name": "roundId", "type": "uint80"},
                    {"name": "answer", "type": "int256"},
                    {"name": "startedAt", "type": "uint256"},
                    {"name": "updatedAt", "type": "uint256"},
                    {"name": "answeredInRound", "type": "uint80"}
                ],
                "stateMutability": "view",
                "type": "function"
            }
        ]
    
    def get_crypto_prices(self):
        try:
            # Get ETH price
            _, eth_price, _, _, _ = self.eth_usd_feed.functions.latestRoundData().call()
            eth_price_usd = eth_price / 10**8
            
            # Get BTC price
            _, btc_price, _, _, _ = self.btc_usd_feed.functions.latestRoundData().call()
            btc_price_usd = btc_price / 10**8
            
            return eth_price_usd, btc_price_usd
        except Exception as e:
            if self.message_callback:
                self.message_callback(f"⚠️ Crypto price fetch failed: {str(e)}")
            return None, None
    
    def register_user_on_blockchain(self, face_hash):
        try:
            if not self.nft_contract:
                return None
                
            transaction = self.nft_contract.functions.registerUser(face_hash).build_transaction({
                'from': self.account.address,
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
                'gas': 200000,
                'gasPrice': self.w3.to_wei('20', 'gwei')
            })
            
            # Fixed: Use new web3 transaction signing method
            signed_txn = self.w3.eth.account.sign_transaction(transaction, private_key=PRIVATE_KEY)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)  # Fixed: use raw_transaction
            return tx_hash.hex()
            
        except Exception as e:
            if self.message_callback:
                self.message_callback(f"❌ Blockchain registration failed: {str(e)}")
            return None
    
    def request_nft_mint(self, metadata_uri):
        try:
            if not self.nft_contract:
                return None
                
            transaction = self.nft_contract.functions.requestNFT(metadata_uri).build_transaction({
                'from': self.account.address,
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
                'gas': 500000,
                'gasPrice': self.w3.to_wei('30', 'gwei')
            })
            
            # Fixed: Use new web3 transaction signing method
            signed_txn = self.w3.eth.account.sign_transaction(transaction, private_key=PRIVATE_KEY)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)  # Fixed: use raw_transaction
            return tx_hash.hex()
            
        except Exception as e:
            if self.message_callback:
                self.message_callback(f"❌ NFT minting failed: {str(e)}")
            return None
    
    def monitor_vrf_fulfillment(self, tx_hash):
        try:
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)
            if not receipt.status:
                return False, "Transaction failed"
            
            # Monitor for fulfillment
            for i in range(30):
                time.sleep(10)
                try:
                    # Check if any new tokens were minted
                    token_counter = self.nft_contract.functions.getTokenCounter().call()
                    if token_counter > 0:
                        return True, f"NFT minted successfully! Token counter: {token_counter}"
                except:
                    continue
            
            return False, "VRF fulfillment timeout"
            
        except Exception as e:
            return False, f"VRF monitoring error: {str(e)}"
