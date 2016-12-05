import falcon

from falcon_cors import CORS

from andromeda.core.preprocessing import TextPreprocessorApiResource
from andromeda.core.featureextraction import LifeProcessorApiResource

cors = CORS(allow_all_origins=True)

app = falcon.API(middleware=[cors.middleware])

app.add_route('/textpreprocessor/{level}', TextPreprocessorApiResource())
app.add_route('/lifeprocessor/', LifeProcessorApiResource())

