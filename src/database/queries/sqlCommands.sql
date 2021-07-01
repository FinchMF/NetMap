INSERT INTO WordSearch(
-- 0    
-- normalized insert statement of static record struture
    tweet_time,
    tweet_id,
    full_text,
    text_range,
    tweet_user_id,
    tweet_user_name,
    tweet_user_screen_name,
    tweet_user_location,
    tweet_user_description,
    tweet_user_followers_count,
    tweet_user_friends_count,
    tweet_user_tweet_count,
    tweet_retweeted,
    tweet_favorited,
    tweet_retweet_count, 
    tweet_favorite_count,
    tweet_in_reply_to_status_id,
    tweet_in_reply_to_user_id, 
    tweet_in_reply_to_user_screen_name,
    retweeted_tweet_time,
    retweeted_full_text,
    retweeted_text_range,
    retweeted_tweet_id,
    retweeted_source,
    retweet_in_reply_to_id,
    retweet_in_reply_to_user_screename,
    retweet_user_id,
    retweet_user_screen_name,
    retweet_user_description,
    retweet_user_creation,
    retweet_user_followers_count,
    retweet_user_friends_count,
    retweet_retweeted_count,
    retweet_favorited_count,
    search_query,
    search_location,
    search_time
)
-- alittle bit of a hack, but this allows for string formating
-- when pulled into python during automation
VALUES {}
;


-- dynamic insertion through table alteration
ALTER TABLE WordSearch
-- 1
-- using the same 'formatting' hack to allow for dynamic addition of columns
ADD {} VARCHAR(200)
;

INSERT INTO WordSearch(
-- 2
-- using the 'formatting' hack to allow for dynamic insertion to added columns
    {}
)

VALUES {}
;

SELECT * FROM WordSearch WHERE twitter_user_name = {}
-- 3
;
SELECT * FROM WordSearch WHERE search_location = {}
-- 4
;
SELECT * FROM WordSearch WHERE search_query = {}
-- 5
;
SELECT * FROM WordSearch
-- 6
;
