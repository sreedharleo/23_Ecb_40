def solve_knapsack(capacity, items):
    """
    Solves the standard 0/1 Knapsack problem using Dynamic Programming.
    
    Parameters:
    - capacity (int): The total MechanicHours available at the depot.
    - items (list): List of dicts, each containing:
      {"TaskID": str, "Duration": int, "Impact": int}
      
    Returns:
    - selected_items (list): The list of items selected for this depot.
    - total_impact (int): The sum of impacts of selected items.
    """
    n = len(items)
    if n == 0 or capacity <= 0:
        return [], 0

    # dp[i][w] will store the maximum impact for the first i items with capacity w
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    # Build table dp[][] in bottom-up manner
    for i in range(1, n + 1):
        item = items[i - 1]
        duration = item["Duration"]
        impact = item["Impact"]

        for w in range(capacity + 1):
            if duration <= w:
                # We can choose to either exclude or include the item
                dp[i][w] = max(
                    dp[i - 1][w],
                    dp[i - 1][w - duration] + impact
                )
            else:
                # The item's duration is too large to fit in capacity w
                dp[i][w] = dp[i - 1][w]

    # Trace back to find which items were selected
    selected_items = []
    w = capacity
    for i in range(n, 0, -1):
        # If the value changed, it means the item was included
        if dp[i][w] != dp[i - 1][w]:
            item = items[i - 1]
            selected_items.append(item)
            w -= item["Duration"]

    total_impact = dp[n][capacity]
    return selected_items, total_impact


def schedule_vehicles(depots, vehicles):
    """
    Coordinates scheduling of vehicles across multiple depots sequentially.
    
    Parameters:
    - depots (list): List of depots [{"ID": int, "MechanicHours": int}]
    - vehicles (list): List of vehicles [{"TaskID": str, "Duration": int, "Impact": int}]
    
    Returns:
    - result (dict): Contains the schedule allocations and summary.
    """
    # Create copies of lists to avoid mutating input parameters
    remaining_vehicles = list(vehicles)
    
    # Sort depots by capacity (MechanicHours) descending to prioritize allocating large stations first
    sorted_depots = sorted(depots, key=lambda x: x["MechanicHours"], reverse=True)
    
    schedule = []
    total_scheduled_impact = 0
    total_allocated_hours = 0
    
    for depot in sorted_depots:
        depot_id = depot["ID"]
        capacity = depot["MechanicHours"]
        
        # Solve 0/1 Knapsack for this depot with the remaining vehicles
        assigned_for_depot, depot_impact = solve_knapsack(capacity, remaining_vehicles)
        
        depot_hours = sum(v["Duration"] for v in assigned_for_depot)
        
        schedule.append({
            "depotId": depot_id,
            "allocatedHours": depot_hours,
            "totalImpact": depot_impact,
            "vehicles": assigned_for_depot
        })
        
        total_scheduled_impact += depot_impact
        total_allocated_hours += depot_hours
        
        # Remove assigned vehicles from the pool of remaining vehicles
        assigned_ids = {v["TaskID"] for v in assigned_for_depot}
        remaining_vehicles = [v for v in remaining_vehicles if v["TaskID"] not in assigned_ids]
        
    return {
        "schedule": schedule,
        "unassigned_vehicles": remaining_vehicles,
        "totalImpact": total_scheduled_impact,
        "totalAllocatedHours": total_allocated_hours
    }
