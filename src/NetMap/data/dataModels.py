
from NetMap import ( TWEET, logger, List, Dict )

class TweetData(dict):

    """Base Tweet Data Model Object for Filtering"""

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.__dict__ = self

    @staticmethod
    def filterData(tweet: TWEET):

        """Tweet Filter Model"""

        DATA: dict = TweetData()
        # general info about tweet content and owner's account
        DATA.tweet_time: str = tweet.created_at.strftime("%Y-%m-%dT%H:%M:%S")
        DATA.tweet_id: int = tweet.id
        DATA.full_text: str = tweet.full_text
        DATA.text_range: str = tweet.display_text_range
        DATA.tweet_user_id: int = tweet.user.id
        DATA.tweet_user_name: str = tweet.user.name
        DATA.tweet_user_screen_name: str = tweet.user.screen_name
        DATA.tweet_user_location: str = tweet.user.location
        DATA.tweet_user_description: str = tweet.user.description
        DATA.tweet_user_followers_count: int = tweet.user.followers_count
        DATA.tweet_user_friends_count: int = tweet.user.friends_count
        DATA.tweet_user_creation: str = tweet.user.created_at.strftime("%Y-%m-%dT%H:%M:%S")
        DATA.tweet_user_tweet_count: int = tweet.user.statuses_count
        DATA.tweet_retweeted: bool = tweet.retweeted
        DATA.tweet_favorited: bool = tweet.favorited
        DATA.tweet_retweet_count: int = tweet.retweet_count
        DATA.tweet_favorite_count: int = tweet.favorite_count
        # if tweet is a reply, log who it is a rely to
        DATA.tweet_in_reply_to_status_id: int = tweet.in_reply_to_status_id
        DATA.tweet_in_reply_to_user_id: int = tweet.in_reply_to_user_id
        DATA.tweet_in_reply_to_user_screen_name: str = tweet.in_reply_to_screen_name
        # general info about content's origin if conetent is retweeted
        DATA.retweeted_tweet_time: str = tweet.retweeted_status.created_at.strftime("%Y-%m-%dT%H:%M:%S") if 'retweeted_status' in tweet.__dict__ else None
        DATA.retweeted_full_text: str = tweet.retweeted_status.full_text if 'retweeted_status' in tweet.__dict__ else None
        DATA.retweeted_text_range: str = tweet.retweeted_status.display_text_range if 'retweeted_status' in tweet.__dict__ else None
        DATA.retweeted_tweet_id: int = tweet.retweeted_status.id if 'retweeted_status' in tweet.__dict__ else None
        DATA.retweeted_source: str = tweet.retweeted_status.source if 'retweeted_status' in tweet.__dict__ else None
        DATA.retweet_in_reply_to_id: int = tweet.retweeted_status.in_reply_to_status_id if 'retweeted_status' in tweet.__dict__ else None
        DATA.retweet_in_reply_to_user_id: int = tweet.retweeted_status.in_reply_to_user_id if 'retweeted_status' in tweet.__dict__ else None
        DATA.retweet_in_reply_to_user_screenname: str = tweet.retweeted_status.in_reply_to_screen_name if 'retweeted_status' in tweet.__dict__ else None
        DATA.retweet_user_id: int = tweet.retweeted_status.user.id if 'retweeted_status' in tweet.__dict__ else None
        DATA.retweet_user_screen_name: str = tweet.retweeted_status.user.screen_name if 'retweeted_status' in tweet.__dict__ else None
        DATA.retweet_user_description: str = tweet.retweeted_status.user.description if 'retweeted_status' in tweet.__dict__ else None
        DATA.retweet_user_creation: str = tweet.retweeted_status.user.created_at.strftime("%Y-%m-%dT%H:%M:%S") if 'retweeted_status' in tweet.__dict__ else None
        DATA.retweet_user_followers_count: int = tweet.retweeted_status.user.followers_count if 'retweeted_status' in tweet.__dict__ else None
        DATA.retweet_user_friends_count: int = tweet.retweeted_status.user.friends_count if 'retweeted_status' in tweet.__dict__ else None
        DATA.retweet_retweeted_count: int = tweet.retweeted_status.retweet_count if 'retweeted_status' in tweet.__dict__ else None
        DATA.retweet_favorited_count: int = tweet.retweeted_status.favorite_count if 'retweeted_status' in tweet.__dict__ else None

        return DATA


class FilterTweet:

    """Tweet Filtering Object
       ----------------------
       Recieves tweet object from twitter API
       and filters out all noisey data. 

       Relevant data inlcudes dimensions depicting:
        - Tweet Text and Content descriptors
        - Tweet's Owner
        - Accounts referenced in Tweet
        - If Tweet is retweet:
            - Original Tweet Text and Content descriptors
            - Original Tweet's Owner
            - Accounts referenced in Original Tweet

        How the process works:
        ----------------------
          - the object first searches for all hashtags and mentions
          - then checks to see if the content is a retweet
           
          - once that is complete, the tweet is filtered by a filter template
          - subsequent to the initial template, the hashtags and mentions data is added dynamically
    """
    def __init__(self, tweet: TWEET, verbose: bool=False):

        """filtering process automatic"""

        # fetch all hashtags
        self.hashtags: List[str] = [ h['text'] for h in tweet.entities['hashtags'] ]
        # fetch all mentioned accounts
        self.users_mentions_screennames: List[str] = [ s['screen_name'] for s in tweet.entities['user_mentions'] ]
        self.users_mentions_names: List[str] = [ s['name'] for s in tweet.entities['user_mentions'] ]
        self.users_mentions_ids: List[str] = [ s['id'] for s in tweet.entities['user_mentions'] ]

        try:
            # check if tweet's content is original or retweeted
            # if retweeted fetch hashtags in the retweeted content
            self.retweeted_hashtags: List[str] = [ h['text'] for h in tweet.retweeted_status.entities['hashtags'] ]
            # fetch all mentioned accounts from the retweeted content
            self.retweeted_mentions_screennames: List[str] = [ s['screen_name'] for s in tweet.retweeted_status.entities['user_mentions'] ]
            self.retweeted_mentions_names: List[str] = [ s['name'] for s in tweet.retweeted_status.entities['user_mentions'] ]
            self.retweeted_mentions_ids: List[str] = [ s['id'] for s in tweet.retweeted_status.entities['user_mentions'] ]

        except Exception:
            if verbose:
                logger.info("Tweet is Orginal | Not Retweeted from Another Account")
        # filtered tweet object
        self.TWEET: Dict[str, Any] = TweetData().filterData(tweet=tweet)
        self.addFilteredData()

    def addFilteredData(self):

        """Add additional filtered data to Tweet Object"""
        # collect filtered data attributes
        filteredData: List[tuple] = [ i for i in zip(self.__dict__.keys(), self.__dict__.values()) if i[0] != 'TWEET']
        # iterate through tuples and set dynamic categorical keys in filtered tweet object
        for datas in filteredData:
            x=0
            # access the tuple containing keys and values
            for data in datas:
                # check that values are being accessed
                # not keys
                if type(data) == list:
                    # iterate through values 
                    # generate dynamic categorical keys
                    for d in data:
                        self.TWEET[f'{datas[0]}_{x}'] = d
                        x+=1    