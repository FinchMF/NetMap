from NetMap import ( TwCli, SearchParams, Tools, mongoModel, logger )

class LINE:
    """Object to execute pipeline"""
    # client for pipeline
    client = TwCli()
    def __init__(self, params: dict, records: int):
        # set parameters and db client
        self.records = records
        self.params = SearchParams(**params)
        self.dbModel = mongoModel(database='NetMap', 
                                  collection='TwitterRecords')
        
    def getData(self):
        """Function to call Twitter API and retrieve"""
        self.data = Tools.collect_search(params=self.params, 
                                         client=LINE.client, 
                                         records=self.records)
        
    def send2db(self):
        """Function to send data to pipeline"""
        if self.data is not None:
            self.data.fillna('None')
            self.dbModel.client.insertMany(data=self.data.to_dict('records'))
        else:
            logger.info('No data has been collected | run getData') 