"""
Blockchain Implementation for Healthcare Management System
"""

import hashlib
import json
from datetime import datetime


class Block:
    """Block in the blockchain"""
    
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.timestamp = datetime.now().isoformat()
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self._calculate_hash()
    
    def _calculate_hash(self):
        """Calculate SHA-256 hash of block data"""
        input_str = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(input_str.encode()).hexdigest()
    
    def mine_block(self, difficulty):
        """Mine block with proof-of-work"""
        target = "0" * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self._calculate_hash()
        print(f"Block Mined: {self.hash}")
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce,
            'hash': self.hash
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create Block from dictionary"""
        block = cls.__new__(cls)
        block.index = data['index']
        block.timestamp = data['timestamp']
        block.data = data['data']
        block.previous_hash = data['previous_hash']
        block.nonce = data['nonce']
        block.hash = data['hash']
        return block
    
    def __str__(self):
        return f"Block(index={self.index}, hash={self.hash[:16]}...)"


class Blockchain:
    """Blockchain for healthcare data integrity"""
    
    def __init__(self, difficulty=2):
        self.chain = []
        self.difficulty = difficulty
        self._create_genesis_block()
    
    def _create_genesis_block(self):
        """Create the genesis block"""
        genesis_block = Block(0, "Genesis Block - Healthcare System", "0")
        self.chain.append(genesis_block)
    
    def get_latest_block(self):
        """Get the latest block in the chain"""
        return self.chain[-1]
    
    def add_block(self, data):
        """Add a new block to the blockchain"""
        latest_block = self.get_latest_block()
        new_block = Block(len(self.chain), data, latest_block.hash)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        return new_block
    
    def is_chain_valid(self):
        """Validate the integrity of the blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Check if current block's hash is valid
            if current_block.hash != current_block._calculate_hash():
                return False
            
            # Check if current block points to previous block
            if current_block.previous_hash != previous_block.hash:
                return False
        
        return True
    
    def get_size(self):
        """Get the number of blocks in the chain"""
        return len(self.chain)
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'chain': [block.to_dict() for block in self.chain],
            'difficulty': self.difficulty
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create Blockchain from dictionary"""
        blockchain = cls.__new__(cls)
        blockchain.chain = [Block.from_dict(block_data) for block_data in data['chain']]
        blockchain.difficulty = data['difficulty']
        return blockchain
    
    def __str__(self):
        return f"Blockchain(blocks={len(self.chain)}, difficulty={self.difficulty})"
