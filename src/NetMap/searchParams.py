
from NetMap import ( datetime, timedelta, LocationServices )

        
def set_locations(locations: list) -> dict:

    return LocationServices(locations=locations).fetch(radius=4)


def set_wordList():

    return [

        'trump',
        'covid19',
        'biden'
    ]

def set_dates():

    deltas = {

        'today': datetime.today().strftime('%Y-%m-%d'),
        'yesterday': (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d'),
        'two_days_ago': (datetime.today() - timedelta(days=2)).strftime('%Y-%m-%d')

    }

    return [

        [deltas['yesterday'], deltas['today']],
        [deltas['two_days_ago'], deltas['yesterday']]
    ]

class SearchParams:

    def __init__():

        pass

