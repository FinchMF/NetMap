from NetMap import ( 
                        API, Cursor, OAuthHandler, TweepError,
                        date, datetime, timedelta, time, 
                        cfg, logger, List, USER, DATAFRAME, pd
                    )

class TwCreds:
    """
    Initializing an authorization to Twitter's API via Tweepy
    """
    def __init__(self):

        self.__creds = cfg.twitter_credentials()

    def authenticate(self):
        """connects API keys for authorization"""
        auth = OAuthHandler(self.creds['consumer_key'], self.creds['consumer_secret_key'])
        auth.set_access_token(self.creds['access_token'], self.creds['access_secret_token'])

        return auth

    @property
    def creds(self):
        return self.__creds


class TwCli:
    """
    Interactive Authorized Client
    """
    def __init__(self):

        self.__auth = TwCreds().authenticate()
        self.__client = API(self.__auth)

    @property
    def client(self):
        return self.__client

    def check_twitter_user_exists(self, username: str) -> bool:
        """Check to see if User account exists"""
        try:
            self.client.get_user(username)
            logger.info(f"{username} found")
            return True

        except:
            logger.info(f"{username} is not found")
            return False

    def get_user_id(self, username: str) -> str:

        user = self.client.get_user(username)

        return user.id_str

    def get_user_followers(self, username: str) -> List[USER]:

        """
        Recieve all followers from given Username
        """

        responses = []

        for page in Cursor(self.client.followers, 
                           screen_name=username, 
                           wait_on_rate_limit=True,
                           count=200).pages():

            logger.info(f"Collected: {[p.screen_name for p in page]}")

            try:

                responses.extend(page)

            except TweepError as e:
                logging.info(f"{e} going to sleep")
                time.sleep(60)
                continue

        return responses

    def build_dataframe(self, username: str, data: List[USER], save: bool = False) -> DATAFRAME:

        """Build DataFrame from Followers"""

        def f(username: str, data: USER) -> USER:

            data = data.__dict__
            data.update({'USER': username})

            return data
        
        prepared_data = [f(username, d) for d in data]

        dataframe = pd.DataFrame(prepared_data).drop(['_api', '_json'], axis=1)

        if save:

            dataframe.to_csv(f'{username}_followers.csv')

        return dataframe