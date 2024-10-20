from cassandra.cluster import Cluster
import hashlib
import json
class Server:
    def __init__(self):
        self.cluster = Cluster()
        self.session = self.cluster.connect()
        self.merkle_tree = None
        self.keyspace = "project3"  # keyspace(database) name for storing data
        self.table = "data" # table name for storing data
        # Create keyspace and corresponding table
        self.session.execute(
            "CREATE KEYSPACE IF NOT EXISTS " + self.keyspace + " WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' : 1};")
        self.session.set_keyspace(self.keyspace)
        self.session.execute(f"CREATE TABLE IF NOT EXISTS {self.table} (key text PRIMARY KEY, value text);")
        #Add create statement for MHT


    def add_data(self, key, value):
        # Use insert syntax to add a new key-value pair to the target table
        insert_stmt = self.session.prepare(
            f"INSERT INTO {self.table} (key, value) VALUES (?, ?);"
        )
        self.session.execute(insert_stmt, (key, value))

    def get_data(self, key):
        # Retrieve value by key
        select_stmt = self.session.prepare(
            f"SELECT value FROM {self.table} WHERE key = ?;"
        )
        result = self.session.execute(select_stmt, [key])
        return result.one()  # This will return None if no data found, or a Row instance
    def update_leaf(self, key,value, hash_value):
        update_stmt = self.session.prepare(
            f"UPDATE {self.table} SET hash = ? WHERE key = ?;"
        )
        self.session.execute(update_stmt, (hash_value, key))
