# PID Controller Dashboard

## **Project Overview**
This project implements a **PID Controller Dashboard** using Python and Dash. It provides a real-time visualization of process variables, setpoints, and controller outputs. The dashboard also allows dynamic tuning of PID parameters and generates alerts when critical changes occur.

---

## **Features**
- **Dynamic Parameter Adjustment:** Adjust Proportional (Σ), Integral (γ), and Derivative (δ) gains using sliders.
- **Live Visualization:** Monitor the process variable, setpoint, error, and control output.
- **Alerts and Warnings:** Get notified when the error or control output exceeds critical thresholds.
- **Data Export:** Download real-time data logs for offline analysis.
- **Steady Background:** The graph remains static while lines update dynamically.

---

## **How It Works**
The dashboard simulates a PID control system with the following components:

1. **PID Controller Equation:**
   \[ u(t) = K_p \cdot e(t) + K_i \cdot \int_{0}^{t} e(\tau) d\tau + K_d \cdot \frac{d}{dt}e(t) \]
   - **Proportional Gain (Σ):** Reacts to the magnitude of the current error.
   - **Integral Gain (γ):** Addresses accumulated past errors.
   - **Derivative Gain (δ):** Anticipates future error trends.

2. **Adjustable Parameters:**
   - Sliders dynamically modify \( K_p \), \( K_i \), and \( K_d \).

3. **Alerts:**
   - **High Error Detected:** When \( |e(t)| > 10 \).
   - **Excessive Control Output:** When control output \( u(t) > 50 \).

4. **Real-Time Plot:**
   - Visualizes live changes in:
     - Process Variable
     - Setpoint
     - Error
     - Control Output

---

## **Dependencies**
To run the project, install the following Python libraries:

```bash
pip install dash plotly pandas
```

- **Dash:** For interactive web applications.
- **Plotly:** For dynamic visualizations.
- **Pandas:** For real-time data management.

### **Optional:**
Ensure you have Python version **3.7 or later**.

```bash
python --version
```

---

## **Installation and Usage**

### **1. Clone the Repository**
```bash
git clone https://github.com/MahmoudNasrAly/Proportional-Integral-Differentiation
cd Proportional-Integral-Differentiation
```

### **2. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3. Run the Application**
```bash
python pid_dashboard.py
```

### **4. Access the Dashboard**
Open your browser and navigate to:
```
http://127.0.0.1:8050/
```

---

## **Requirements File**

Save the following in a `requirements.txt` file:
```
dash
plotly
pandas
```

---

## **Git Ignore File**

Add the following in a `.gitignore` file to avoid committing unnecessary files:
```
__pycache__/
*.pyc
*.log
*.csv
.DS_Store
```

---

## **Examples**

### **Example 1: High Error Detected**
- **Scenario:** The process variable deviates significantly from the setpoint.
- **Alert Triggered:** "High error detected: 15. Adjusting system to reach setpoint."
- **Resolution:** Tune \( K_p \) to reduce the error faster.

### **Example 2: Excessive Control Output**
- **Scenario:** The control output exceeds safe operating levels.
- **Alert Triggered:** "Control output too high: 55. Consider retuning PID gains."
- **Resolution:** Adjust \( K_d \) to dampen the system response.

---

## **Contact and Support**
For issues or contributions, please submit a GitHub issue or pull request.

