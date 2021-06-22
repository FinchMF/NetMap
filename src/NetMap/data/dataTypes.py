
from NetMap import ( List, Dict, Any, Union, Optional, TypeVar )

DATAFRAME: type = TypeVar('pd.core.frames.DataFrame')
DATETIME: type = TypeVar('datetime.datetime')
USER: type = TypeVar('tweepy.models.User')
TWEET: type = TypeVar('tweepy.models.Status')
SEARCH: type = TypeVar('tweepy.models.SearchResults')
CLIENT: type = TypeVar('NetMap.twBot.TwClis')
PARAMS: type = TypeVar('NetMap.search.searchParams.SearchParams')