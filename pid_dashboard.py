import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import plotly.graph_objs as go
import pandas as pd
import time

# PID Controller Class
class PIDController:
    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp  # Proportional gain
        self.Ki = Ki  # Integral gain
        self.Kd = Kd  # Derivative gain
        self.previous_error = 0
        self.integral = 0

    def compute(self, setpoint, process_variable, dt):
        error = setpoint - process_variable
        self.integral += error * dt
        derivative = (error - self.previous_error) / dt
        output = (self.Kp * error) + (self.Ki * self.integral) + (self.Kd * derivative)
        self.previous_error = error
        return output, error

# Initialize PID Controller
pid = PIDController(Kp=1.0, Ki=0.1, Kd=0.05)

# Simulated process variables
setpoint = 100
process_variable = 50
dt = 0.1

# Create a DataFrame to store real-time data
data = pd.DataFrame(columns=["Time", "Setpoint", "Process Variable", "Error", "Control Output", "Integral", "Adjusting Parameter"])

# Dash App Initialization
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Enhanced PID Controller Dashboard"),

    # Sliders for PID Parameters
    html.Div([
        html.Label("Proportional Gain (Kp):"),
        dcc.Slider(id="kp-slider", min=0.1, max=5.0, step=0.1, value=1.0),
        html.Label("Integral Gain (Ki):"),
        dcc.Slider(id="ki-slider", min=0.0, max=1.0, step=0.01, value=0.1),
        html.Label("Derivative Gain (Kd):"),
        dcc.Slider(id="kd-slider", min=0.0, max=1.0, step=0.01, value=0.05)
    ], style={"margin": "20px"}),

    # Live Graph
    dcc.Graph(id="live-graph"),

    # Data Export Button
    html.Button("Download Data", id="download-button"),
    dcc.Download(id="download-dataframe-csv"),

    # Text Display for Adjusting Parameter
    html.Div(id="adjusting-parameter-text", style={"margin": "20px", "fontSize": "20px", "color": "blue"}),

    # Alerts and Warnings
    html.Div(id="alerts-text", style={"margin": "20px", "fontSize": "20px", "color": "red"}),

    # Update Interval
    dcc.Interval(id="interval-component", interval=100, n_intervals=0)  # Update every 100ms
])

# Callback to update PID parameters from sliders
@app.callback(
    [Output("adjusting-parameter-text", "children"),
     Output("kp-slider", "value"),
     Output("ki-slider", "value"),
     Output("kd-slider", "value")],
    [Input("kp-slider", "value"),
     Input("ki-slider", "value"),
     Input("kd-slider", "value")]
)
def update_pid_parameters(kp, ki, kd):
    pid.Kp = kp
    pid.Ki = ki
    pid.Kd = kd

    adjusting_parameter = "Adjusting Parameter: "
    if kp != pid.Kp:
        adjusting_parameter += "Proportional Gain (Kp)"
    elif ki != pid.Ki:
        adjusting_parameter += "Integral Gain (Ki)"
    elif kd != pid.Kd:
        adjusting_parameter += "Derivative Gain (Kd)"
    else:
        adjusting_parameter += "None"

    return adjusting_parameter, kp, ki, kd

# Callback to update graph
@app.callback(
    [Output("live-graph", "figure"),
     Output("alerts-text", "children")],
    [Input("interval-component", "n_intervals"),
     Input("kp-slider", "value"),
     Input("ki-slider", "value"),
     Input("kd-slider", "value")]
)
def update_graph(n, kp, ki, kd):
    global process_variable, data

    # Update PID parameters dynamically
    pid.Kp = kp
    pid.Ki = ki
    pid.Kd = kd

    # Compute PID output
    control_output, error = pid.compute(setpoint, process_variable, dt)
    process_variable += control_output * dt

    # Append new data
    data = pd.concat([data, pd.DataFrame({
        "Time": [time.time()],
        "Setpoint": [setpoint],
        "Process Variable": [process_variable],
        "Error": [error],
        "Control Output": [control_output],
        "Integral": [pid.integral],
        "Adjusting Parameter": ["Kp: {:.2f}, Ki: {:.2f}, Kd: {:.2f}".format(kp, ki, kd)]
    })], ignore_index=True)

    # Generate alerts based on system conditions
    alerts = ""
    if abs(error) > 10:
        alerts = f"High error detected: {error:.2f}. Adjusting system to reach setpoint."
    elif abs(control_output) > 50:
        alerts = f"Control output too high: {control_output:.2f}. Consider retuning PID gains."

    # Create live plot with steady background
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data["Time"], y=data["Setpoint"], mode="lines", name="Setpoint"))
    fig.add_trace(go.Scatter(x=data["Time"], y=data["Process Variable"], mode="lines", name="Process Variable"))
    fig.add_trace(go.Scatter(x=data["Time"], y=data["Error"], mode="lines", name="Error"))
    fig.add_trace(go.Scatter(x=data["Time"], y=data["Control Output"], mode="lines", name="Control Output"))
    fig.add_trace(go.Scatter(x=data["Time"], y=data["Integral"], mode="lines", name="Integral"))

    fig.update_layout(
        title="PID Controller Monitoring",
        xaxis_title="Time",
        yaxis_title="Value",
        xaxis_fixedrange=True,
        yaxis_fixedrange=True,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(255,255,255,1)"
    )

    return fig, alerts

# Callback to export data
@app.callback(
    Output("download-dataframe-csv", "data"),
    [Input("download-button", "n_clicks")],
    prevent_initial_call=True
)
def download_data(n_clicks):
    return dcc.send_data_frame(data.to_csv, "pid_log.csv", index=False)

if __name__ == "__main__":
    app.run_server(debug=True)
