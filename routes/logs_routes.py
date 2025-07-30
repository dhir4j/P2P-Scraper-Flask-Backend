from flask import Blueprint, request, jsonify
from services.logs_service import LogsService

logs_bp = Blueprint('logs', __name__)

@logs_bp.route('/logs', methods=['GET'])
def get_logs():
    """API endpoint to get logs data"""
    exchange_name = request.args.get('exchange')

    if not exchange_name:
        return jsonify({"error": "Exchange name is required"}), 400

    try:
        response_data = LogsService.get_logs(exchange_name)
        
        if not response_data:
            return jsonify({"message": "No data found"}), 404
            
        return jsonify(response_data), 200

    except FileNotFoundError as e:
        return jsonify({"error": f"Database not found: {str(e)}"}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500