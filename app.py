import os
import logging
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Enable CORS for all routes
CORS(app)

# In-memory data storage for demo purposes
users = [
    {"id": 1, "name": "John Doe", "email": "john@example.com"},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}
]

# Counter for generating new user IDs
next_user_id = 3

# Error handler for 404
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Not Found",
        "message": "The requested resource was not found",
        "status_code": 404
    }), 404

# Error handler for 400
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "error": "Bad Request",
        "message": "The request was invalid",
        "status_code": 400
    }), 400

# Error handler for 500
@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal Server Error",
        "message": "An internal error occurred",
        "status_code": 500
    }), 500

# Documentation page route
@app.route('/')
def documentation():
    return render_template('index.html')

# API Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "API is running successfully",
        "timestamp": "2025-09-01T00:00:00Z"
    })

# Get all users
@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users"""
    try:
        return jsonify({
            "status": "success",
            "data": users,
            "count": len(users)
        })
    except Exception as e:
        logging.error(f"Error getting users: {str(e)}")
        return jsonify({
            "error": "Internal Server Error",
            "message": "Failed to retrieve users"
        }), 500

# Get a specific user by ID
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get a specific user by ID"""
    try:
        user = next((u for u in users if u["id"] == user_id), None)
        if user:
            return jsonify({
                "status": "success",
                "data": user
            })
        else:
            return jsonify({
                "error": "Not Found",
                "message": f"User with ID {user_id} not found"
            }), 404
    except Exception as e:
        logging.error(f"Error getting user {user_id}: {str(e)}")
        return jsonify({
            "error": "Internal Server Error",
            "message": "Failed to retrieve user"
        }), 500

# Create a new user
@app.route('/api/users', methods=['POST'])
def create_user():
    """Create a new user"""
    global next_user_id
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "error": "Bad Request",
                "message": "No JSON data provided"
            }), 400
        
        if 'name' not in data or 'email' not in data:
            return jsonify({
                "error": "Bad Request",
                "message": "Name and email are required"
            }), 400
        
        # Check if email already exists
        if any(u["email"] == data["email"] for u in users):
            return jsonify({
                "error": "Conflict",
                "message": "User with this email already exists"
            }), 409
        
        new_user = {
            "id": next_user_id,
            "name": data["name"],
            "email": data["email"]
        }
        
        users.append(new_user)
        next_user_id += 1
        
        return jsonify({
            "status": "success",
            "message": "User created successfully",
            "data": new_user
        }), 201
        
    except Exception as e:
        logging.error(f"Error creating user: {str(e)}")
        return jsonify({
            "error": "Internal Server Error",
            "message": "Failed to create user"
        }), 500

# Update a user
@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update a user"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "error": "Bad Request",
                "message": "No JSON data provided"
            }), 400
        
        user_index = next((i for i, u in enumerate(users) if u["id"] == user_id), None)
        
        if user_index is None:
            return jsonify({
                "error": "Not Found",
                "message": f"User with ID {user_id} not found"
            }), 404
        
        # Update user fields
        if 'name' in data:
            users[user_index]['name'] = data['name']
        if 'email' in data:
            # Check if email already exists for another user
            if any(u["email"] == data["email"] and u["id"] != user_id for u in users):
                return jsonify({
                    "error": "Conflict",
                    "message": "User with this email already exists"
                }), 409
            users[user_index]['email'] = data['email']
        
        return jsonify({
            "status": "success",
            "message": "User updated successfully",
            "data": users[user_index]
        })
        
    except Exception as e:
        logging.error(f"Error updating user {user_id}: {str(e)}")
        return jsonify({
            "error": "Internal Server Error",
            "message": "Failed to update user"
        }), 500

# Delete a user
@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user"""
    try:
        user_index = next((i for i, u in enumerate(users) if u["id"] == user_id), None)
        
        if user_index is None:
            return jsonify({
                "error": "Not Found",
                "message": f"User with ID {user_id} not found"
            }), 404
        
        deleted_user = users.pop(user_index)
        
        return jsonify({
            "status": "success",
            "message": "User deleted successfully",
            "data": deleted_user
        })
        
    except Exception as e:
        logging.error(f"Error deleting user {user_id}: {str(e)}")
        return jsonify({
            "error": "Internal Server Error",
            "message": "Failed to delete user"
        }), 500

# Get API information
@app.route('/api/info', methods=['GET'])
def api_info():
    """Get API information"""
    return jsonify({
        "name": "Simple Flask REST API",
        "version": "1.0.0",
        "description": "A simple REST API built with Flask",
        "endpoints": {
            "health": "/api/health",
            "users": "/api/users",
            "user_detail": "/api/users/<id>",
            "info": "/api/info"
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
