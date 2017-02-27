import os
import re
import json
import falcon

from andromeda.config import ConfigReader
from andromeda.app.closeup.text.timeextractionhandler import TimeExtractionHandler
from andromeda.app.closeup.text.locationextractionhandler import LocationExtractionHandler


class QueryProcessor:

    def __init__(self):
        self.config = ConfigReader(os.path.join(ConfigReader.CONFIG_DIR, 'closeup.yaml')).data
        self.time_extraction_handler = TimeExtractionHandler()
        self.location_extraction_handler = LocationExtractionHandler(self.config)





    def process(self, query_str, time_format_str='%A, %B %d, %Y - %H:%M:%S', limit=10):
        location_data_list = self.location_extraction_handler.process(query_str, limit)
        time_data_dict = self.time_extraction_handler.process(query_str, time_format_str)

        return { 'time-references' : time_data_dict,  'location-ranking' : location_data_list }



class QueryProcessorApiResource(object):

    def __init__(self):
        self.query_processor = QueryProcessor()


    def on_get(self, req, resp):

        query = req.get_param('query') or ''
        time_format_str = req.get_param('format') or None
        limit = req.get_param('limit') or 10

        print query
        try:
            limit = int(limit)
        except:
            limit = 10

        try:
            query = query.decode('unicode-escape')
        except Exception, e:
            pass # Do nothing in case the string is already in unicode

        try:
            time_format_str = time_format_str.decode('unicode-escape')
        except Exception, e:
            time_format_str = None

        query = re.sub(' +',' ', query).strip()
        if time_format_str is None:
            data_json = self.query_processor.process(query, limit=limit)
        else:
            data_json = self.query_processor.process(query, time_format_str=time_format_str, limit=limit)


        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = json.dumps( data_json )



if __name__ == "__main__":

    query_processor = QueryProcessor()

    q = "brotzeit vivocity now many people right now"
    #q = "kinokuniya queue waiting time now"
    #q = "crowd store"
    q = "marina bay sands"
    result_list = query_processor.process(q, limit=20)
    for result in result_list['location-ranking']:
        print result


