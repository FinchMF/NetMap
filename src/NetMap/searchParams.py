
from NetMap import ( LocationServices, DateRange )

        
def set_locations(locations: list) -> dict:

    return LocationServices(locations=locations).fetch(radius=4)


def set_wordList():

    return [

        'trump',
        'covid19',
        'biden'
    ]

def set_dates(start_date: str = None, num_days: int = 7):

    return DateRange(start_date=start_date, num_days=num_days).dates

class SearchParams:

    def __init__():

        pass

