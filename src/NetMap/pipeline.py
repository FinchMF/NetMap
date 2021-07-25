from NetMap import ( TwCli, SearchParams, Tools, 
                     mongoModel, logger, Union,
                     pd, DATAFRAME, Web, FIGURE )
class NET(Web):
    """Object Inheiriting WEB"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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

    def callData(self, query: dict = None) -> Union[dict, list] :
        """Function to read stored data"""
        if query == None:
            return self.dbModel.client.findAll()
        else:
            return self.dbModel.client.findBy(query=query)

    @staticmethod
    def dataFramed(data: list) -> DATAFRAME:
        """Function to convert returned"""
        return pd.DataFrame(data)

    @staticmethod
    def generateNetwork(data: DATAFRAME, title: str) -> FIGURE:
        """Function to Generate Network Visual"""
        # instantiate network and generate network figure
        n = NET(data=data, title=title)
        n.generate()
        logger.info(f"{title} Network Graph generated")
        return n.figure