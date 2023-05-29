import requests
import os

def estimate_entry_waiting_time():
    response = requests.get('https://beaconcha.in/api/v1/validators/queue')
    data = response.json()
    beacon_entering = data["data"]["beaconchain_entering"]
    active_validators = data["data"]["validatorscount"]

    churn_limit = max(4, active_validators // 65536)
    activation_rate_per_epoch = churn_limit  # 4 validators per epoch (every 6.4 minutes) as a minimum

    waiting_time_epochs = beacon_entering / activation_rate_per_epoch
    waiting_time_seconds = waiting_time_epochs * 12 * 32  # 12 seconds per slot, 32 slots per epoch

    waiting_time_minutes = waiting_time_seconds // 60
    waiting_time_seconds = round(waiting_time_seconds % 60)
    waiting_time_hours = waiting_time_minutes // 60
    waiting_time_minutes = round(waiting_time_minutes % 60)

    return waiting_time_hours, waiting_time_minutes, waiting_time_seconds, beacon_entering, active_validators
def estimate_exit_waiting_time():
    validator_queue_url = "https://beaconcha.in/api/v1/validators/queue"
    validator_queue_data = requests.get(validator_queue_url).json()
    beacon_exiting = validator_queue_data["data"]["beaconchain_exiting"]
    active_validators = validator_queue_data["data"]["validatorscount"]

    churn_limit = max(4, active_validators // 65536)

    waiting_time_epochs = beacon_exiting / churn_limit
    waiting_time_seconds = waiting_time_epochs * 12 * 32  # 12 seconds per slot, 32 slots per epoch

    waiting_time_minutes = waiting_time_seconds // 60
    waiting_time_seconds = round(waiting_time_seconds % 60)
    waiting_time_hours = waiting_time_minutes // 60
    waiting_time_minutes = round(waiting_time_minutes % 60)

    return waiting_time_hours, waiting_time_minutes, waiting_time_seconds, beacon_exiting, active_validators

def generate_html(entry_waiting_time_hours, entry_waiting_time_minutes, beacon_entering, exit_waiting_time_hours, exit_waiting_time_minutes, beacon_exiting, active_validators):
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Validator Queue</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            background-color: #f4f4f4;
            padding: 1rem;
        }}

        h1 {{
            color: #333;
            font-size: 2rem;
        }}

        p {{
            font-size: 1.1rem;
            color: #666;
            margin-bottom: 1.5rem;
        }}
    </style>
</head>
<body>
    <h1>Ethereum Validator Queue</h1>
    <p>Estimated waiting time for new validators: {entry_waiting_time_hours} hours and {entry_waiting_time_minutes} minutes</p>
    <p>Pending validators (entry queue): {beacon_entering}</p>
    <p>Estimated waiting time for exit queue: {exit_waiting_time_hours} hours and {exit_waiting_time_minutes} minutes</p>
    <p>Pending validators (exit queue): {beacon_exiting}</p>
    <p>Active validators: {active_validators}</p>
    <hr>
    <p>
        <a href="https://github.com/etheralpha/validatorqueue-com" target="_blank">
          <svg height="40" width="40" aria-hidden="true" viewBox="0 0 16 16" version="1.1" data-view-component="true" class="github-link"><path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path></svg>
        </a>
    </p>
</body>
</html>"""

    with open("index.html", "w") as f:
        f.write(html_content)

entry_waiting_time_hours, entry_waiting_time_minutes, entry_waiting_time_seconds, beacon_entering, active_validators = estimate_entry_waiting_time()
exit_waiting_time_hours, exit_waiting_time_minutes, exit_waiting_time_seconds, beacon_exiting, active_validators = estimate_exit_waiting_time()

generate_html(entry_waiting_time_hours, entry_waiting_time_minutes, beacon_entering, exit_waiting_time_hours, exit_waiting_time_minutes, beacon_exiting, active_validators)
