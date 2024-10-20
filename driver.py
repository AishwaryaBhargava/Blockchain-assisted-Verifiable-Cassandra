from db_provider import Server
from data_owner import DataOwner
from adv_client import MaliciousClient
from query_client import QueryClient
from blockchain import Blockchain

if __name__ == '__main__':
    # Define Data
    data_provider = Server()
    data = {
        "k1": "v1",
        "k2": "v2",
        "k3": "v3",
    }

    # Setup blockchain
    blockchain = Blockchain('http://127.0.0.1:8545')
    blockchain.compile_contract()
    blockchain.deploy_contract()

    # Setup Data Owner
    data_owner = DataOwner(data, data_provider, blockchain)
    data_owner.build_merkle_tree() # build a merkle tree on the Data Owner side
    data_owner.insert_data_to_server() # upload data to the server
    data_owner.upload_merkle_tree_to_server() # upload merkle tree to the server
    data_owner.upload_merkle_root_to_blockchain() # save merkle root


    # Query client
    query_client = QueryClient(data_provider, blockchain)
    k1_query_value = query_client.query_by_key("k1") # query one item in the data
    #print(f"Retrieved value for 'k1': {k1_query_value}")

    k1_proofs = query_client.retrieve_verification_path_by_tree(0) # 0 means root path
    #print(f"Proofs for 'k1': {k1_proofs}")

    if query_client.query_verification(k1_query_value, k1_proofs, blockchain.get_merkle_root()):
        print("Retrived value is verified")
    else:
        print("Retrived value is modified")

    # Case when adversary exist
    adversary = MaliciousClient(data_provider)
    adversary.modify_data_by_key("k1", "v11") # adversary changes the first key value pair
    # Query again to see if result is modified
    k1_query_value_m = query_client.query_by_key("k1")
    k1_proofs_m = query_client.retrieve_verification_path_by_tree(0)
    if query_client.query_verification(k1_query_value_m, k1_proofs, blockchain.get_merkle_root()):
        print("Retrived value is verified")
    else:
        print("Retrived value is modified")
