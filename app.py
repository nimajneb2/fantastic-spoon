from flask import Flask, render_template, request, jsonify
import os
from rebrickable_api import RebrickableAPI

app = Flask(__name__)
api = RebrickableAPI(api_key=os.getenv('REBRICKABLE_API_KEY'))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/search/part', methods=['GET'])
def search_part():
    part_num = request.args.get('part_num', '').strip()
    
    if not part_num:
        return jsonify({'error': 'Part number is required'}), 400
    
    if not is_valid_part_number(part_num):
        return jsonify({'error': 'Invalid part number format'}), 400
    
    part_data = api.get_part(part_num)
    
    if 'error' in part_data:
        status_code = part_data.get('status_code', 500)
        return jsonify({'error': part_data['error']}), status_code
    
    colors_data = api.get_part_colors(part_num)
    if 'results' in colors_data:
        part_data['colors'] = colors_data['results']
    
    return jsonify(part_data)


@app.route('/api/search/element', methods=['GET'])
def search_element():
    element_id = request.args.get('element_id', '').strip()
    
    if not element_id:
        return jsonify({'error': 'Element ID is required'}), 400
    
    if not is_valid_element_id(element_id):
        return jsonify({'error': 'Invalid element ID format'}), 400
    
    element_data = api.get_element(element_id)
    
    if 'error' in element_data:
        status_code = element_data.get('status_code', 500)
        return jsonify({'error': element_data['error']}), status_code
    
    return jsonify(element_data)


@app.route('/api/search/parts', methods=['GET'])
def search_parts():
    query = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)
    
    if not query:
        return jsonify({'error': 'Search query is required'}), 400
    
    if len(query) < 2:
        return jsonify({'error': 'Search query must be at least 2 characters'}), 400
    
    if page < 1:
        return jsonify({'error': 'Page must be greater than 0'}), 400
    
    results = api.search_parts(query, page)
    
    if 'error' in results:
        status_code = results.get('status_code', 500)
        return jsonify({'error': results['error']}), status_code
    
    return jsonify(results)


def is_valid_part_number(part_num: str) -> bool:
    if not part_num or len(part_num) > 50:
        return False
    return all(c.isalnum() or c in '-_.' for c in part_num)


def is_valid_element_id(element_id: str) -> bool:
    if not element_id or len(element_id) > 20:
        return False
    return element_id.isdigit()


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
