from NetMap import ( mongo )

class mongoModel:
    """Object to connect to local mongodb"""
    server = "mongodb://localhost:27017/"

    def __init__(self, database: str, collection: str):
        # instantiates connection to database and collection on server
        self.database = database
        self.collection = collection
        self.client = mongo.MongoCLi(
                      server=mongoModel.server
                      ).connect(db=database, 
                      collection=collection)