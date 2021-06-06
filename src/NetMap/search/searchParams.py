
from NetMap import ( LocationServices, DateRange, WordSearch )

def set_wordList(words: list) -> dict:
    """function to setup word list
       ---------------------------
       Parametes:
        - words (list of strings) - takes in words
        
        Returns:
        - formatted word object (dict)
            - keys: 
                - words
                - as_hashtags
                - count
            - value:
                - list of strings all lowercase
                - list of strigns all lowercase, as a hashtag
                - integer expressing how many words there are"""
    return WordSearch(words).formatted
        
def set_locations(locations: list) -> dict:
    """function to set geocodes
       ------------------------
       Parameters:
        - locations (list of strings) - takes in names of cities
           - can exact address as well
        
        Return:
        - geocode object (dict) keys are location strings, values geocodes
        
        
        This object calls LocationServices - which is build around Google Maps API"""
    return LocationServices(locations=locations).fetch(radius=4)


def set_dates(start_date: str = None, num_days: int = 7):
    """function to set dates 
       ---------------------
       Parameters:
       - start_date (string) default to none. If added, use format %Y-%m-%d
       - num_days (integer) looks back days from start date. 
         If no start_date, current day will be used"""
    return DateRange(start_date=start_date, num_days=num_days).dates

class SearchParams:

    """Parameter Object to Store and Set Necessary Seach Inputs"""

    def __init__(self, locations: list, words: list, 
                        start_date: str = None, num_days: int = 7):

        self.__locations = set_locations(locations=locations)
        self.__dates = set_dates(start_date=start_date, num_days=num_days)
        self.__words = set_wordList(words=words)

    @property
    def locations(self):
        return self.__locations

    @property
    def dates(self):
        return self.__dates

    @property
    def words(self):
        return self.__words