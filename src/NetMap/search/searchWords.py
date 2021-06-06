
class WordSearch(list):

    """Word Collection Object"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__list__ = self
        # automate formatting
        self.format()

    def format(self):
        
        """Formats Words
          --------------
          - lowercase
          - option with hashtag
          - number of words"""

        self.formatted: dict = {

            'words': [ word.lower() for word in self ],
            'as_hashtags': [ f"#{word.lower()}" for word in self ],
            'count': len(self)
        }