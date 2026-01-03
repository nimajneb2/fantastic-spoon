import requests
import cachetools
from functools import wraps

# Cache for API responses (maxsize=100, TTL=1 hour)
part_cache = cachetools.TTLCache(maxsize=100, ttl=3600)
element_cache = cachetools.TTLCache(maxsize=100, ttl=3600)

REBRICKABLE_BASE_URL = "https://rebrickable.com/api/v3/lego"


def cache_result(cache_dict):
    """Decorator to cache function results"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from arguments
            key = str(args) + str(kwargs)
            if key in cache_dict:
                return cache_dict[key]
            
            result = func(*args, **kwargs)
            cache_dict[key] = result
            return result
        return wrapper
    return decorator


@cache_result(part_cache)
def search_part(part_num):
    """
    Search for a LEGO part by part number
    Returns part data or None if not found
    """
    try:
        url = f"{REBRICKABLE_BASE_URL}/parts/{part_num}/"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return None
        else:
            response.raise_for_status()
            
    except requests.exceptions.RequestException as e:
        print(f"Error searching for part {part_num}: {e}")
        raise


@cache_result(element_cache)
def search_element(element_id):
    """
    Search for a LEGO element by element ID
    Returns element data or None if not found
    """
    try:
        url = f"{REBRICKABLE_BASE_URL}/elements/{element_id}/"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return None
        else:
            response.raise_for_status()
            
    except requests.exceptions.RequestException as e:
        print(f"Error searching for element {element_id}: {e}")
        raise


@cache_result(part_cache)
def get_part_colors(part_num):
    """
    Get color variations for a specific part
    """
    try:
        url = f"{REBRICKABLE_BASE_URL}/parts/{part_num}/colors/"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
            
    except requests.exceptions.RequestException as e:
        print(f"Error getting colors for part {part_num}: {e}")
        raise


def validate_input(search_term):
    """
    Validate search input
    Returns tuple (is_valid, error_message)
    """
    if not search_term or not search_term.strip():
        return False, "Search term cannot be empty"
    
    # Remove any whitespace
    search_term = search_term.strip()
    
    # Check length (most LEGO part numbers are 4-7 characters)
    if len(search_term) < 3 or len(search_term) > 20:
        return False, "Search term must be between 3 and 20 characters"
    
    # Check for invalid characters (allow alphanumeric and common LEGO separators)
    import re
    if not re.match(r'^[a-zA-Z0-9\-_]+$', search_term):
        return False, "Search term contains invalid characters"
    
    return True, ""