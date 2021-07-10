
from NetMap import ( random, pd, re, 
                     CLIENT, DATAFRAME, PARAMS,
                     logger, Tuple )

class Tools:

    """suit of pure functions used to build objects"""

    @staticmethod
    def choose_random_accounts(followers: list, num_accounts: int) -> list:

        """Select Declared Number of Random Followers
           ------------------------------------------
           Parameters:
            - followers (list of strings) handles returned from Twitter API
            - num_accounts (integer) to declare number of accounts to randomly choose
            
            Returns:
            - list of handles (list of strings)
        """

        collectedFollowers: list = []
        # add and count randomly choosen handles
        while len(collectedFollowers) < num_accounts:
            # set random idx
            rand_idx: int = random.randint(0, len(followers)-1)
            # choose follower
            follower: str = followers[rand_idx]
            # add the follower
            # remove it from the list to avoid it being recalled
            collector = collectedFollowers.append
            collector(follower)
            followers.remove(follower)

        return collectedFollowers

    @staticmethod
    def collect_randomly_chosen(selected_followers: list, 
                                client: CLIENT, 
                                records: int = 5 ) -> DATAFRAME:

        """Collect all the followers of the randomly choosen followers from seed account
            ----------------------------------------------------------------------------
            - Parameters:
                - selected_followers (lsit of strings) 
                - client (twittwe client)
                - records (integer) """

        followersFramed = []
        # iterate through randomly chosen accounts from seed account
        for follower in selected_followers:
            # retrieve there followers
            data = client.get_user_followers(username=follower, 
                                             records=records)

            try:
                # attempt to make dataframe
                dataframe = client.build_followers_dataframe(username=follower,
                                                             data=data, 
                                                             save=False)

            except Exception as e:
                logger.info(f"{e} | {follower}")

            collector = followersFramed.append
            collector(dataframe)

        return pd.concat(followersFramed)

    @staticmethod
    def collect_search(params: PARAMS, client: CLIENT, records: int) -> DATAFRAME:

        """Collect all results in PARAMS parameters
           ----------------------------------------
           Parameters:
            - params: object contain all parameters set to search twitter
            - client: client to reach Twitter API
            - records: amount of pagination per search

            Returns:
            - Dataframe of all search results
        """

        fullSearch = []
        # iterate through date parameters
        for date in params.dates:
            # iterate through geo locations
            for city, geocode in params.locations.items():
                print(city)
                # iterate through set words as hashtags
                for word in params.words['as_hashtags']:
                    # search each word at each location for each date
                    tweets = client.search(date=date[0], 
                                           records=records,
                                           geocode=geocode,
                                           search_query=word)
                    # generate dataframe and append
                    dataframe = client.build_tweet_dataframe(search_query=word, 
                                                             city=city,
                                                             date=date[0],
                                                             data=tweets)
                    collector = fullSearch.append
                    collector(dataframe)
        # concat all dataframes and return
        return pd.concat(fullSearch)

    @staticmethod
    def deEmoji(text: str) -> str:

        regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    
        return regrex_pattern.sub(r'',text)

    @staticmethod
    def seperateNormalizedData(data: DATAFRAME) -> Tuple[dict]:
        """Function to parse returned twitter data"""
        # this function preps the data to be inserted into sql database
        pattern = r'\d+$'
        
        normalized_dataCols = []
        unnormalized_dataCols = []
        # parse the columns by matching a regex pattern
        for col in list(data.columns):
            if re.search(pattern, col):
                unnormalized_dataCols.append(col)
            else:
                normalized_dataCols.append(col)
        # convert the parsed data into dictionaries
        normalData = data[normalized_dataCols].to_dict('records')
        unnormalData = data[unnormalized_dataCols].to_dict('records')

        return normalData, unnormalData

    @staticmethod
    def processDataValues(data: dict) -> tuple:
        """Function to process data values for normalized inputs"""
        x = list(data.values())
        for i in len(x):

            if type(x[i]) == str:
                x[i] = Tools.deEmoji(x[i])

            if type(x[i]) == bool:
                x[i]= str(x[i])

            if type(x[i]) == list:
                x[i] = str(x[i])

        return tuple(x)


        
    @staticmethod
    def pipe():
        """Function to Pass Tweet DataFrame into SQL DB"""
        pass
