import json
from urllib.request import Request, urlopen
import urllib.parse

class ScryfallError(Exception):
  def __init__(self, scryfall_data, *args, **kwargs):
    super(self.__class__, self).__init__(*args, **kwargs)

    self._status = scryfall_data['status']
    self._code = scryfall_data['code']
    self._details = scryfall_data['details']
    self._type = scryfall_data['type']
    self._warnings = scryfall_data['warnings']

  @property
  def status(self):
    return self._status

  @property
  def code(self):
    return self._code

  @property
  def details(self):
    return self._details

  @property
  def type(self):
    return self._type

  def warnings(self):
    return self._warnings

class ScrythonRequestHandler:
  scryfall_data = {}
  _user_agent = 'Scrython/2.0'
  _accept = 'application/json'
  _endpoint = ''

  @property
  def endpoint(self):
    return self._endpoint

  def __init__(self, **kwargs) -> None:
    self._build_path(**kwargs)
    self._build_params(**kwargs)
    self._fetch()

    if self.scryfall_data['object'] == 'error':
      raise ScryfallError(self.scryfall_data, self.scryfall_data['details'])

  def _fetch(self):
    request = Request(f'https://api.scryfall.com/{self.endpoint}?{self._encoded_query_params}')
    request.add_header('User-Agent', self._user_agent)
    request.add_header('Accept', self._accept)
  
    response = urlopen(request)
    charset = response.info().get_param('charset') or 'utf-8'
    decoded = response.read().decode(charset)

    self.scryfall_data = json.loads(decoded)

  def _build_params(self, **kwargs):
    self._query_params = {
      'format': kwargs.get('format', 'json'),
      'face': kwargs.get('face', ''),
      'version': kwargs.get('version', ''),
      'pretty': kwargs.get('pretty', '')
    }

    self._encoded_query_params = urllib.parse.urlencode(self._query_params)

  def _build_path(self, **kwargs):
    parts = self.endpoint.strip("/").split("/")
    resolved = []

    for part in parts:
      if not part.startswith(':'):
        resolved.append(part)
        continue

      value = kwargs.get(part[1:], None)
      if value is None:
         raise KeyError(f"Missing required path parameter: '{key}'")

      resolved.append(str(value))

    self._endpoint = "/" + "/".join(resolved)
