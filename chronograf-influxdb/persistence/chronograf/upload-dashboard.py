import os 
import urllib.request
import json

class Config(object):
  CHRONOGRAF_URL = os.getenv('CHRONOGRAF_URL', 'http://chronograf:8888')
  DASHBOARD_DATA_FILES = os.getenv('DASHBOARD_DATA_FILES', 'basic-metrics.json')

def read_json(filename):
  dir_path = os.path.dirname(os.path.realpath(__file__))
  file = open("%s/%s" % (dir_path, filename))
  return json.loads(file.read())

def upload_dashboard(dashboard):
  postdata = dashboard
  req = urllib.request.Request(URL)
  req.add_header('Content-Type','application/json')
  data = json.dumps(dashboard)
  data = data.encode('utf-8')
  req.add_header('Content-Length', len(data))
  response = urllib.request.urlopen(req, data)
  return response

URL = '%s/chronograf/v1/dashboards' % (Config.CHRONOGRAF_URL)

filenames = Config.DASHBOARD_DATA_FILES.split('|')
for filename in filenames:
  data = read_json('json/%s' % (filename))
  try:
    upload_dashboard(data)
    print('> %s loaded' % (filename))
  except Exception as e:
    print(str(e))
