from flask import Blueprint, request, jsonify
from services.liquidity_service import LiquidityService

liquidity_bp = Blueprint('liquidity', __name__)

@liquidity_bp.route('/get_liquidity', methods=['POST'])
def get_liquidity():
    """API for fetching liquidity data (reusable for all exchanges)"""
    try:
        exchange_name = request.args.get('exchange', 'okx')  # Default to OKX if not provided
        
        data = request.json
        country = data.get('country')
        payment_methods = data.get('payment_methods', [])
        
        if not country or not payment_methods:
            return jsonify({"error": "Country and payment methods are required"}), 400
        
        # Find fiat table name, passing exchange_name for correct mapping
        fiat_table = LiquidityService.get_fiat_table_by_country(country, exchange_name)
        
        if not fiat_table:
            return jsonify({"error": f"Country '{country}' is not recognized for exchange '{exchange_name}'"}), 404

        payment_methods = set(payment_methods)
        result = LiquidityService.calculate_liquidity(fiat_table, payment_methods, exchange_name)
        return jsonify(result)
    
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
    except FileNotFoundError as e:
        return jsonify({"error": f"Database or mapping file not found: {str(e)}"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500