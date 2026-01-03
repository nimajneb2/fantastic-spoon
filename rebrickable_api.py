import requests
from typing import Optional, Dict, Any
from functools import lru_cache


class RebrickableAPI:
    BASE_URL = "https://rebrickable.com/api/v3/lego"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({'Authorization': f'key {api_key}'})
    
    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.BASE_URL}/{endpoint}"
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return {'error': 'Not found', 'status_code': 404}
            elif e.response.status_code == 401:
                return {'error': 'Unauthorized - API key required', 'status_code': 401}
            else:
                return {'error': f'HTTP error: {e.response.status_code}', 'status_code': e.response.status_code}
        except requests.exceptions.ConnectionError:
            return {'error': 'Connection error - unable to reach Rebrickable API', 'status_code': 503}
        except requests.exceptions.Timeout:
            return {'error': 'Request timeout', 'status_code': 504}
        except requests.exceptions.RequestException as e:
            return {'error': f'Request failed: {str(e)}', 'status_code': 500}
    
    @lru_cache(maxsize=128)
    def get_part(self, part_num: str) -> Dict[str, Any]:
        endpoint = f"parts/{part_num}/"
        return self._make_request(endpoint)
    
    @lru_cache(maxsize=128)
    def get_part_colors(self, part_num: str) -> Dict[str, Any]:
        endpoint = f"parts/{part_num}/colors/"
        return self._make_request(endpoint)
    
    @lru_cache(maxsize=128)
    def search_parts(self, search_term: str, page: int = 1) -> Dict[str, Any]:
        endpoint = "parts/"
        params = {'search': search_term, 'page': page, 'page_size': 20}
        return self._make_request(endpoint, params)
    
    @lru_cache(maxsize=128)
    def get_element(self, element_id: str) -> Dict[str, Any]:
        endpoint = f"elements/{element_id}/"
        return self._make_request(endpoint)
    
    def clear_cache(self):
        self.get_part.cache_clear()
        self.get_part_colors.cache_clear()
        self.search_parts.cache_clear()
        self.get_element.cache_clear()
