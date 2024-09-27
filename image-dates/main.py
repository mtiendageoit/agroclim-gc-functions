import ee
import json
import functions_framework

image_collection = 'COPERNICUS/S2_HARMONIZED'

ee.Authenticate()
ee.Initialize(project='agroclim-prj')

@functions_framework.http
def handler(request):
  request_json = request.get_json()
  from_date = request_json.get('from', None)
  to_date = request_json.get('to', None)
  coords = request_json.get('coords', None)

  roi = ee.Geometry.Polygon(coords)
  collection = (ee.ImageCollection(image_collection)
              .filterBounds(roi)
              .filterDate(from_date, to_date))
  
  images = collection.toList(collection.size()).map(lambda image: get_info(ee.Image(image)))

  response = json.dumps(images.getInfo())
  return response, 200, {'Content-Type': 'application/json'}



def get_info(image):
  date = ee.Date(image.get('system:time_start')).format('yyyy-MM-dd')
  cloudy = ee.Number(image.get('CLOUDY_PIXEL_PERCENTAGE'))
  return {'date': date, 'cloudy': cloudy.format('%.0f')}