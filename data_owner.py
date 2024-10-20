from db_provider import Server
import merkletools
import hashlib
class DataOwner:
    #init data owner with the key value data
    #specify the server object
    def __init__(self,key_value_data,server,blockchain):
        self.data= key_value_data
        self.server= server
        self.merkle_tree = None
        self.blockchain = blockchain
    #insert data to self.server
    def insert_data_to_server(self):
        for key, value in self.data.items():
            self.server.add_data(key, value)
    # build merkle tree on data owner side to get the merkle root, key+value as values
    # You can use functions provided by merkletools
    def build_merkle_tree(self):
        self.merkle_tree = merkletools.MerkleTools(hash_type="sha256")
        for key, value in self.data.items():
            leaf = hashlib.sha256(f"{value}".encode()).hexdigest()
            #print(f"Adding leaf for {key}: {leaf}")
            #self.server.update_leaf(key,value,leaf)
            self.merkle_tree.add_leaf(leaf)
        self.merkle_tree.make_tree()
        #print(f"Merkle Tree Root: {self.merkle_tree.get_merkle_root()}")
    # upload self.merkle_tree to self.server
    def upload_merkle_tree_to_server(self):
        self.server.merkle_tree = self.merkle_tree

    def get_merkle_root(self):
        return self.merkle_tree.get_merkle_root() if self.merkle_tree else None

    def upload_merkle_root_to_blockchain(self):
        root = self.get_merkle_root()
        self.blockchain.set_merkle_root(root)
        print(f"Merkle root uploaded to the blockchain.")
