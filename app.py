from flask import Flask, render_template, request, jsonify
from rebrickable_api import search_part, search_element, validate_input
import traceback

app = Flask(__name__)


@app.route('/')
def index():
    """Render the main search page"""
    return render_template('index.html')


@app.route('/api/search/part/<part_num>')
def api_search_part(part_num):
    """
    API endpoint to search for a LEGO part
    Returns JSON response with part data
    """
    try:
        # Validate input
        is_valid, error_message = validate_input(part_num)
        if not is_valid:
            return jsonify({
                'success': False,
                'error': error_message
            }), 400
        
        # Search for the part
        part_data = search_part(part_num)
        
        if part_data is None:
            return jsonify({
                'success': False,
                'error': f"Part '{part_num}' not found"
            }), 404
        
        return jsonify({
            'success': True,
            'data': part_data
        })
        
    except Exception as e:
        print(f"Error in part search: {e}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': 'An error occurred while searching for the part'
        }), 500


@app.route('/api/search/element/<element_id>')
def api_search_element(element_id):
    """
    API endpoint to search for a LEGO element
    Returns JSON response with element data
    """
    try:
        # Validate input
        is_valid, error_message = validate_input(element_id)
        if not is_valid:
            return jsonify({
                'success': False,
                'error': error_message
            }), 400
        
        # Search for the element
        element_data = search_element(element_id)
        
        if element_data is None:
            return jsonify({
                'success': False,
                'error': f"Element '{element_id}' not found"
            }), 404
        
        return jsonify({
            'success': True,
            'data': element_data
        })
        
    except Exception as e:
        print(f"Error in element search: {e}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': 'An error occurred while searching for the element'
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    # Run in debug mode for development
    app.run(debug=True, host='0.0.0.0', port=5000)