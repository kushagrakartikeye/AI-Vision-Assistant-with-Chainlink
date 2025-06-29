// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

// Verified correct imports for Chainlink VRF v2.5
import {VRFConsumerBaseV2Plus} from "@chainlink/contracts/src/v0.8/vrf/dev/VRFConsumerBaseV2Plus.sol";
import {VRFV2PlusClient} from "@chainlink/contracts/src/v0.8/vrf/dev/libraries/VRFV2PlusClient.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract AIVisionNFT is VRFConsumerBaseV2Plus, ERC721URIStorage {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;
    
    // Chainlink VRF Configuration
    uint256 public s_subscriptionId;
    bytes32 public keyHash;
    uint32 public callbackGasLimit;
    uint16 public requestConfirmations;
    uint32 public numWords;
    
    // NFT Tracking
    mapping(uint256 => address) public s_requestIdToSender;
    mapping(uint256 => string) public s_requestIdToTokenURI;
    mapping(uint256 => uint256) public s_requestIdToTokenId;
    mapping(address => string) public userToFaceHash;
    
    // Events
    event UserRegistered(address indexed user, string faceHash);
    event NFTRequested(uint256 indexed requestId, address requester);
    event NFTMinted(uint256 indexed tokenId, address owner);

    constructor(
        uint256 subscriptionId,
        address vrfCoordinator,
        bytes32 _keyHash,
        uint32 _callbackGasLimit,
        uint16 _requestConfirmations,
        uint32 _numWords
    ) 
        VRFConsumerBaseV2Plus(vrfCoordinator)
        ERC721("AI Vision NFT", "AIVN")
    {
        s_subscriptionId = subscriptionId;
        keyHash = _keyHash;
        callbackGasLimit = _callbackGasLimit;
        requestConfirmations = _requestConfirmations;
        numWords = _numWords;
    }

    function registerUser(string memory faceHash) public {
        require(bytes(userToFaceHash[msg.sender]).length == 0, "User already registered");
        userToFaceHash[msg.sender] = faceHash;
        emit UserRegistered(msg.sender, faceHash);
    }

    function isUserRegistered(address user) public view returns (bool) {
        return bytes(userToFaceHash[user]).length > 0;
    }

    function requestNFT(string memory tokenURI) external returns (uint256 requestId) {
        require(isUserRegistered(msg.sender), "User not registered");
        
        VRFV2PlusClient.RandomWordsRequest memory req = VRFV2PlusClient.RandomWordsRequest({
            keyHash: keyHash,
            subId: s_subscriptionId,
            requestConfirmations: requestConfirmations,
            callbackGasLimit: callbackGasLimit,
            numWords: numWords,
            extraArgs: VRFV2PlusClient._argsToBytes(
                VRFV2PlusClient.ExtraArgsV1({nativePayment: false})
            )
        });
        
        requestId = s_vrfCoordinator.requestRandomWords(req);
        s_requestIdToSender[requestId] = msg.sender;
        s_requestIdToTokenURI[requestId] = tokenURI;
        
        emit NFTRequested(requestId, msg.sender);
        return requestId;
    }

    // FIXED: Changed 'memory' to 'calldata' to match the base function signature
    function fulfillRandomWords(
        uint256 requestId,
        uint256[] calldata randomWords
    ) internal override {
        address nftOwner = s_requestIdToSender[requestId];
        string memory tokenURI = s_requestIdToTokenURI[requestId];
        
        _tokenIds.increment();
        uint256 newTokenId = _tokenIds.current();
        
        _safeMint(nftOwner, newTokenId);
        _setTokenURI(newTokenId, tokenURI);
        
        s_requestIdToTokenId[requestId] = newTokenId;
        emit NFTMinted(newTokenId, nftOwner);
    }

    function getTokenIdByRequest(uint256 requestId) public view returns (uint256) {
        return s_requestIdToTokenId[requestId];
    }

    function getUserFaceHash(address user) public view returns (string memory) {
        return userToFaceHash[user];
    }

    function getTokenCounter() public view returns (uint256) {
        return _tokenIds.current();
    }
}
