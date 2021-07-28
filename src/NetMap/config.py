from NetMap import ( load_dotenv, os )

load_dotenv()

def twitter_credentials():

    return {

        'consumer_key': os.getenv('TWITTER_CONSUMER'),
        'consumer_secret_key': os.getenv('TWITTER_CONSUMER_SECRET'),
        'access_token': os.getenv('TWITTER_ACCESS'), 
        'access_secret_token': os.getenv('TWITTER_ACCESS_SECRET') 

            }

def google_credentials():

    return {

        'google_key': os.getenv('GOOGLE')
    }


def sql_credentials():

    return {

        'user': os.getenv('SQL_ROOT'),
        'password': os.getenv('PW_SQL')
        
        }

def mongo_credentials():

    return {

        'server': os.getenv('MONGO_SERVER')
    }