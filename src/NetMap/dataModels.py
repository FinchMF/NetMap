
from NetMap import ( TWEET, logger, List, Dict )

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
    """
    def __init__(self, tweet: TWEET, verbose: bool=False):
        """filtering process"""
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
        self.TWEET: Dict[str, str] = {
                        # general info about tweet content and owner's account
                        'tweet_time': tweet.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
                        'tweet_id': tweet.id,
                        'full_text': tweet.full_text,
                        'text_range': tweet.display_text_range,
                        'tweet_user_id': tweet.user.id,
                        'tweet_user_name': tweet.user.name,
                        'tweet_user_screen_name': tweet.user.screen_name,
                        'tweet_user_location': tweet.user.location,
                        'tweet_user_description': tweet.user.description,
                        'tweet_user_followers_count': tweet.user.followers_count,
                        'tweet_user_friends_count': tweet.user.friends_count,
                        'tweet_user_creation': tweet.user.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
                        'tweet_user_tweet_count': tweet.user.statuses_count,
                        'tweet_retweeted': tweet.retweeted,
                        'tweet_favorited': tweet.favorited,
                        'tweet_retweet_count': tweet.retweet_count,
                        'tweet_favortite_count': tweet.favorite_count,
                        # if tweet is a reply, log who it is a reply to
                        'in_reply_to_status_id': tweet.in_reply_to_status_id,
                        'in_reply_to_user_id': tweet.in_reply_to_user_id,
                        'in_reply_to_screen_name': tweet.in_reply_to_screen_name,
                        # general info about content if the content is retweeted
                        'retweeted_tweet_time': tweet.retweeted_status.created_at.strftime("%Y-%m-%dT%H:%M:%S") if 'retweeted_status' in tweet.__dict__ else None,
                        'retweeted_full_text': tweet.retweeted_status.full_text if 'retweeted_status' in tweet.__dict__ else None,
                        'retweeted_text_range': tweet.retweeted_status.display_text_range if 'retweeted_status' in tweet.__dict__ else None,
                        'retweeted_tweet_id': tweet.retweeted_status.id if 'retweeted_status' in tweet.__dict__ else None,
                        'retweeted_source': tweet.retweeted_status.source if 'retweeted_status' in tweet.__dict__ else None,
                        'retweet_in_reply_to_id': tweet.retweeted_status.in_reply_to_status_id if 'retweeted_status' in tweet.__dict__ else None,
                        'retweet_in_reply_to_user_id': tweet.retweeted_status.in_reply_to_user_id if 'retweeted_status' in tweet.__dict__ else None,
                        'retweet_in_reply_to_user_screenname': tweet.retweeted_status.in_reply_to_screen_name if 'retweeted_status' in tweet.__dict__ else None,
                        'retweet_user_id': tweet.retweeted_status.user.id if 'retweeted_status' in tweet.__dict__ else None,
                        'retweet_user_screen_name': tweet.retweeted_status.user.screen_name if 'retweeted_status' in tweet.__dict__ else None,
                        'retweet_user_description': tweet.retweeted_status.user.description if 'retweeted_status' in tweet.__dict__ else None,
                        'retweet_user_creation': tweet.retweeted_status.user.created_at.strftime("%Y-%m-%dT%H:%M:%S") if 'retweeted_status' in tweet.__dict__ else None,
                        'retweet_user_followers': tweet.retweeted_status.user.followers_count if 'retweeted_status' in tweet.__dict__ else None,
                        'retweet_user_friends_count': tweet.retweeted_status.user.friends_count if 'retweeted_status' in tweet.__dict__ else None,
                        'retweet_retweeted_count': tweet.retweeted_status.retweet_count if 'retweeted_status' in tweet.__dict__ else None,
                        'retweet_favorited_count': tweet.retweeted_status.favorite_count if 'retweeted_status' in tweet.__dict__ else None
        }
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