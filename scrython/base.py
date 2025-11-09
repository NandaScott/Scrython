import json
import urllib.error
import urllib.parse
from urllib.request import Request, urlopen

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

  @property
  def warnings(self):
    return self._warnings

class ScrythonRequestHandler:
  scryfall_data = {}
  _user_agent = 'Scrython/2.0'
  _accept = 'application/json'
  _content_type = 'application/json'
  _endpoint = ''

  @property
  def endpoint(self):
    return self._endpoint

  def __init__(self, **kwargs) -> None:
    self._build_path(**kwargs)
    self._build_params(**kwargs)
    self._fetch(**kwargs)

    if self.scryfall_data['object'] == 'error':
      raise ScryfallError(self.scryfall_data, self.scryfall_data['details'])

  def _fetch(self, **kwargs):
    if data := kwargs.get('data', None):
      data = json.dumps(data).encode('utf-8')

    request = Request(f'https://api.scryfall.com/{self.endpoint}?{self._encoded_query_params}', data=data)
    request.add_header('User-Agent', self._user_agent)
    request.add_header('Accept', self._accept)
    request.add_header('Content-Type', self._content_type)

    try:
      with urlopen(request) as response:
        charset = response.info().get_param('charset') or 'utf-8'
        decoded = response.read().decode(charset)

        self.scryfall_data = json.loads(decoded)
    except urllib.error.HTTPError as exc:
      raise Exception(f'{exc}: {request.get_full_url()}')

  def _build_params(self, **kwargs):
    self._query_params = {
      'format': kwargs.get('format', 'json'),
      'face': kwargs.get('face', ''),
      'version': kwargs.get('version', ''),
      'pretty': kwargs.get('pretty', ''),
      **kwargs
    }

    self._encoded_query_params = urllib.parse.urlencode(self._query_params)

  def _build_path(self, **kwargs):
    parts = self.endpoint.strip("/").split("/")
    resolved = []

    for part in parts:
      if not part.startswith(':'):
        resolved.append(part)
        continue

      key = part[1:]
      optional = key.endswith('?')

      if optional:
        key = key[:-1]

      value = kwargs.get(key, None)
      if value is None and not optional:
         raise KeyError(f"Missing required path parameter: '{key}'")

      if value is not None and not optional:
        resolved.append(str(value))

    self._endpoint = "/".join(resolved)
