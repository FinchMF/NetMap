
from NetMap import ( datetime, timedelta, logger )

class Num2Words:

    """Integer to String Conversion Object"""

    num2words: dict = {1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', 
                       6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine', 10: 'Ten', 
                       11: 'Eleven', 12: 'Twelve', 13: 'Thirteen', 14: 'Fourteen', 
                       15: 'Fifteen', 16: 'Sixteen', 17: 'Seventeen', 18: 'Eighteen', 
                       19: 'Nineteen', 20: 'Twenty', 30: 'Thirty', 40: 'Forty', 
                       50: 'Fifty', 60: 'Sixty', 70: 'Seventy', 80: 'Eighty', 
                       90: 'Ninety', 0: 'Zero'}

    def convert(cls, number: int) -> str:

        try: 
            return cls.num2words[number]

        except KeyError:

            try:
                return cls.num2words[number-number%10] + cls.num2words[number%10].lower()

            except KeyError:

                logger.info(" Number Outside Range")

class DateRange:

    """Date Object to Generate List of Dates"""

    def __init__(self, start_date: str=None, num_days: int=7):

        self.__start: str = start_date if start_date != None else datetime.today().strftime('%Y-%m-%d')
        self.__num_days: int = num_days
        # generation functions
        self.genDeltas()
        self.genDateList()

    def genDeltas(self) -> dict:

        """Generates Time Deltas for Date List"""

        self.deltas: dict = {}
        self.deltas['start'] = self.__start
        start: DATETIME = datetime.strptime(self.__start, '%Y-%m-%d')

        for day in range(1, self.__num_days):

            self.deltas[f'{Num2Words().convert(number=day)}_day_back']: str = (start - timedelta(days=day)).strftime('%Y-%m-%d')

    def genDateList(self) -> list:

        """Generates List of Dates for Search Parameters"""

        self.dates: list = []

        for i, _ in enumerate(list(self.deltas.values())):

            try:

                self.dates.append([list(self.deltas.values())[i+1], list(self.deltas.values())[i]])
            except:
                
                logger.info(" Finished")
                continue 