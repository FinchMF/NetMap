from NetMap import ( pymongo, LOG )

class MongoCli:
    """Object to handle Mongo Connection"""
    def __init__(self, server: str):

        self.server = server
    
    def connect(self, db: str, collection: str):
        """Connect to Database and Access Declared Collection"""
        self.client = pymongo.MongoClient(self.server)
        LOG.info(f"Client Connected to server: {self.server}")
        self.database = self.client[f"{db}"]
        self.collection = self.database[f"{collection}"]
        LOG.info(f"Client Connected to database: {db} | Collection: {collection}")

    def insertMany(self, data: list):
        """Function to insert many documents"""
        self.collection.insert_many(data)

    def insert(self, data: dict):
        """Function to insert one document"""
        self.collection.insert(data)

    def findAll(self) -> list:
        """Function to retrieve all documents from a collection"""
        found_data = []
        for data in self.collection.find():
            found_data.append(data)
        # the return is a list of dictionaries
        return found_data

    def findOne(self) -> dict:
        """Function to retrieve one document"""
        # this function is check
        return self.collection.find_one()

    def findBy(self, query: dict) -> list:
        """Function to retrieve all records containing an attribute"""
        found_data = []
        for data in self.collection.find(query):
            found_data.append(data)
        # the return is a list of dictionaries
        return found_data