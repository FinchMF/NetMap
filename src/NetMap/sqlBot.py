from NetMap import ( cfg, conn, logger )

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
            return self.auth

        else:
            logger.info(f"Database {db} chosen to connect")
            return self.auth.update({'database': db})


class SQL_Cli:
    """SQL Client Object"""
    def __init__(self, db: str = None):
        # authenticate
        self.__auth = SQL_Credentials().authenticate(db=db)
        # set connection parameters
        self.__db = conn.connect(

            host=self.auth['host'],
            user=self.auth['user'],
            password=self.auth['password'],
            database=self.auth['database']
            
        )

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