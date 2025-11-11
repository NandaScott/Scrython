import json
import urllib.error
import urllib.parse
from typing import Dict, Any, Optional, List
from urllib.request import Request, urlopen

class ScryfallError(Exception):
  def __init__(self, scryfall_data: Dict[str, Any], *args: Any, **kwargs: Any) -> None:
    super(self.__class__, self).__init__(*args, **kwargs)

    self._status: int = scryfall_data['status']
    self._code: str = scryfall_data['code']
    self._details: str = scryfall_data['details']
    self._type: Optional[str] = scryfall_data['type']
    self._warnings: Optional[List[str]] = scryfall_data['warnings']

  @property
  def status(self) -> int:
    return self._status

  @property
  def code(self) -> str:
    return self._code

  @property
  def details(self) -> str:
    return self._details

  @property
  def type(self) -> Optional[str]:
    return self._type

  @property
  def warnings(self) -> Optional[List[str]]:
    return self._warnings

class ScrythonRequestHandler:
  """
  Base class for all Scryfall API requests.

  This class handles HTTP communication with the Scryfall API including
  path building, query parameter encoding, and error handling.

  IMPORTANT - Rate Limiting:
      Scryfall requires 50-100ms delay between requests. This class does
      NOT enforce rate limiting - you must implement delays in your code.

      Example:
          import time
          card1 = scrython.Cards(fuzzy='Lightning Bolt')
          time.sleep(0.1)  # 100ms delay
          card2 = scrython.Cards(fuzzy='Counterspell')

  API Requirements:
      - User-Agent header is required (default: 'Scrython/2.0')
      - Accept header is required (default: 'application/json')
      - HTTPS with TLS 1.2+ is required
  """
  scryfall_data: Dict[str, Any] = {}
  _user_agent: str = 'Scrython/2.0 (https://github.com/NandaScott/Scrython)'
  _accept: str = 'application/json'
  _content_type: str = 'application/json'
  _endpoint: str = ''

  @classmethod
  def set_user_agent(cls, user_agent: str) -> None:
    """
    Set a custom User-Agent header for all Scrython requests.

    Scryfall recommends identifying your application in the User-Agent.

    Args:
        user_agent: Custom User-Agent string

    Example:
        scrython.Cards.set_user_agent('MyMTGApp/1.0 (contact@example.com)')
    """
    cls._user_agent = user_agent

  @property
  def endpoint(self) -> str:
    return self._endpoint

  def __init__(self, **kwargs: Any) -> None:
    self._build_path(**kwargs)
    self._build_params(**kwargs)
    self._fetch(**kwargs)

    if self.scryfall_data['object'] == 'error':
      raise ScryfallError(self.scryfall_data, self.scryfall_data['details'])

  def _fetch(self, **kwargs: Any) -> None:
    data: Optional[bytes] = None
    if data_param := kwargs.get('data', None):
      data = json.dumps(data_param).encode('utf-8')

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

  def _build_params(self, **kwargs: Any) -> None:
    self._query_params: Dict[str, Any] = {
      'format': kwargs.get('format', 'json'),
      'face': kwargs.get('face', ''),
      'version': kwargs.get('version', ''),
      'pretty': kwargs.get('pretty', ''),
      **kwargs
    }

    self._encoded_query_params: str = urllib.parse.urlencode(self._query_params)

  def _build_path(self, **kwargs: Any) -> None:
    parts = self.endpoint.strip("/").split("/")
    resolved: List[str] = []

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
