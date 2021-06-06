
from NetMap import ( LocationServices, DateRange, WordSearch )

def set_wordList(words: list) -> dict:

    return WordSearch(words).formatted
        
def set_locations(locations: list) -> dict:

    return LocationServices(locations=locations).fetch(radius=4)


def set_dates(start_date: str = None, num_days: int = 7):

    return DateRange(start_date=start_date, num_days=num_days).dates

class SearchParams:

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
