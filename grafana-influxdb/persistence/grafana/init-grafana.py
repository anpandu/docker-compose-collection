import base64
import json
import os 
import time
import urllib.request

class Config(object):
  GRAFANA_URL = os.getenv('GRAFANA_URL', 'http://localhost:3003')
  GRAFANA_USER = os.getenv('GRAFANA_USER', 'admin')
  GRAFANA_PASS = os.getenv('GRAFANA_PASS', 'admin123')
  INFLUXDB_URL = os.getenv('INFLUXDB_URL', 'http://localhost:8086')
  DATASOURCE_DATA_FILE = os.getenv('DATASOURCE_DATA_FILE', 'datasources.json')
  DASHBOARD_DATA_FILES = os.getenv('DASHBOARD_DATA_FILES', 'basic-metrics.json')

def read_json(filename):
  dir_path = os.path.dirname(os.path.realpath(__file__))
  file = open("%s/%s" % (dir_path, filename))
  return json.loads(file.read())

def post(url, username, password, json_data):
  req = urllib.request.Request(url)
  req.add_header('Content-Type','application/json')
  data = json.dumps(json_data)
  data = data.encode('utf-8')
  req.add_header('Content-Length', len(data))
  credentials = ('%s:%s' % (username, password))
  encoded_credentials = base64.b64encode(credentials.encode('ascii'))
  req.add_header('Authorization', 'Basic %s' % encoded_credentials.decode("ascii"))
  response = urllib.request.urlopen(req, data)
  return response

time.sleep(10)
print('init grafana daatasources + dashboards')
url = '%s/api/datasources' % (Config.GRAFANA_URL)
data = read_json('json/%s' % (Config.DATASOURCE_DATA_FILE))
for datum in data:
  datum['url'] = Config.INFLUXDB_URL
  try:
    post(url, Config.GRAFANA_USER, Config.GRAFANA_PASS, datum)
    print('>>> LOADED:' % Config.DATASOURCE_DATA_FILE)
  except Exception as e:
    print('>>> FAILED: %s' % Config.DATASOURCE_DATA_FILE)
    print('>>> %s' % str(e))

url = '%s/api/dashboards/db' % (Config.GRAFANA_URL)
filenames = Config.DASHBOARD_DATA_FILES.split('|')
for filename in filenames:
  data = read_json('json/%s' % (filename))
  data['annotations'] = None
  data['id'] = None
  data['uid'] = None
  data = {
    "dashboard": data,
    "folderId": 0,
    "overwrite": False
  }
  try:
    post(url, Config.GRAFANA_USER, Config.GRAFANA_PASS, data)
    print('>>> LOADED:' % filename)
  except Exception as e:
    print('>>> FAILED: %s' % filename)
    print('>>> %s' % str(e))