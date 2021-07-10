CREATE TABLE {}.WordSearch (
    -- general info about tweet content and owner's account
    tweet_time VARCHAR(30),
    tweet_id VARCHAR(100),
    full_text VARCHAR(300),
    text_range VARCHAR(30),
    tweet_user_id VARCHAR(100),
    tweet_user_name VARCHAR(100),
    tweet_user_screen_name VARCHAR(100),
    tweet_user_location VARCHAR(100),
    tweet_user_description VARCHAR(300),
    tweet_user_followers_count INT,
    tweet_user_friends_count INT,
    tweet_user_creation VARCHAR(100),
    tweet_user_tweet_count INT,
    tweet_retweeted VARCHAR(10),
    tweet_favorited VARCHAR(10),
    tweet_retweet_count INT,
    tweet_favorite_count INT, 
    -- for tweets that are replys, log data here else None
    tweet_in_reply_to_status_id VARCHAR(100),
    tweet_in_reply_to_user_id VARCHAR(100),
    tweet_in_reply_to_user_screen_name VARCHAR(100),
    -- general in about content's origin if content is retweeted
    retweeted_tweet_time VARCHAR(30),
    retweeted_full_text VARCHAR(300),
    retweeted_text_range VARCHAR(30),
    retweeted_tweet_id VARCHAR(100),
    retweeted_source VARCHAR(70),
    retweet_in_reply_to_id VARCHAR(100),
    retweet_in_reply_user_id VARCHAR(100),
    retweet_in_reply_to_user_screenname VARCHAR(100),
    retweet_user_id VARCHAR(100),
    retweet_user_screen_name VARCHAR(100),
    retweet_user_description VARCHAR(300),
    retweet_user_creation VARCHAR(100),
    retweet_user_followers_count INT,
    retweet_user_friends_count INT,
    retweet_retweeted_count INT,
    retweet_favorited_count INT,
    
    -- LOGGED SEARCH PARAMS
    -- the word or phrase the tweet is a result of
    search_query VARCHAR(300),
    -- the location the tweet is a result of
    search_location VARCHAR(300),
    -- the time the tweet was searched
    search_time VARCHAR(20),

    PRIMARY KEY (tweet_id)

)
;