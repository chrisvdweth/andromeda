import falcon

from falcon_cors import CORS

from andromeda.core.preprocessing import TextPreprocessorApiResource
from andromeda.core.featureextraction import LifeProcessorApiResource
from andromeda.core.featureextraction import TimeExtractorApiResource
from andromeda.app.closeup import QueryProcessorApiResource

cors = CORS(allow_all_origins=True)

app = falcon.API(middleware=[cors.middleware])

app.add_route('/textpreprocessor/{level}', TextPreprocessorApiResource())
app.add_route('/lifeprocessor/', LifeProcessorApiResource())
app.add_route('/timeextractor/', TimeExtractorApiResource())
app.add_route('/closeup/search/', QueryProcessorApiResource())



# curl "http://172.29.32.195:8000/timeextractor?query=monday&format=%25A%2C%20%25B%20%25d%2C%20%25Y%20%2D20%25H%3A%25M%3A%25S"

# curl "http://sesame.comp.nus.edu.sg/app/onespace/communicator/andromeda-api/timeextractor/?query=monday&format=%25A%2C%20%25B%20%25d%2C%20%25Y%20%2D20%25H%3A%25M%3A%25S"


# curl "http://172.29.32.195:8000/closeup/search/?query=vivocity&format=%25A%2C%20%25B%20%25d%2C%20%25Y%20%2D%20%25H%3A%25M%3A%25S"


# curl "http://sesame.comp.nus.edu.sg/app/onespace/communicator/andromeda-api/closeup/search/?query=time&format=%25A%2C%20%25B%20%25d%2C%20%25Y%20%2D%20%25H%3A%25M%3A%25S"
