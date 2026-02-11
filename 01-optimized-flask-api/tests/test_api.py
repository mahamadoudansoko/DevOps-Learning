"""
Unit tests for Flask API
Run with: pytest tests/
"""

import pytest
import json
from app.api import app


@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    app.config['API_KEY'] = 'test-api-key'
    
    with app.test_client() as client:
        yield client


@pytest.fixture
def api_headers():
    """Return headers with valid API key"""
    return {
        'X-API-Key': 'test-api-key',
        'Content-Type': 'application/json'
    }


class TestHealthEndpoints:
    """Test health and readiness endpoints"""
    
    def test_health_check(self, client):
        """Test /health endpoint"""
        response = client.get('/health')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'timestamp' in data
        assert 'version' in data
    
    def test_readiness_check(self, client):
        """Test /ready endpoint"""
        response = client.get('/ready')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['ready'] == True
        assert 'checks' in data


class TestAuthentication:
    """Test API key authentication"""
    
    def test_missing_api_key(self, client):
        """Test request without API key returns 401"""
        response = client.get('/metrics')
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data['success'] == False
        assert 'API key required' in data['error']
    
    def test_invalid_api_key(self, client):
        """Test request with invalid API key returns 401"""
        headers = {'X-API-Key': 'wrong-key'}
        response = client.get('/metrics', headers=headers)
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data['success'] == False
        assert 'Invalid API key' in data['error']
    
    def test_valid_api_key(self, client, api_headers):
        """Test request with valid API key succeeds"""
        response = client.get('/metrics', headers=api_headers)
        
        assert response.status_code == 200


class TestMetricsEndpoint:
    """Test metrics endpoint"""
    
    def test_get_metrics(self, client, api_headers):
        """Test /metrics returns proper metrics"""
        response = client.get('/metrics', headers=api_headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'requests_total' in data
        assert 'requests_success' in data
        assert 'requests_failed' in data


class TestProcessEndpoint:
    """Test /api/v1/process endpoint"""
    
    def test_process_missing_data(self, client, api_headers):
        """Test process endpoint with no data returns 400"""
        response = client.post('/api/v1/process', headers=api_headers)
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] == False
    
    def test_process_missing_action(self, client, api_headers):
        """Test process endpoint without 'action' field returns 400"""
        payload = {'data': 'test'}
        response = client.post(
            '/api/v1/process',
            headers=api_headers,
            data=json.dumps(payload)
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'action' in data['error']
    
    def test_process_echo_action(self, client, api_headers):
        """Test process endpoint with echo action"""
        payload = {
            'action': 'echo',
            'data': {'message': 'hello world'}
        }
        response = client.post(
            '/api/v1/process',
            headers=api_headers,
            data=json.dumps(payload)
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert data['action'] == 'echo'
        assert data['data']['message'] == 'hello world'
    
    def test_process_validate_ip_action(self, client, api_headers):
        """Test process endpoint with validate_ip action"""
        payload = {
            'action': 'validate_ip',
            'ip': '192.168.1.1'
        }
        response = client.post(
            '/api/v1/process',
            headers=api_headers,
            data=json.dumps(payload)
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert data['valid'] == True
        assert data['ip'] == '192.168.1.1'
    
    def test_process_validate_invalid_ip(self, client, api_headers):
        """Test validate_ip with invalid IP"""
        payload = {
            'action': 'validate_ip',
            'ip': 'not-an-ip'
        }
        response = client.post(
            '/api/v1/process',
            headers=api_headers,
            data=json.dumps(payload)
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert data['valid'] == False
    
    def test_process_unknown_action(self, client, api_headers):
        """Test process endpoint with unknown action"""
        payload = {'action': 'unknown_action'}
        response = client.post(
            '/api/v1/process',
            headers=api_headers,
            data=json.dumps(payload)
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] == False
        assert 'Unknown action' in data['error']


class TestErrorHandlers:
    """Test custom error handlers"""
    
    def test_404_not_found(self, client):
        """Test 404 handler"""
        response = client.get('/nonexistent-endpoint')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['success'] == False
        assert 'not found' in data['error'].lower()


class TestSecurityHeaders:
    """Test security headers are present"""
    
    def test_security_headers_present(self, client):
        """Test that security headers are added to responses"""
        response = client.get('/health')
        
        assert 'X-Content-Type-Options' in response.headers
        assert response.headers['X-Content-Type-Options'] == 'nosniff'
        
        assert 'X-Frame-Options' in response.headers
        assert response.headers['X-Frame-Options'] == 'DENY'
        
        assert 'X-XSS-Protection' in response.headers

