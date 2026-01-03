// LEGO Search Application JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const searchPartBtn = document.getElementById('searchPartBtn');
    const searchElementBtn = document.getElementById('searchElementBtn');
    const partInput = document.getElementById('partInput');
    const elementInput = document.getElementById('elementInput');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const searchResults = document.getElementById('searchResults');

    // Add enter key support for search inputs
    partInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            searchPart();
        }
    });

    elementInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            searchElement();
        }
    });

    // Search button event listeners
    searchPartBtn.addEventListener('click', searchPart);
    searchElementBtn.addEventListener('click', searchElement);

    // Validation helper
    function validateSearchTerm(term) {
        if (!term || !term.trim()) {
            return { valid: false, message: 'Please enter a search term' };
        }
        
        term = term.trim();
        
        if (term.length < 3 || term.length > 20) {
            return { valid: false, message: 'Search term must be between 3 and 20 characters' };
        }
        
        // Check for invalid characters
        const regex = /^[a-zA-Z0-9\-_]+$/;
        if (!regex.test(term)) {
            return { valid: false, message: 'Search term contains invalid characters' };
        }
        
        return { valid: true };
    }

    // Show loading state
    function showLoading() {
        searchResults.innerHTML = '';
        loadingSpinner.classList.remove('d-none');
        searchResults.classList.add('d-none');
    }

    // Hide loading state
    function hideLoading() {
        loadingSpinner.classList.add('d-none');
        searchResults.classList.remove('d-none');
    }

    // Show error message
    function showError(message) {
        hideLoading();
        searchResults.innerHTML = `
            <div class="alert alert-error fade-in">
                <i class="fas fa-exclamation-triangle me-2"></i>
                ${message}
            </div>
        `;
    }

    // Show "no results" message
    function showNoResults(searchTerm, searchType) {
        hideLoading();
        const searchTypeText = searchType === 'part' ? 'part' : 'element';
        searchResults.innerHTML = `
            <div class="no-results fade-in">
                <i class="fas fa-search"></i>
                <h5>No ${searchTypeText} found</h5>
                <p class="mb-0">No ${searchTypeText} matching "${searchTerm}" was found in the Rebrickable database.</p>
                <p class="mt-2">Try checking your spelling or using a different search term.</p>
            </div>
        `;
    }

    // Format part data for display
    function formatPartData(data) {
        const part = data.data;
        const imageUrl = part.part_img_url || 'https://rebrickable.com/static/img/npd.png';
        const categoryName = part.part_cat_id || 'Unknown Category';
        
        return `
            <div class="card search-result-card fade-in">
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-3 text-center">
                            <img src="${imageUrl}" alt="${part.name}" class="part-image">
                        </div>
                        <div class="col-md-9">
                            <div class="d-flex justify-content-between align-items-start mb-3">
                                <div>
                                    <h4 class="mb-1">${part.name || 'Unknown Part'}</h4>
                                    <span class="badge-category">
                                        <i class="fas fa-tag me-1"></i>Part #${part.part_num}
                                    </span>
                                </div>
                            </div>
                            
                            <div class="info-item">
                                <span class="info-label">
                                    <i class="fas fa-folder me-1"></i>Category:
                                </span>
                                ${categoryName}
                            </div>
                            
                            ${part.part_material ? `
                                <div class="info-item">
                                    <span class="info-label">
                                        <i class="fas fa-industry me-1"></i>Material:
                                    </span>
                                    ${part.part_material}
                                </div>
                            ` : ''}
                            
                            ${part.year_from || part.year_to ? `
                                <div class="info-item">
                                    <span class="info-label">
                                        <i class="fas fa-calendar me-1"></i>Years:
                                    </span>
                                    ${part.year_from || 'Unknown'} - ${part.year_to || 'Present'}
                                </div>
                            ` : ''}
                            
                            <div class="info-item">
                                <span class="info-label">
                                    <i class="fas fa-link me-1"></i>Rebrickable:
                                </span>
                                <a href="https://rebrickable.com/parts/${part.part_num}/" 
                                   target="_blank" rel="noopener noreferrer">
                                    View on Rebrickable <i class="fas fa-external-link-alt ms-1 small"></i>
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    // Format element data for display
    function formatElementData(data) {
        const element = data.data;
        const imageUrl = element.part.part_img_url || 'https://rebrickable.com/static/img/npd.png';
        
        return `
            <div class="card search-result-card fade-in">
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-3 text-center">
                            <img src="${imageUrl}" alt="${element.part.name}" class="part-image">
                        </div>
                        <div class="col-md-9">
                            <div class="d-flex justify-content-between align-items-start mb-3">
                                <div>
                                    <h4 class="mb-1">${element.part.name || 'Unknown Part'}</h4>
                                    <span class="badge-category">
                                        <i class="fas fa-barcode me-1"></i>Element #${element.id}
                                    </span>
                                </div>
                            </div>
                            
                            <div class="info-item">
                                <span class="info-label">
                                    <i class="fas fa-puzzle-piece me-1"></i>Part Number:
                                </span>
                                ${element.part.part_num}
                            </div>
                            
                            ${element.color ? `
                                <div class="info-item">
                                    <span class="info-label">
                                        <i class="fas fa-palette me-1"></i>Color:
                                    </span>
                                    <span style="display: inline-block; width: 16px; height: 16px; 
                                           background-color: #${element.color.rgb}; 
                                           border: 1px solid #ccc; vertical-align: middle; margin-right: 8px;"></span>
                                    ${element.color.name} (${element.color.id})
                                </div>
                            ` : ''}
                            
                            ${element.part.part_cat_id ? `
                                <div class="info-item">
                                    <span class="info-label">
                                        <i class="fas fa-folder me-1"></i>Category:
                                    </span>
                                    ${element.part.part_cat_id}
                                </div>
                            ` : ''}
                            
                            ${element.element_img_url ? `
                                <div class="info-item">
                                    <span class="info-label">
                                        <i class="fas fa-image me-1"></i>Element Image:
                                    </span>
                                    <a href="${element.element_img_url}" target="_blank" rel="noopener noreferrer">
                                        View Image <i class="fas fa-external-link-alt ms-1 small"></i>
                                    </a>
                                </div>
                            ` : ''}
                            
                            <div class="info-item">
                                <span class="info-label">
                                    <i class="fas fa-link me-1"></i>Rebrickable:
                                </span>
                                <a href="https://rebrickable.com/parts/${element.part.part_num}/" 
                                   target="_blank" rel="noopener noreferrer">
                                    View Part Details <i class="fas fa-external-link-alt ms-1 small"></i>
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    // Search for a part
    async function searchPart() {
        const searchTerm = partInput.value.trim();
        
        // Validate input
        const validation = validateSearchTerm(searchTerm);
        if (!validation.valid) {
            showError(validation.message);
            return;
        }
        
        showLoading();
        
        try {
            const response = await fetch(`/api/search/part/${encodeURIComponent(searchTerm)}`);
            const data = await response.json();
            
            if (response.ok) {
                if (data.success) {
                    hideLoading();
                    searchResults.innerHTML = formatPartData(data);
                } else {
                    showError(data.error || 'An error occurred while searching');
                }
            } else {
                if (response.status === 404) {
                    showNoResults(searchTerm, 'part');
                } else if (response.status === 400) {
                    showError(data.error || 'Invalid search term');
                } else {
                    showError('An error occurred while connecting to the server');
                }
            }
        } catch (error) {
            console.error('Search error:', error);
            showError('Unable to connect to the server. Please try again later.');
        }
    }

    // Search for an element
    async function searchElement() {
        const searchTerm = elementInput.value.trim();
        
        // Validate input
        const validation = validateSearchTerm(searchTerm);
        if (!validation.valid) {
            showError(validation.message);
            return;
        }
        
        showLoading();
        
        try {
            const response = await fetch(`/api/search/element/${encodeURIComponent(searchTerm)}`);
            const data = await response.json();
            
            if (response.ok) {
                if (data.success) {
                    hideLoading();
                    searchResults.innerHTML = formatElementData(data);
                } else {
                    showError(data.error || 'An error occurred while searching');
                }
            } else {
                if (response.status === 404) {
                    showNoResults(searchTerm, 'element');
                } else if (response.status === 400) {
                    showError(data.error || 'Invalid search term');
                } else {
                    showError('An error occurred while connecting to the server');
                }
            }
        } catch (error) {
            console.error('Search error:', error);
            showError('Unable to connect to the server. Please try again later.');
        }
    }

    // Clear results when switching tabs
    document.getElementById('part-tab').addEventListener('click', function() {
        searchResults.innerHTML = '';
    });

    document.getElementById('element-tab').addEventListener('click', function() {
        searchResults.innerHTML = '';
    });
});