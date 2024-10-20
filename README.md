# Blockchain-assisted-Verifiable-Cassandra

A system that combines blockchain technology with Apache Cassandra to provide verifiable data operations using Merkle trees. This implementation ensures data integrity and allows for verification of data modifications through blockchain-based merkle root storage.

## System Architecture

The system consists of several key components:

1. **Data Owner** (`data_owner.py`)
   - Manages the original data
   - Builds Merkle trees for data verification
   - Uploads data to Cassandra server
   - Publishes Merkle roots to blockchain

2. **Database Provider** (`db_provider.py`)
   - Implements Cassandra server functionality
   - Handles data storage and retrieval
   - Maintains Merkle tree structure

3. **Blockchain Component** (`blockchain.py`)
   - Manages smart contract interactions
   - Stores and retrieves Merkle roots
   - Uses Web3 for Ethereum blockchain integration

4. **Query Client** (`query_client.py`)
   - Performs data queries
   - Retrieves verification proofs
   - Validates data integrity using Merkle proofs

5. **Security Testing** (`adv_client.py`)
   - Implements malicious client behavior
   - Tests system security measures

## Prerequisites

- Python 3.x
- Apache Cassandra
- Ethereum client (Ganache recommended for development)
- Python packages:
  ```
  pip install web3
  pip install py-solc-x
  pip install cassandra-driver
  pip install merkletools
  ```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/AishwaryaBhargava/Blockchain-assisted-Verifiable-Cassandra.git
cd Blockchain-assisted-Verifiable-Cassandra
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start Cassandra service:
```bash
sudo service cassandra start
```

4. Start Ganache or your preferred Ethereum client:
```bash
ganache-cli
```

## Usage

### Basic Setup and Data Operations

```python
from db_provider import Server
from data_owner import DataOwner
from blockchain import Blockchain
from query_client import QueryClient

# Initialize components
server = Server()
blockchain = Blockchain('http://127.0.0.1:8545')
blockchain.compile_contract()
blockchain.deploy_contract()

# Prepare data
data = {
    "k1": "v1",
    "k2": "v2",
    "k3": "v3"
}

# Setup data owner and upload data
data_owner = DataOwner(data, server, blockchain)
data_owner.build_merkle_tree()
data_owner.insert_data_to_server()
data_owner.upload_merkle_tree_to_server()
data_owner.upload_merkle_root_to_blockchain()

# Query and verify data
query_client = QueryClient(server, blockchain)
value = query_client.query_by_key("k1")
proofs = query_client.retrieve_verification_path_by_tree(0)
is_verified = query_client.query_verification(value, proofs, blockchain.get_merkle_root())
```

### Running the Complete System

Use the provided driver script:
```bash
python driver.py
```

This will:
1. Set up the system components
2. Insert sample data
3. Create and store Merkle tree
4. Perform verification tests
5. Demonstrate malicious modification detection

## Components Detail

### 1. Database Provider (Server)
```python
server = Server()
server.add_data("key1", "value1")
result = server.get_data("key1")
```

### 2. Data Owner
```python
data_owner = DataOwner(data, server, blockchain)
data_owner.build_merkle_tree()
data_owner.upload_merkle_root_to_blockchain()
```

### 3. Query Client
```python
query_client = QueryClient(server, blockchain)
value = query_client.query_by_key("k1")
proofs = query_client.retrieve_verification_path_by_tree(0)
is_verified = query_client.query_verification(value, proofs, root)
```

### 4. Blockchain Integration
```python
blockchain = Blockchain('http://127.0.0.1:8545')
blockchain.compile_contract()
blockchain.deploy_contract()
blockchain.set_merkle_root(root)
stored_root = blockchain.get_merkle_root()
```

## Security Features

1. **Data Integrity Verification**
   - Merkle tree-based verification
   - Blockchain-stored root values
   - Proof validation for each query

2. **Tamper Detection**
   - Automatic detection of unauthorized modifications
   - Verification against blockchain-stored roots
   - Complete audit trail

3. **Smart Contract Security**
   - Simple, focused contract design
   - Minimal attack surface
   - Public verification capability

## Testing

The system includes tests for both normal operations and malicious scenarios:

```python
# Normal operation test
value = query_client.query_by_key("k1")
is_valid = query_client.query_verification(value, proofs, root)

# Malicious modification test
adversary = MaliciousClient(server)
adversary.modify_data_by_key("k1", "modified_value")
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Acknowledgments

- Apache Cassandra team
- Ethereum and Web3.py developers
- MerkleTools library contributors
