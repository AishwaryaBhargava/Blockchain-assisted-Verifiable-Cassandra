import hashlib
from blockchain import Blockchain
from db_provider import Server
import merkletools

# This class serves as a query client and also performs verification
class QueryClient:
    def __init__(self, server, blockchain):
        self.server = server
        self.blockchain = blockchain

    # perform query to server
    def query_by_key(self, key):
        # Assuming Server has a method get_data to fetch data
        return self.server.get_data(key)

    # get proof from server's merkle tree
    def retrieve_verification_path_by_tree(self, key_index):
        # Assuming Server has the Merkle Tree object with proof functionality
        proof = self.server.merkle_tree.get_proof(key_index)
        return proof

    def retrieve_root_from_blockchain(self):
        # Fetch the Merkle root from the smart contract
        root_from_blockchain = self.blockchain.get_merkle_root()
        return root_from_blockchain

    def query_verification(self, retrieved_row, proofs, root_from_blockchain):
        if not retrieved_row:
            return "Verification failed: No data retrieved."
        retrieved_value = retrieved_row.value
        leaf_hash = hashlib.sha256(f"{retrieved_value}".encode()).hexdigest()
        is_valid = self.server.merkle_tree.validate_proof(proofs, leaf_hash, root_from_blockchain)
        if is_valid:
            print("Verification successful: Data is authentic.")
        else:
            print("Verification failed: Data has been tampered.")
        return is_valid
