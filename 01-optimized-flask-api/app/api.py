"""
Secure Flask API - Production Ready
Enhanced version with health checks, structured logging, and security headers
"""

from flask import Flask, request, jsonify
import logging
import os
import time
from datetime import datetime
from functools import wraps

# Import configuration
from .config import Config
from .utils import validate_ip_address, setup_logging


# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Setup structured logging
logger = setup_logging()

# Metrics storage (in production, use Prometheus)
metrics = {
    "requests_total": 0,
    "requests_success": 0,
    "requests_failed": 0,
    "startup_time": datetime.utcnow().isoformat()
}


def require_api_key(f):
    """Decorator to validate API key"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('X-API-Key')
        
        if not auth_header:
            logger.warning(f"Missing API key from {request.remote_addr}")
            metrics["requests_failed"] += 1
            return jsonify({
                "success": False,
                "error": "API key required"
            }), 401
        
        if auth_header != app.config['API_KEY']:
            logger.warning(f"Invalid API key from {request.remote_addr}")
            metrics["requests_failed"] += 1
            return jsonify({
                "success": False,
                "error": "Invalid API key"
            }), 401
        
        return f(*args, **kwargs)
    
    return decorated_function


@app.before_request
def before_request():
    """Log all incoming requests"""
    metrics["requests_total"] += 1
    request.start_time = time.time()
    logger.info(f"Incoming request: {request.method} {request.path} from {request.remote_addr}")


@app.after_request
def after_request(response):
    """Add security headers and log response"""
    # Security headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    
    # Log response time
    if hasattr(request, 'start_time'):
        duration = time.time() - request.start_time
        logger.info(f"Request completed: {request.method} {request.path} - "
                   f"Status: {response.status_code} - Duration: {duration:.3f}s")
    
    return response


@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for container orchestration
    Returns detailed health status
    """
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "Optimized Flask API",
        "version": app.config['VERSION'],
        "uptime_seconds": (datetime.utcnow() - 
                          datetime.fromisoformat(metrics["startup_time"])).total_seconds(),
        "environment": app.config['ENVIRONMENT']
    }
    
    logger.debug("Health check requested")
    return jsonify(health_status), 200


@app.route('/ready', methods=['GET'])
def readiness_check():
    """
    Readiness probe for Kubernetes
    Returns 200 if app is ready to serve traffic
    """
    # Add checks for database, cache, etc. here
    # For now, simple check
    return jsonify({
        "ready": True,
        "checks": {
            "api": "ok"
        }
    }), 200


@app.route('/metrics', methods=['GET'])
@require_api_key
def get_metrics():
    """
    Prometheus-compatible metrics endpoint
    Requires API key authentication
    """
    return jsonify(metrics), 200


@app.route('/api/v1/process', methods=['POST'])
@require_api_key
def process_data():
    """
    Main API endpoint - processes incoming data
    Requires API key authentication
    """
    try:
        # Get JSON data
        data = request.get_json()
        
        if not data:
            logger.error("No JSON data provided")
            metrics["requests_failed"] += 1
            return jsonify({
                "success": False,
                "error": "No data provided"
            }), 400
        
        # Validate required fields
        if 'action' not in data:
            logger.error("Missing 'action' field")
            metrics["requests_failed"] += 1
            return jsonify({
                "success": False,
                "error": "Missing 'action' field"
            }), 400
        
        action = data.get('action')
        logger.info(f"Processing action: {action}")
        
        # Process based on action type
        if action == 'validate_ip':
            ip_address = data.get('ip')
            if not ip_address:
                return jsonify({
                    "success": False,
                    "error": "IP address required"
                }), 400
            
            is_valid = validate_ip_address(ip_address)
            
            metrics["requests_success"] += 1
            return jsonify({
                "success": True,
                "action": action,
                "ip": ip_address,
                "valid": is_valid,
                "timestamp": datetime.utcnow().isoformat()
            }), 200
        
        elif action == 'echo':
            # Simple echo for testing
            metrics["requests_success"] += 1
            return jsonify({
                "success": True,
                "action": action,
                "data": data.get('data', {}),
                "timestamp": datetime.utcnow().isoformat()
            }), 200
        
        else:
            logger.warning(f"Unknown action: {action}")
            metrics["requests_failed"] += 1
            return jsonify({
                "success": False,
                "error": f"Unknown action: {action}"
            }), 400
    
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        metrics["requests_failed"] += 1
        return jsonify({
            "success": False,
            "error": "Internal server error"
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    logger.warning(f"404 error: {request.path}")
    return jsonify({
        "success": False,
        "error": "Endpoint not found"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"500 error: {str(error)}")
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500


if __name__ == '__main__':
    # This is only used for local development
    # In production, use gunicorn or uwsgi
    logger.info(f"Starting Flask API in {app.config['ENVIRONMENT']} mode")
    logger.info(f"Debug mode: {app.config['DEBUG']}")
    
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )