from formatting import *
from piwik import *
from google import *
from twfy_api import *
from common_base_measures import *
from twfy import *
from fms import *
from hfymp import *
from pb import *
from wtt import *
from wdtk import *
from common import *
from newsletter import *

def example_dir():
    return os.path.dirname(__file__) + "/examples/"

    
def fake_api_response(module, value):
    mock_api = SimpleApiUrl(value)
    module.urllib.urlopen = lambda url: mock_api
    
    
class SimpleApiUrl:
    '''An object whose read method returns a json string containing the value the SimpleApiUrl 
    was initialized with (jsonified if an int value)'''
    def __init__(self, value):
       self.value = value

    def read(self):
        if type(self.value) == int:
            return '{"value":%d}' % self.value
        else:
            return self.value
            

    
