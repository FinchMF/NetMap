
from NetMap import ( requests, cfg )

def callGoogle(endpoint: str, params: dict) -> str:

    """Call google maps API
       --------------------
       Parameters:
       -endpoint (string) Google Maps API URL
       -params (dictionary) JSON containing API key and city

        Returns:
        -geocode (string)
    """
    # hit API 
    call = requests.get(endpoint, params=params)
    response = call.json()
    # grab first element in payload
    result: dict = response['results'][0]
    # format lat and lng to a string
    return f"{result['geometry']['location']['lat']}, {result['geometry']['location']['lng']}"
    
class LocationServices:

    """Location object to convert city names to geocodes"""

    def __init__(self, locations: list):

        self.__api_endpoint: str = 'https://maps.googleapis.com/maps/api/geocode/json'
        self.__api_key: str = cfg.google_credentials()
        self.__locations: list = locations
        self.__set_locations: dict = {}

    @property
    def locations(self):
        return self.__locations

    @property
    def set_locations(self):
        return self.__set_locations
        
    def fetch(self, radius: int) -> dict:

        """Converts Object Defined Locations to Geocodes adding delcared Radius
            -------------------------------------------------------------------
            Parameters:
            -radius (integer) to declare radius surrounding converted geocodes
            
            Returns:
            -geocodes (dictionary) where keys are cities
                                         values are geocodes with radius attached
        """
        # convert radius integer to string
        radius: str = f"{radius}mi" 
        # set empty dict
        geocodes: dict = {}
        # iterate through instantiated locations list
        # set search parameters to pass to callGoogle method
        for location in self.locations:

            params: dict = {

                'address': location,
                'sensor': 'false',
                'key': self.__api_key['google_key']

            }
            # define key value pairs | city - geocode
            geocodes[location]: str = f"{callGoogle(endpoint=self.__api_endpoint, params=params)},{radius}"

        return geocodes