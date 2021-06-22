
from NetMap import ( random, pd, 
                     CLIENT, DATAFRAME, PARAMS,
                     logger )

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
            collector = colletedFollowers.append
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
    def collect_search(params: PARAMS, client: CLIENT) -> DATAFRAME:

        """Collect all results in PARAMS parameters
           ----------------------------------------
           Parameters:
            - params: object contain all parameters set to search twitter
            - client: client to reach Twitter API

            Returns:
            - Dataframe of all search results
        """

        fullSearch = []
        # iterate through date parameters
        for date in params.dates:
            # iterate through geo locations
            for city, geocode in params.locations.items():
                # iterate through set words as hashtags
                for word in params.words['as_hashtags']:
                    # search each word per location each date
                    tweets = client.search(date=date[0], 
                                           records=2,
                                           geocode=geocode,
                                           search_query=word)
                    # generate dataframe and append
                    dataframe = client.build_tweet_dataframe(search_query=word, 
                                                             data=tweets)
                    fullSearch.append(dataframe)
        # concat all dataframes and return
        return pd.concat(fullSearch)