
import sys
import os.path
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), 
            os.path.pardir
            )
        )
    )
import unittest
import NetMap
from NetMap import SearchParams

class Settings(dict):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self

    @staticmethod
    def set_simpleParams():
        """simple parameters"""
        params: dict = Settings()

        params.locations: list = ['manhattan']
        params.words: list = ['search', 'words']
        params.start_date: str = '2021-06-01'
        params.num_days: int = 7

        return params

    @staticmethod
    def set_complexParams():
        """complex parameters"""
        params: dict = Settings()

        params.locations: list = ['20 W 34th St, New York, NY 10001']
        params.words: list = ['SEARCH', 'wOrDs']
        params.start_date: str = '2021-06-01'
        params.num_days: int = 7

        return params

        
class TestSearchParams(unittest.TestCase):

    """Test Suite for SearchParams Object"""
    # test 1 - generic object test
    def test_SearchParamsObject(self):
        """Simple Test to Confirm Return Object Type"""
        # call object
        params = SearchParams(**Settings.set_simpleParams())
        # test that the SearchParam object is accurately returned
        self.assertIsInstance(params, NetMap.search.searchParams.SearchParams)
    # test 2.1 - Location
    def test_SearchParamsLocationStr(self):
        """Testing Locations Returns are Correct Type"""
        # call object
        params = SearchParams(**Settings.set_simpleParams())
        # test that the geocode value in the location dict is a string
        self.assertIsInstance(params.locations[list(params.locations.keys())[0]], str)
    # test 2.2 - Location
    def test_SearchParamsLocationMultiStr(self):
        """Testing Locations Returns are Correctly Generated"""
        # call object
        params = SearchParams(**Settings.set_simpleParams())
        # parse geocode value
        result = params.locations[list(params.locations.keys())[0]].split(',')
        # test that after parsing there are three strings
        # these strings are the lat, lng and radius
        self.assertEqual(len(result), 3)
        self.assertIsInstance(result[0], str)
        self.assertIsInstance(result[1], str)
        self.assertIsInstance(result[2], str)
    # test 2.3 - Location
    def test_SearchParamsLocationComplex(self):
        """Testing Locations Returns Accurate in Complex Search"""
        # call object
        params = SearchParams(**Settings.set_complexParams())
        # parse geocode value
        result = params.locations[list(params.locations.keys())[0]].split(',')
        # repeat prior test 
        self.assertEqual(len(result), 3)
        self.assertIsInstance(result[0], str)
        self.assertIsInstance(result[1], str)
        self.assertIsInstance(result[2], str)
    # test 3.1 - Word
    def test_SearchParamsWordCount(self):
        """Testing Word Search Return Count"""
        # call object
        params = SearchParams(**Settings.set_simpleParams())
        # pull count key
        count = params.words['count']
        # test that count equals the length of the input list
        self.assertEqual(count, len(Settings.set_simpleParams()['words']))
    

if __name__ == '__main__':

    unittest.main()