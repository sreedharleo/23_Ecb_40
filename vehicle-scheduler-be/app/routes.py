from flask import Blueprint, jsonify, request
from app.services import AffordMedService
from app.scheduler import schedule_vehicles

bp = Blueprint('routes', __name__)
service = AffordMedService()

@bp.route('/schedule', methods=['GET', 'POST'])
def get_schedule():
    try:
        depots = None
        vehicles = None

        # Check if the request is a POST and has JSON body data
        if request.method == 'POST' and request.is_json:
            req_data = request.get_json(silent=True)
            if req_data:
                depots = req_data.get('depots')
                vehicles = req_data.get('vehicles')

        # If data was not provided in the request body, fetch from the external test server
        if not depots or not vehicles:
            depots = service.get_depots()
            vehicles = service.get_vehicles()

        # Run the optimization algorithm
        scheduled_result = schedule_vehicles(depots, vehicles)

        # Log completion to the external logs API
        total_impact = scheduled_result.get("totalImpact", 0)
        log_message = (
            f"Schedule computed. Assigned {len(scheduled_result['schedule'])} depots. "
            f"Total Impact: {total_impact}."
        )
        
        service.send_log(
            stack="backend",
            level="info",
            package="routes",
            message=log_message
        )

        return jsonify(scheduled_result), 200

    except Exception as e:
        # Log failure
        err_msg = f"Scheduling failed: {str(e)}"
        service.send_log(
            stack="backend",
            level="error",
            package="routes",
            message=err_msg
        )
        return jsonify({"error": str(e)}), 500
