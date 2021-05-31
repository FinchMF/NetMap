
from NetMap import ( List, Dict, Any, Union, Optional, TypeVar )

DATAFRAME = TypeVar('pd.core.frames.DataFrame')
DATETIME = TypeVar('datetime.datetime')
USER = TypeVar('tweepy.models.User')
TWEET = TypeVar('tweepy.models.Status')
SEARCH = TypeVar('tweepy.models.SearchResults')