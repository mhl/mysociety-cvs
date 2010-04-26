import unittest
from sitestats.newsletters import common
from datetime import date

class CommonTests(unittest.TestCase):
    
    def testPercentChange(self):
        self.assertEqual("-6%", common.percent_change(15, 16, ''), "percent change 15 from 16 is 6%")
        self.assertEqual("-6%", common.percent_change(16, 17, ''), "percent change 16 from 17 is 6%")
        
    def testPercentChangeForPercents(self):
        self.assertEqual("-1%", common.percent_change(15, 16, '%'), "percent change from 15% to 16% is 1%" )
