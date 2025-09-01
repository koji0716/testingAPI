document.addEventListener('DOMContentLoaded', function() {
    const methodSelect = document.getElementById('method');
    const endpointSelect = document.getElementById('endpoint');
    const requestBodySection = document.getElementById('request-body-section');
    const requestBodyTextarea = document.getElementById('request-body');
    const testApiButton = document.getElementById('test-api');
    const responseElement = document.getElementById('response');

    // Show/hide request body section based on method
    function toggleRequestBodySection() {
        const method = methodSelect.value;
        if (method === 'POST' || method === 'PUT') {
            requestBodySection.style.display = 'block';
        } else {
            requestBodySection.style.display = 'none';
        }
    }

    // Update endpoint options based on method
    function updateEndpointOptions() {
        const method = methodSelect.value;
        endpointSelect.innerHTML = '';
        
        switch(method) {
            case 'GET':
                endpointSelect.innerHTML = `
                    <option value="/api/health">Health Check</option>
                    <option value="/api/info">API Info</option>
                    <option value="/api/users">All Users</option>
                    <option value="/api/users/1">User by ID (ID: 1)</option>
                    <option value="/api/users/2">User by ID (ID: 2)</option>
                `;
                break;
            case 'POST':
                endpointSelect.innerHTML = `
                    <option value="/api/users">Create User</option>
                `;
                requestBodyTextarea.value = JSON.stringify({
                    "name": "New User",
                    "email": "newuser@example.com"
                }, null, 2);
                break;
            case 'PUT':
                endpointSelect.innerHTML = `
                    <option value="/api/users/1">Update User (ID: 1)</option>
                    <option value="/api/users/2">Update User (ID: 2)</option>
                `;
                requestBodyTextarea.value = JSON.stringify({
                    "name": "Updated Name",
                    "email": "updated@example.com"
                }, null, 2);
                break;
            case 'DELETE':
                endpointSelect.innerHTML = `
                    <option value="/api/users/1">Delete User (ID: 1)</option>
                    <option value="/api/users/2">Delete User (ID: 2)</option>
                `;
                break;
        }
    }

    // Test API endpoint
    async function testApi() {
        const method = methodSelect.value;
        const endpoint = endpointSelect.value;
        const requestBody = requestBodyTextarea.value;

        testApiButton.disabled = true;
        testApiButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Loading...';
        
        try {
            const options = {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                }
            };

            if ((method === 'POST' || method === 'PUT') && requestBody.trim()) {
                try {
                    JSON.parse(requestBody); // Validate JSON
                    options.body = requestBody;
                } catch (e) {
                    throw new Error('Invalid JSON in request body');
                }
            }

            const response = await fetch(endpoint, options);
            const data = await response.json();
            
            const formattedResponse = {
                status: response.status,
                statusText: response.statusText,
                headers: {
                    'Content-Type': response.headers.get('Content-Type'),
                    'Date': response.headers.get('Date')
                },
                body: data
            };

            responseElement.textContent = JSON.stringify(formattedResponse, null, 2);
            responseElement.className = response.ok ? 
                'bg-success text-white p-3 rounded' : 
                'bg-danger text-white p-3 rounded';
                
        } catch (error) {
            responseElement.textContent = JSON.stringify({
                error: 'Request Failed',
                message: error.message,
                timestamp: new Date().toISOString()
            }, null, 2);
            responseElement.className = 'bg-danger text-white p-3 rounded';
        } finally {
            testApiButton.disabled = false;
            testApiButton.innerHTML = '<i class="fas fa-paper-plane me-2"></i>Send Request';
        }
    }

    // Event listeners
    methodSelect.addEventListener('change', function() {
        toggleRequestBodySection();
        updateEndpointOptions();
    });

    testApiButton.addEventListener('click', testApi);

    // Initialize
    toggleRequestBodySection();
    updateEndpointOptions();

    // Auto-refresh API status
    async function checkApiStatus() {
        try {
            const response = await fetch('/api/health');
            const data = await response.json();
            
            const statusBadge = document.querySelector('.badge.bg-success');
            if (statusBadge && response.ok) {
                statusBadge.innerHTML = '<i class="fas fa-check-circle me-1"></i>API Status: Online';
                statusBadge.className = 'badge bg-success fs-6';
            } else {
                statusBadge.innerHTML = '<i class="fas fa-times-circle me-1"></i>API Status: Offline';
                statusBadge.className = 'badge bg-danger fs-6';
            }
        } catch (error) {
            const statusBadge = document.querySelector('.badge.bg-success, .badge.bg-danger');
            if (statusBadge) {
                statusBadge.innerHTML = '<i class="fas fa-times-circle me-1"></i>API Status: Offline';
                statusBadge.className = 'badge bg-danger fs-6';
            }
        }
    }

    // Check API status every 30 seconds
    setInterval(checkApiStatus, 30000);
});
