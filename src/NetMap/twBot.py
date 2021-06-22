from NetMap import ( 
                        API, Cursor, OAuthHandler, 
                        TweepError, RateLimitError,
                        date, datetime, timedelta, time, 
                        cfg, logger, pd,
                        List, USER, DATAFRAME, DATETIME,
                        TWEET, Dict, Any, FilterTweet
                    )

class TwCreds:

    """Initializing an authorization to Twitter's API via Tweepy"""

    def __init__(self):

        self.__creds: Dict[str, str] = cfg.twitter_credentials()

    def authenticate(self):
        """connects API keys for authorization"""
        auth = OAuthHandler(self.creds['consumer_key'], self.creds['consumer_secret_key'])
        auth.set_access_token(self.creds['access_token'], self.creds['access_secret_token'])

        return auth

    @property
    def creds(self):
        return self.__creds


class TwCli:

    """Interactive Authorized Client"""

    def __init__(self):
        """Authorize Client"""
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

        """Fetch twitter username's twitter id"""

        user: USER = self.client.get_user(username)

        return user.id_str

    def get_user_followers(self, username: str, records: int) -> List[USER]:

        """Recieve all followers from given Username
           -----------------------------------------
           Parameters:
            - username (string) to declare what username's followers to be searched
            - records (integer) to delcare who many records of followers to search through
           
           Returns:
            - list of twitter users that are followers of delcared username
        """

        responses: list = []
        x: int =0
        # paginate through search records in Twitter API
        for page in Cursor(self.client.followers, 
                            screen_name=username,
                            wait_on_rate_limit=True,
                            count=200).pages(records):
                            # NOTE: count limit is 200
                            # 200 followers per page are returned

            logger.info(f" Page: {x}")
            logger.info(f" Collected: {[p.screen_name for p in page]} \n")

            responses.extend(page)
            x+=1

        return responses

    def build_followers_dataframe(self, username: str, data: List[USER], save: bool = False) -> DATAFRAME:

        """Build DataFrame from Followers
           ------------------------------
           Parameters:
            - username (string) to declare user followers are of
            - data (list) iterative containing objects to be added in dataframe
            - save (boolean) to declare whether dataframe saves to csv

           Returns:
           - DataFrame of Followers
        """
        # helper function to add usernname to USER object
        def f(username: str, data: USER) -> Dict[str, Any]:
            """add username"""
            data: Dict[str, Any] = data.__dict__
            data.update({'USER': username})

            return data
        # utilize helper function
        prepared_data: List[Dict[str, Any]] = [ f(username, d) for d in data ]
        # build dataframe
        dataframe: DATAFRAME = pd.DataFrame(prepared_data).drop(['_api', '_json'], axis=1)

        if save:
            # if saved - save csv with username in file title
            # NOTE: after sql db is set up, these csv will be pipelined to tables
            dataframe.to_csv(f'{username}_followers.csv')

        return dataframe

    def search(self, date: str, records: int, 
                     geocode: str=None, search_query: str=None) -> List[Dict[str, Any]]:

        """Recieve Searched Tweets
           -----------------------
           Parameters:
            - date (string) to begin look back
            - records (integer) to declare how many records to search through
            - geocode (str) to declare coordinates to search for tweets
            - search_query (string) to declare text pattern to search for in given location and time
            
            Returns:
            - List of Filtered Tweet Objects
            """

        TWEETS: list = []
        count: int = 0
        logger.info(f'Calling Twitter | {date} | {geocode} | {search_query}')
        # paginate through seearch records with Twitter API
        for page in Cursor(self.client.search,
                            q=search_query,
                            lang='en',
                            since=date,
                            tweet_mode='extended',
                            geocode=geocode,
                            count=200).pages(records):
                            # NOTE: count is set at 200 per page, but
                            # Twitter API seems to override this parameter
                            # sending 100 per page
            for tweet in page:
                # for each tweet per page, filtered out noisy data and append to list
                TWEETS.append(FilterTweet(tweet=tweet).TWEET)

            logger.info(f"PAGE: {count} | Tweets Filtered: {len(TWEETS)}")
            count+=1

        return TWEETS

    def build_tweet_dataframe(self, search_query: str, data: List[Dict[str, Any]], save: bool=False) -> DATAFRAME:

        """Build Dataframe from Tweets
           ---------------------------
           Parameters:
            - search query (string) to declare search pattern
            - data (list) iterative containing objects to be added in dataframe
            - save (boolean) to declare whether dataframe saves to csv

           Returns:
           - DataFrame of Tweets
           
        """
        # helper function to add search query to tweet
        def f(search_query: str, data: Dict[str, Any]) -> Dict[str, Any]:
            """add search query"""
            data.update({'search_query': search_query})

            return data
        # utilize helper function
        prepared_data: List[Dict[str, Any]] = [ f(search_query, d) for d in data ]
        # build dataframe
        dataframe: DATAFRAME = pd.DataFrame(prepared_data).fillna('None')

        if save:
            # if saved  - save csv with search query
            # NOTE: after sql db is set up - pipe these csvs to tables
            dataframe.to_csv(f'{search_query}.csv')

        return dataframe