# Vehicle Scheduler Backend (Flask)

## Output Screenshot
![Postman Output Screenshot](./screenshot.png)


This is the backend service for the **Vehicle Scheduler** application, built using **Python and Flask**. 

The application implements a customized **Multiple Knapsack Scheduling Algorithm** using Dynamic Programming from scratch (without using external algorithm libraries) to assign maintenance tasks (vehicles) to depots while maximizing business impact and adhering to capacity constraints.

---

## Technical Stack

* **Language**: Python 3.x
* **Framework**: Flask
* **Libraries**: `requests` (for external API communication), `python-dotenv` (for configuration management)

---

## Algorithmic Problem Description

This scheduling challenge maps directly to the **0/1 Multiple Knapsack Problem (MKP)**:
* **Knapsacks**: The maintenance **Depots**, where the capacity of each knapsack is defined by its `MechanicHours` budget.
* **Items**: The **Vehicles** (tasks), where each item's weight is its `Duration` (in hours) and its value is its `Impact` (business priority).
* **Objective**: Assign each task to at most one depot to maximize the sum of scheduled task impacts, ensuring no depot's total assigned task duration exceeds its `MechanicHours` capacity.

### Algorithm Details (`app/scheduler.py`)
1. **Depot Sorting**: We sort the depots in descending order of their capacity (`MechanicHours`). This greedy initialization ensures that depots with the largest bandwidth are filled optimally first.
2. **Sequential Knapsack (Dynamic Programming)**: For each depot, we solve the exact 0/1 Knapsack problem using a 2D dynamic programming array (`dp[i][w]`) on the pool of remaining unassigned vehicles.
3. **Tracking & Cleanup**: Once a subset of tasks is assigned to a depot, those tasks are extracted from the pool of remaining vehicles, and the algorithm proceeds to the next depot. Any unassignable tasks are returned in the `unassigned_vehicles` list.

---

## Project Structure

```text
vehicle-scheduler-be/
│
├── app/
│   ├── __init__.py      # App factory initialization
│   ├── config.py        # Central configuration loading (.env)
│   ├── routes.py        # Blueprint definition for the /schedule endpoint
│   ├── scheduler.py     # 0/1 Knapsack optimization algorithm
│   └── services.py      # Client APIs (Auth token caching, depots, vehicles, logs)
│
├── requirements.txt     # Python package requirements
├── run.py               # Application entrypoint
└── README.md            # Project documentation
```

---

## Setup & Running Instructions

### 1. Environment Configuration
Create a `.env` file in the project root directory (or one level up from `vehicle-scheduler-be`) with the following variables:

```env
CLIENT_ID=your_evaluation_client_id
CLIENT_SECRET=your_evaluation_client_secret
EMAIL=your_university_email
NAME=your_name
ROLL_NO=your_roll_number
ACCESS_CODE=your_access_code
```

### 2. Install Dependencies
Initialize a virtual environment and install the required modules:

```bash
# Navigate to directory
cd vehicle-scheduler-be

# Create & activate virtual environment
python -m venv venv
# On Windows Command Prompt:
venv\Scripts\activate
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1

# Install requirements
pip install -r requirements.txt
```

### 3. Run the Server
Start the local Flask development server:

```bash
python run.py
```
The server will boot and run on `http://127.0.0.1:5000`.

---

## API Reference

### `GET /schedule`
Fetches current depots and vehicles from the external test server automatically using the authorization Bearer token, schedules them, logs the audit status to the external logs API, and returns the result.

* **Response (Status 200)**:
  ```json
  {
    "schedule": [
      {
        "depotId": 3,
        "allocatedHours": 131,
        "totalImpact": 225,
        "vehicles": [
          { "TaskID": "task-uuid", "Duration": 4, "Impact": 8 },
          ...
        ]
      }
    ],
    "totalAllocatedHours": 131,
    "totalImpact": 225,
    "unassigned_vehicles": []
  }
  ```

### `POST /schedule`
Enables custom payload testing (ideal for Postman screenshots displaying **Request Body, Response, and Response Time**).

* **Headers**: `Content-Type: application/json`
* **Request Body**:
  ```json
  {
    "depots": [
      { "ID": 2, "MechanicHours": 100 },
      { "ID": 3, "MechanicHours": 150 }
    ],
    "vehicles": [
      { "TaskID": "v-1", "Duration": 25, "Impact": 80 },
      { "TaskID": "v-2", "Duration": 40, "Impact": 90 }
    ]
  }
  ```
* **Response (Status 200)**: Same format as GET.
