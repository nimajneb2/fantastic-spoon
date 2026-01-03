# LEGO Part & Element Search - Rebrickable Integration

A Flask web application that integrates with the Rebrickable API to search for LEGO part and element numbers.

## Features

- **Part Search**: Look up LEGO parts by part number
  - View part details including name, category, material, and year range
  - See all available colors for the part
  - View element IDs for each color variant
  - Display part images from Rebrickable

- **Element Search**: Look up specific LEGO elements by element ID
  - View element details including the associated part and color
  - Display element images with the specific color
  - See design IDs and related information

- **User-Friendly Interface**:
  - Clean, modern design with responsive layout
  - Tab-based navigation between part and element search
  - Real-time search with loading indicators
  - Error handling with helpful messages
  - Mobile-responsive design

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create a virtual environment and activate it:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your Rebrickable API key:
   - Register for a free account at https://rebrickable.com/
   - Navigate to Settings > API to get your API key
   - Create a `.env` file or set the environment variable:
   ```bash
   export REBRICKABLE_API_KEY=your_api_key_here
   ```
   - Alternatively, copy `.env.example` to `.env` and add your key

## Usage

### Running the Application

1. Ensure your API key is set (see Installation step 4)

2. Start the Flask development server:
```bash
python app.py
```

3. Open your browser and navigate to:
```
http://localhost:5000
```

### Using the Search

**Part Search:**
- Enter a LEGO part number (e.g., `3001`, `2456`, `3003`)
- Click "Search" to view part details and available colors

**Element Search:**
- Enter a LEGO element ID (e.g., `300121`, `4211010`)
- Click "Search" to view element details including part and color information

## API Integration

This application uses the Rebrickable API v3. The API provides access to a comprehensive LEGO database including:
- Parts and their properties
- Elements (parts in specific colors)
- Color information
- Images and external IDs

### API Key (Required)

The Rebrickable API requires authentication. You must obtain a free API key to use this application:

1. Register for a free account at https://rebrickable.com/
2. Navigate to Settings > API
3. Copy your API key
4. Set it as an environment variable:

```bash
export REBRICKABLE_API_KEY=your_api_key_here
```

Or create a `.env` file in the project root (see `.env.example`)

## Project Structure

```
.
├── app.py                  # Main Flask application
├── rebrickable_api.py      # Rebrickable API integration module
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html         # Main HTML template
├── static/
│   └── css/
│       └── style.css      # Styles and responsive design
└── README.md              # This file
```

## API Endpoints

### GET /api/search/part
Search for a part by part number.

**Query Parameters:**
- `part_num` (required): LEGO part number

**Example:**
```
GET /api/search/part?part_num=3001
```

### GET /api/search/element
Search for an element by element ID.

**Query Parameters:**
- `element_id` (required): LEGO element ID

**Example:**
```
GET /api/search/element?element_id=300121
```

## Error Handling

The application includes comprehensive error handling:
- Input validation for part numbers and element IDs
- API error handling (404, 401, 503, etc.)
- Network error handling
- User-friendly error messages
- Graceful degradation when images fail to load

## Caching

The application implements LRU caching to minimize API calls:
- Part data cached (128 entries)
- Part color data cached (128 entries)
- Element data cached (128 entries)
- Part search results cached (128 entries)

## Technologies Used

- **Backend**: Flask 3.0.0
- **HTTP Client**: Requests 2.31.0
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **API**: Rebrickable API v3

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Data provided by [Rebrickable](https://rebrickable.com/)
- LEGO® is a trademark of the LEGO Group
