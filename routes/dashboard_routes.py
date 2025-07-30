from flask import Blueprint, request, jsonify
from services.dashboard_service import DashboardService

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    """API endpoint to get dashboard data"""
    try:
        exchange_name = request.args.get('exchange', 'okx')
        data = DashboardService.fetch_dashboard_data(exchange_name)
        return jsonify(data)
    except FileNotFoundError as e:
        return jsonify({"error": f"Database not found: {str(e)}"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@dashboard_bp.route('/calculate', methods=['GET'])
def calculate_dashboard_metrics():
    """API to calculate dashboard metrics (reusable for all exchanges)"""
    try:
        exchange_name = request.args.get('exchange', 'okx')  # Default to okx if not provided
        result = DashboardService.calculate_metrics(exchange_name)
        return jsonify(result)
    except FileNotFoundError as e:
        return jsonify({"error": f"Database not found: {str(e)}"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500