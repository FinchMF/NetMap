from NetMap import ( cfg, conn )

class SQL_Credentials:

    def __init__(self):

        self.creds = cfg.sql_credentials()
        self.auth = {

            'host': 'localhost',
            'user': self.creds['user'],
            'password': self.creds['password']
        }

    def authenticate(self, db=None):

        if db == None:

            return self.auth

        else:

            return self.auth.update({'database': db})
