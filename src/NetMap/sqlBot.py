from NetMap import ( cfg, conn, logger, Union, DATAFRAME, pd )

# helper function to read in SQL commands
def read_sql(file: str) -> list:
    """SQL COMMAND READER
       ------------------
       Parameters:
        - file (string) location of commands
        
       Returns:
        - sql (list) a list of commands callable by index during runtime
    """
    sql = open(file)
    sql = sql.read()
    sql = sql.split(';')

    return sql

class SQL_Credentials:
    """SQL Authentication Object"""
    def __init__(self):

        self.creds = cfg.sql_credentials()
        self.auth = {

            'host': 'localhost',
            'user': self.creds['user'],
            'password': self.creds['password']
        }

    def authenticate(self, db: str = None):
        """Sets Chosen Database to authentication"""
        if db == None:
            logger.info('NO DATABASE CHOSEN')

        else:
            logger.info(f"Database {db} chosen to connect")
            self.auth.update({'database': db})


class SQL_Cli:
    """SQL Client Object"""
    def __init__(self, db: str = None):
        S = SQL_Credentials()
        S.authenticate(db=db)
        # authenticate
        self.__auth = S
        # set connection parameters
        self.__db = conn.connect(

            host=self.__auth.auth['host'],
            user=self.__auth.auth['user'],
            password=self.__auth.auth['password'],
            database=self.__auth.auth['database']

        )

    @property
    def db(self):
        return self.__db

    def execute(self, query: str):
        """SQL Execution Command
           ----------------------
           Parameters:
            - query (string) command to execute
            
        This function connects to db, executes query this closes connection
        """
        cursor=self.db.cursor()
        logger.info('Connection Established')
        cursor.execute(query)
        cursor.close()
        logger.info(f'{query} Executed | Connection Closed')

    
    def insert(self, query: str):
        """SQL Insert Command
           -------------------
           Parameters:
            - query (string) command to insert values

        This function connects to db, inserts values to respective columns then closes connection
        """
        cursor=self.db.cursor()
        logger.info('Connection Established')
        cursor.execute(query)
        self.db.commit()
        cursor.close()
        logger.info(f'Row Count: {cursor.rowcount} inserted | Connection Closed')

    def fetch(self, query: str, verbose: bool = False) -> list:
        """SQL Fetch Command
           -----------------
           Parameters:
            - query (string) command to query recordsd

           Return:
            - res (list) returns queried records
        
        This fucntion connected to db, queries db then closes connection
        """
        cursor = self.db.cursor()
        logger.info('Connection Established')
        cursor.execute(query)
        res = cursor.fetchall()
        logger.info(f'{query} fetched')
        cursor.close()
        if verbose:
            for r in res:
                logger.info(f'line: {r}')

        return res

class sqlModel:
    """Object for SQL"""
    # list of commands 
    commands = './database/queries/sqlCommands.sql'
    checkCreate = './database/createDatabase.sql'

    def __init__(self, db: str = None):

        self.db = db
        self.commands = read_sql(file=sqlModel.commands)
        self.checkCreate = read_sql(file=sqlModel.checkCreate)
        self.__SQL = SQL_Cli(db=db)

    @property
    def SQL(self):
        return self.__SQL

    def checkCreateDataBase(self):
        # this function needs to be places in the Client
        # or i need to allow create a logic that connects to SQL then builds db second
        try:
            self.SQL.execute(self.checkCreate[0])
            logger.info(f' + | {self.db} created')
        except:
            logger.info(f' + | {self.db} already exists |')


    def insertNormalizedData(self, data: dict):
        """Function to insert normalized tweet data"""
        # this function takes all static data retrieved from tweet 
        # dynamic data includes hashtags and mentions
        data = list(data.values())
        self.SQL.insert(self.commands[0].format(data))
        logger.info(f' + | Data Inserted to {self.db} |')

    def insertAddedColumn(self, column: str, data: str):
        """Function to insert data on a specific column"""
        # this function is set up to be used when entering in unstructured data
        self.SQL.insert(self.commands[2].format(column, data))
        logger.info(f' + | Data: {data} Inserted on Column: {column} | ')

    def buildAddedColumn(self, column: str):
        """Function to build column"""
        # this function is set up to be used in case ustructured data has not occurred yet
        self.SQL.insert(self.commands[1].format(column))
        logger.info(f' + | Column: {column} added |')

    def insertUnstructuredData(self, data: dict):
        """Function to insert unstructured tweet data"""
        for column, cell in data.items():
            # this function is transform the sql table
            try:
                self.insertAddedColumn(column=column, data=cell)
            except:
                self.buildAddedColumn(column=column)
                self.insertAddedColumn(column=column, data=cell)

    def retrieveUserData(self, user: str, 
                           as_dataframe: bool = False,  
                           verbose: bool = False) -> Union[dict, DATAFRAME]:
        """Function to Retrieve all data from specific user"""
        DATA = self.SQL.fetch(query=self.commands[3].format(user), verbose=verbose)
        logger.info(f' + | Retrieved all current records on User {user} |')
        if as_dataframe:

            return pd.DataFrame(DATA)

        else:

            return DATA

    def retrieveLocationData(self, location: str,
                                    as_dataframe: bool = False,
                                    verbose: bool = False) -> Union[dict, DATAFRAME]:
        """Function to Retrieve all data from specific location"""
        DATA = self.SQL.fetch(query=self.commands[4].format(location), verbose=verbose)
        logger.info(f' + | Retrieved all current records on Location {location} | ')
        if as_dataframe:

            return pd.DataFrame(DATA)

        else:

            return DATA

    def retreiveWordData(self, word: str,
                               as_dataframe: bool = False,
                               verbose: bool = False) -> Union[dict, DATAFRAME]:
        """Function to Retrieve all data from specific word"""
        DATA = self.SQL.fetch(query=self.command[5].format(word), verbose=verbose)
        logger.info(f' + | Retrieved all current records on Word {word} | ')
        if as_dataframe:

            return pd.DataFrame(DATA)
        
        else:

            return DATA

    def retrieveAllData(self, as_dataframe: bool = False, 
                              verbose: bool = False) -> Union[dict, DATAFRAME]:
        """Function to Retrieve all data in database"""
        DATA = self.SQL.fetch(query=self.commands[6], verbose=verbose)
        logger.info(f' + | Retrieved all current records |')
        if as_dataframe:

            return pd.DataFrame(DATA)

        else:

            return DATA