# Hospital Management System - Complete Project Code

## Table of Contents
1. [requirements.txt](#requirementstxt)
2. [run_hospital_system.py](#run_hospital_systempy)
3. [flask_app.py](#flask_apppy)
4. [tkinter_flask_gui.py](#tkinter_flask_guipy)
5. [create_hospital_database.py](#create_hospital_databasepy)
6. [README.md](#readmemd)
7. [USAGE_INSTRUCTIONS.md](#usage_instructionsmd)

---

## requirements.txt

```txt
streamlit==1.51.0
mysql-connector-python==9.5.0
pandas==2.3.3
plotly==6.4.0
tkcalendar==1.6.1
flask==3.1.2
flask-cors==6.0.1
requests==2.32.5
```

---

## run_hospital_system.py

```python
import subprocess
import time
import sys
import os
import threading
import tkinter as tk
from tkinter import messagebox

def start_flask_server():
    """Start Flask server in background"""
    try:
        print("🚀 Starting Flask API server...")
        # Set environment variable to disable Flask debug mode for subprocess
        env = os.environ.copy()
        env['FLASK_ENV'] = 'production'
        
        # Start Flask server
        flask_process = subprocess.Popen([
            sys.executable, "flask_app.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
        
        return flask_process
    except Exception as e:
        print(f"❌ Failed to start Flask server: {e}")
        return None

def start_tkinter_gui():
    """Start Tkinter GUI"""
    try:
        print("🖥️ Starting Tkinter GUI...")
        print("⏳ Waiting for Flask server to start...")
        
        # Wait for Flask to be ready (check connection)
        import urllib.request
        import urllib.error
        
        max_retries = 15
        retry_count = 0
        flask_ready = False
        
        while retry_count < max_retries and not flask_ready:
            try:
                time.sleep(1)
                urllib.request.urlopen('http://localhost:5000/api/test', timeout=1)
                flask_ready = True
                print("✅ Flask server is ready!")
            except (urllib.error.URLError, Exception):
                retry_count += 1
                print(f"⏳ Waiting for Flask... ({retry_count}/{max_retries})")
        
        if not flask_ready:
            raise Exception("Flask server failed to start after 15 seconds")
        
        # Import and run GUI
        from tkinter_flask_gui import HospitalFlaskGUI
        
        root = tk.Tk()
        app = HospitalFlaskGUI(root)
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Failed to start GUI: {e}")
        messagebox.showerror("Error", f"Failed to start GUI: {e}")

def main():
    """Main function to start both Flask and Tkinter"""
    print("🏥 Hospital Management System - Flask + Tkinter")
    print("=" * 50)
    
    # Start Flask server in background
    flask_process = start_flask_server()
    
    if flask_process:
        try:
            # Start Tkinter GUI in main thread
            start_tkinter_gui()
        finally:
            # Clean up Flask process when GUI closes
            print("🛑 Shutting down Flask server...")
            flask_process.terminate()
            flask_process.wait()
            print("✅ System shutdown complete")
    else:
        print("❌ Cannot start system without Flask server")

if __name__ == "__main__":
    main()
```

---


## flask_app.py

### Flask Backend API

`python
from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from datetime import datetime, date, timedelta
import json
import os

app = Flask(__name__)
CORS(app)

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'database': 'hospital_management',
    'user': 'amaanraza',
    'password': 'Amaan123!',
    'port': 3306
}

def get_db_connection():
    """Get database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

def execute_query(query, params=None, fetch_one=False, fetch_all=True):
    """Execute database query"""
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True, buffered=True)
        cursor.execute(query, params or ())
        
        if query.strip().upper().startswith('SELECT'):
            if fetch_one:
                result = cursor.fetchone()
            elif fetch_all:
                result = cursor.fetchall()
            else:
                result = cursor.rowcount
        else:
            connection.commit()
            result = cursor.lastrowid if cursor.lastrowid else cursor.rowcount
        
        cursor.close()
        connection.close()
        return result
        
    except Exception as e:
        print(f"Query execution error: {e}")
        if connection:
            connection.close()
        return None

# Custom JSON encoder for date and time objects
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        elif isinstance(obj, timedelta):
            # Convert timedelta to string format (HH:MM:SS)
            total_seconds = int(obj.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return super().default(obj)

app.json_encoder = DateTimeEncoder

# API Routes

@app.route('/api/test', methods=['GET'])
def test_connection():
    """Test API connection"""
    return jsonify({'status': 'success', 'message': 'Flask API is running'})

@app.route('/api/dashboard', methods=['GET'])
def get_dashboard_data():
    """Get dashboard statistics"""
    try:
        # Patient count
        patient_count = execute_query("SELECT COUNT(*) as count FROM patients", fetch_one=True)
        
        # Doctor count
        doctor_count = execute_query("SELECT COUNT(*) as count FROM doctors WHERE is_active = TRUE", fetch_one=True)
        
        # Today's appointments
        today_appointments = execute_query("""
            SELECT TIME_FORMAT(a.appointment_time, '%H:%i:%s') as appointment_time, 
                   a.status, a.reason,
                   p.first_name, p.last_name,
                   d.first_name as doctor_first_name, d.last_name as doctor_last_name
            FROM appointments a
            JOIN patients p ON a.patient_id = p.patient_id
            JOIN doctors d ON a.doctor_id = d.doctor_id
            WHERE a.appointment_date = CURDATE()
            ORDER BY a.appointment_time
        """)
        
        # Available rooms
        available_rooms = execute_query("SELECT COUNT(*) as count FROM rooms WHERE is_occupied = FALSE AND is_active = TRUE", fetch_one=True)
        
        return jsonify({
            'status': 'success',
            'data': {
                'patient_count': patient_count['count'] if patient_count else 0,
                'doctor_count': doctor_count['count'] if doctor_count else 0,
                'appointment_count': len(today_appointments) if today_appointments else 0,
                'available_rooms': available_rooms['count'] if available_rooms else 0,
                'today_appointments': today_appointments or []
            }
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/patients', methods=['GET'])
def get_patients():
    """Get all patients"""
    try:
        patients = execute_query("""
            SELECT patient_id, first_name, last_name, phone, email, date_of_birth, gender
            FROM patients 
            ORDER BY first_name, last_name
        """)
        
        return jsonify({
            'status': 'success',
            'data': patients or []
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/patients/search', methods=['POST'])
def search_patients():
    """Search patients"""
    try:
        data = request.get_json()
        search_term = data.get('search_term', '')
        
        if not search_term:
            return jsonify({'status': 'error', 'message': 'Search term is required'}), 400
        
        search_pattern = f"%{search_term}%"
        patients = execute_query("""
            SELECT patient_id, first_name, last_name, phone, email, date_of_birth
            FROM patients 
            WHERE first_name LIKE %s OR last_name LIKE %s OR phone LIKE %s OR email LIKE %s
            ORDER BY first_name, last_name
        """, (search_pattern, search_pattern, search_pattern, search_pattern))
        
        return jsonify({
            'status': 'success',
            'data': patients or []
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/patients', methods=['POST'])
def add_patient():
    """Add new patient"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['first_name', 'last_name', 'date_of_birth', 'gender']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'status': 'error', 'message': f'{field} is required'}), 400
        
        # Insert patient
        patient_id = execute_query("""
            INSERT INTO patients (first_name, last_name, date_of_birth, gender, phone, email, address, blood_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data['first_name'],
            data['last_name'],
            data['date_of_birth'],
            data['gender'],
            data.get('phone'),
            data.get('email'),
            data.get('address'),
            data.get('blood_type')
        ), fetch_all=False)
        
        if patient_id:
            return jsonify({
                'status': 'success',
                'message': 'Patient registered successfully',
                'patient_id': patient_id
            })
        else:
            return jsonify({'status': 'error', 'message': 'Failed to register patient'}), 500
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/doctors', methods=['GET'])
def get_doctors():
    """Get all doctors"""
    try:
        doctors = execute_query("""
            SELECT doctor_id, first_name, last_name, specialization, phone, email
            FROM doctors 
            WHERE is_active = TRUE
            ORDER BY specialization, first_name, last_name
        """)
        
        return jsonify({
            'status': 'success',
            'data': doctors or []
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/appointments', methods=['POST'])
def book_appointment():
    """Book new appointment"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['patient_id', 'doctor_id', 'appointment_date', 'appointment_time']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'status': 'error', 'message': f'{field} is required'}), 400
        
        # Check if patient exists
        patient_check = execute_query("""
            SELECT patient_id FROM patients WHERE patient_id = %s
        """, (data['patient_id'],), fetch_one=True)
        
        if not patient_check:
            return jsonify({'status': 'error', 'message': f'Patient ID {data["patient_id"]} does not exist'}), 400
        
        # Check if doctor exists
        doctor_check = execute_query("""
            SELECT doctor_id FROM doctors WHERE doctor_id = %s AND is_active = TRUE
        """, (data['doctor_id'],), fetch_one=True)
        
        if not doctor_check:
            return jsonify({'status': 'error', 'message': f'Doctor ID {data["doctor_id"]} does not exist or is not active'}), 400
        
        # Check doctor availability
        availability = execute_query("""
            SELECT COUNT(*) as count FROM appointments 
            WHERE doctor_id = %s AND appointment_date = %s AND appointment_time = %s 
            AND status IN ('Scheduled', 'In Progress')
        """, (data['doctor_id'], data['appointment_date'], data['appointment_time']), fetch_one=True)
        
        if availability and availability['count'] > 0:
            return jsonify({'status': 'error', 'message': 'Doctor not available at that time'}), 400
        
        # Book appointment
        appointment_id = execute_query("""
            INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, reason, status)
            VALUES (%s, %s, %s, %s, %s, 'Scheduled')
        """, (
            data['patient_id'],
            data['doctor_id'],
            data['appointment_date'],
            data['appointment_time'],
            data.get('reason', '')
        ), fetch_all=False)
        
        if appointment_id:
            return jsonify({
                'status': 'success',
                'message': 'Appointment booked successfully',
                'appointment_id': appointment_id
            })
        else:
            return jsonify({'status': 'error', 'message': 'Failed to book appointment'}), 500
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/appointments/today', methods=['GET'])
def get_today_appointments():
    """Get today's appointments"""
    try:
        appointments = execute_query("""
            SELECT a.appointment_id, TIME_FORMAT(a.appointment_time, '%H:%i:%s') as appointment_time, 
                   a.status, a.reason,
                   p.first_name, p.last_name, p.phone,
                   d.first_name as doctor_first_name, d.last_name as doctor_last_name,
                   d.specialization
            FROM appointments a
            JOIN patients p ON a.patient_id = p.patient_id
            JOIN doctors d ON a.doctor_id = d.doctor_id
            WHERE a.appointment_date = CURDATE()
            ORDER BY a.appointment_time
        """)
        
        return jsonify({
            'status': 'success',
            'data': appointments or []
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/appointments/<int:appointment_id>/status', methods=['PUT'])
def update_appointment_status(appointment_id):
    """Update appointment status"""
    try:
        data = request.get_json()
        status = data.get('status')
        
        if not status:
            return jsonify({'status': 'error', 'message': 'Status is required'}), 400
        
        result = execute_query("""
            UPDATE appointments SET status = %s WHERE appointment_id = %s
        """, (status, appointment_id), fetch_all=False)
        
        if result:
            return jsonify({
                'status': 'success',
                'message': 'Appointment status updated successfully'
            })
        else:
            return jsonify({'status': 'error', 'message': 'Failed to update appointment status'}), 500
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/patients/<int:patient_id>/medical-records', methods=['GET'])
def get_patient_medical_records(patient_id):
    """Get patient medical records"""
    try:
        records = execute_query("""
            SELECT mr.record_id, mr.visit_date, mr.diagnosis, mr.treatment, 
                   mr.prescription, mr.notes,
                   d.first_name as doctor_first_name, d.last_name as doctor_last_name,
                   d.specialization
            FROM medical_records mr
            JOIN doctors d ON mr.doctor_id = d.doctor_id
            WHERE mr.patient_id = %s
            ORDER BY mr.visit_date DESC
        """, (patient_id,))
        
        return jsonify({
            'status': 'success',
            'data': records or []
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/validate/patient/<int:patient_id>', methods=['GET'])
def validate_patient(patient_id):
    """Validate if patient exists"""
    try:
        patient = execute_query("""
            SELECT patient_id, first_name, last_name FROM patients WHERE patient_id = %s
        """, (patient_id,), fetch_one=True)
        
        if patient:
            return jsonify({
                'status': 'success',
                'exists': True,
                'patient': patient
            })
        else:
            return jsonify({
                'status': 'success',
                'exists': False,
                'message': f'Patient ID {patient_id} does not exist'
            })
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/validate/doctor/<int:doctor_id>', methods=['GET'])
def validate_doctor(doctor_id):
    """Validate if doctor exists"""
    try:
        doctor = execute_query("""
            SELECT doctor_id, first_name, last_name, specialization FROM doctors 
            WHERE doctor_id = %s AND is_active = TRUE
        """, (doctor_id,), fetch_one=True)
        
        if doctor:
            return jsonify({
                'status': 'success',
                'exists': True,
                'doctor': doctor
            })
        else:
            return jsonify({
                'status': 'success',
                'exists': False,
                'message': f'Doctor ID {doctor_id} does not exist or is not active'
            })
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

def quick_sort_records(records, sort_by='visit_date', order='desc'):
    """Quick sort implementation for medical records"""
    if len(records) <= 1:
        return records
    
    def compare_records(a, b, sort_field, sort_order):
        """Compare two records based on sort field and order"""
        val_a = a.get(sort_field, '')
        val_b = b.get(sort_field, '')
        
        # Handle different data types
        if sort_field == 'visit_date':
            # Convert date strings to comparable format
            try:
                from datetime import datetime
                if isinstance(val_a, str):
                    val_a = datetime.strptime(val_a.split(',')[1].strip() if ',' in val_a else val_a, '%d %b %Y %H:%M:%S %Z')
                if isinstance(val_b, str):
                    val_b = datetime.strptime(val_b.split(',')[1].strip() if ',' in val_b else val_b, '%d %b %Y %H:%M:%S %Z')
            except:
                pass
        elif sort_field in ['patient_id', 'doctor_id', 'record_id']:
            # Convert to integers for numeric comparison
            try:
                val_a = int(val_a)
                val_b = int(val_b)
            except:
                pass
        else:
            # String comparison (case insensitive)
            val_a = str(val_a).lower()
            val_b = str(val_b).lower()
        
        if sort_order == 'asc':
            return val_a < val_b
        else:
            return val_a > val_b
    
    pivot = records[len(records) // 2]
    left = [x for x in records if compare_records(x, pivot, sort_by, order)]
    middle = [x for x in records if x == pivot]
    right = [x for x in records if compare_records(pivot, x, sort_by, order)]
    
    return quick_sort_records(left, sort_by, order) + middle + quick_sort_records(right, sort_by, order)

@app.route('/api/records/sorted', methods=['POST'])
def get_sorted_records():
    """Get all medical records sorted using quick sort algorithm"""
    try:
        data = request.get_json() or {}
        sort_by = data.get('sort_by', 'visit_date')  # Default sort by visit date
        order = data.get('order', 'desc')  # Default descending order
        record_type = data.get('record_type', 'all')  # all, patient_specific, doctor_specific
        
        # Validate sort parameters
        valid_sort_fields = ['visit_date', 'patient_id', 'doctor_id', 'diagnosis', 'specialization', 'record_id']
        if sort_by not in valid_sort_fields:
            return jsonify({'status': 'error', 'message': f'Invalid sort field. Use one of: {valid_sort_fields}'}), 400
        
        if order not in ['asc', 'desc']:
            return jsonify({'status': 'error', 'message': 'Order must be "asc" or "desc"'}), 400
        
        # Get all medical records with patient and doctor information
        if record_type == 'patient_specific' and data.get('patient_id'):
            query = """
            SELECT mr.record_id, mr.patient_id, mr.doctor_id, mr.visit_date, 
                   mr.diagnosis, mr.treatment, mr.prescription, mr.notes,
                   p.first_name as patient_first_name, p.last_name as patient_last_name,
                   d.first_name as doctor_first_name, d.last_name as doctor_last_name,
                   d.specialization
            FROM medical_records mr
            JOIN patients p ON mr.patient_id = p.patient_id
            JOIN doctors d ON mr.doctor_id = d.doctor_id
            WHERE mr.patient_id = %s
            """
            records = execute_query(query, (data['patient_id'],))
        elif record_type == 'doctor_specific' and data.get('doctor_id'):
            query = """
            SELECT mr.record_id, mr.patient_id, mr.doctor_id, mr.visit_date, 
                   mr.diagnosis, mr.treatment, mr.prescription, mr.notes,
                   p.first_name as patient_first_name, p.last_name as patient_last_name,
                   d.first_name as doctor_first_name, d.last_name as doctor_last_name,
                   d.specialization
            FROM medical_records mr
            JOIN patients p ON mr.patient_id = p.patient_id
            JOIN doctors d ON mr.doctor_id = d.doctor_id
            WHERE mr.doctor_id = %s
            """
            records = execute_query(query, (data['doctor_id'],))
        else:
            # Get all records
            query = """
            SELECT mr.record_id, mr.patient_id, mr.doctor_id, mr.visit_date, 
                   mr.diagnosis, mr.treatment, mr.prescription, mr.notes,
                   p.first_name as patient_first_name, p.last_name as patient_last_name,
                   d.first_name as doctor_first_name, d.last_name as doctor_last_name,
                   d.specialization
            FROM medical_records mr
            JOIN patients p ON mr.patient_id = p.patient_id
            JOIN doctors d ON mr.doctor_id = d.doctor_id
            """
            records = execute_query(query)
        
        if not records:
            return jsonify({
                'status': 'success',
                'data': [],
                'sort_info': {
                    'sort_by': sort_by,
                    'order': order,
                    'algorithm': 'Quick Sort',
                    'record_count': 0
                }
            })
        
        # Convert to list of dictionaries for sorting
        if hasattr(records, 'to_dict'):
            records_list = records.to_dict('records')
        else:
            records_list = records if isinstance(records, list) else []
        
        # Apply quick sort
        sorted_records = quick_sort_records(records_list, sort_by, order)
        
        return jsonify({
            'status': 'success',
            'data': sorted_records,
            'sort_info': {
                'sort_by': sort_by,
                'order': order,
                'algorithm': 'Quick Sort',
                'record_count': len(sorted_records),
                'message': f'Records sorted by {sort_by} in {order}ending order using Quick Sort algorithm'
            }
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/patients/sorted', methods=['POST'])
def get_sorted_patients():
    """Get all patients sorted using quick sort algorithm"""
    try:
        data = request.get_json() or {}
        sort_by = data.get('sort_by', 'last_name')  # Default sort by last name
        order = data.get('order', 'asc')  # Default ascending order
        
        # Validate sort parameters
        valid_sort_fields = ['patient_id', 'first_name', 'last_name', 'date_of_birth', 'gender', 'phone', 'email']
        if sort_by not in valid_sort_fields:
            return jsonify({'status': 'error', 'message': f'Invalid sort field. Use one of: {valid_sort_fields}'}), 400
        
        # Get all patients
        query = """
        SELECT patient_id, first_name, last_name, date_of_birth, gender, phone, email, address, blood_type
        FROM patients 
        """
        patients = execute_query(query)
        
        if not patients:
            return jsonify({
                'status': 'success',
                'data': [],
                'sort_info': {
                    'sort_by': sort_by,
                    'order': order,
                    'algorithm': 'Quick Sort',
                    'record_count': 0
                }
            })
        
        # Convert to list of dictionaries for sorting
        if hasattr(patients, 'to_dict'):
            patients_list = patients.to_dict('records')
        else:
            patients_list = patients if isinstance(patients, list) else []
        
        # Apply quick sort (reuse the same function with appropriate field)
        sorted_patients = quick_sort_records(patients_list, sort_by, order)
        
        return jsonify({
            'status': 'success',
            'data': sorted_patients,
            'sort_info': {
                'sort_by': sort_by,
                'order': order,
                'algorithm': 'Quick Sort',
                'record_count': len(sorted_patients),
                'message': f'Patients sorted by {sort_by} in {order}ending order using Quick Sort algorithm'
            }
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/appointments/sorted', methods=['POST'])
def get_sorted_appointments():
    """Get all appointments sorted using quick sort algorithm"""
    try:
        data = request.get_json() or {}
        sort_by = data.get('sort_by', 'appointment_date')  # Default sort by appointment date
        order = data.get('order', 'desc')  # Default descending order
        
        # Validate sort parameters
        valid_sort_fields = ['appointment_id', 'patient_id', 'doctor_id', 'appointment_date', 'appointment_time', 'status']
        if sort_by not in valid_sort_fields:
            return jsonify({'status': 'error', 'message': f'Invalid sort field. Use one of: {valid_sort_fields}'}), 400
        
        # Get all appointments with patient and doctor information
        query = """
        SELECT a.appointment_id, a.patient_id, a.doctor_id, a.appointment_date, 
               TIME_FORMAT(a.appointment_time, '%H:%i:%s') as appointment_time, 
               a.status, a.reason,
               p.first_name as patient_first_name, p.last_name as patient_last_name,
               d.first_name as doctor_first_name, d.last_name as doctor_last_name,
               d.specialization
        FROM appointments a
        JOIN patients p ON a.patient_id = p.patient_id
        JOIN doctors d ON a.doctor_id = d.doctor_id
        """
        appointments = execute_query(query)
        
        if not appointments:
            return jsonify({
                'status': 'success',
                'data': [],
                'sort_info': {
                    'sort_by': sort_by,
                    'order': order,
                    'algorithm': 'Quick Sort',
                    'record_count': 0
                }
            })
        
        # Convert to list of dictionaries for sorting
        if hasattr(appointments, 'to_dict'):
            appointments_list = appointments.to_dict('records')
        else:
            appointments_list = appointments if isinstance(appointments, list) else []
        
        # Apply quick sort
        sorted_appointments = quick_sort_records(appointments_list, sort_by, order)
        
        return jsonify({
            'status': 'success',
            'data': sorted_appointments,
            'sort_info': {
                'sort_by': sort_by,
                'order': order,
                'algorithm': 'Quick Sort',
                'record_count': len(sorted_appointments),
                'message': f'Appointments sorted by {sort_by} in {order}ending order using Quick Sort algorithm'
            }
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Flask Hospital Management API...")
    print("📡 API will be available at: http://localhost:5000")
    print("🔗 Test connection: http://localhost:5000/api/test")
    
    # Check if running in production mode (from subprocess)
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    
    app.run(debug=debug_mode, host='0.0.0.0', port=5000, use_reloader=False)
`

---


## tkinter_flask_gui.py

### Tkinter GUI Frontend

`python
import tkinter as tk
from tkinter import ttk, messagebox, font
from tkcalendar import DateEntry
from datetime import date, datetime
import requests
import json
import threading
import time
import math

class HospitalFlaskGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🏥 MedFlow Pro - Advanced Hospital Management System")
        self.root.geometry("1600x1000")
        self.root.state('zoomed')  # Maximize window on Windows
        self.root.configure(bg='#0a0e27')  # Deep space blue
        
        # Perfect color scheme - Medical Professional Theme
        self.colors = {
            'primary': '#1e3a8a',      # Medical blue
            'secondary': '#1e40af',    # Bright blue  
            'accent': '#dc2626',       # Medical red
            'success': '#059669',      # Medical green
            'warning': '#d97706',      # Amber warning
            'info': '#0284c7',        # Sky blue
            'light': '#f8fafc',       # Pure light
            'dark': '#0a0e27',        # Deep space
            'card_bg': '#ffffff',     # Pure white
            'card_hover': '#f1f5f9',  # Light hover
            'text_primary': '#1e293b', # Slate dark
            'text_secondary': '#64748b', # Slate medium
            'text_light': '#ffffff',   # Pure white
            'border': '#e2e8f0',      # Light border
            'shadow': '#00000010',     # Subtle shadow
            'gradient_start': '#1e3a8a',
            'gradient_end': '#3b82f6'
        }
        
        # Perfect typography
        self.fonts = {
            'title': ('Segoe UI', 28, 'bold'),
            'subtitle': ('Segoe UI', 14),
            'heading': ('Segoe UI', 18, 'bold'),
            'subheading': ('Segoe UI', 14, 'bold'),
            'body': ('Segoe UI', 11),
            'button': ('Segoe UI', 12, 'bold'),
            'small': ('Segoe UI', 9),
            'metric': ('Segoe UI', 32, 'bold'),
            'icon': ('Segoe UI Emoji', 24)
        }
        
        # Animation variables
        self.animation_speed = 10
        self.hover_effects = {}
        
        # API base URL
        self.api_base = "http://localhost:5000/api"
        
        # Configure perfect styling
        self.configure_perfect_styles()
        
        # Test API connection
        self.test_api_connection()
        
        # Create perfect GUI
        self.create_perfect_widgets()
        
    def test_api_connection(self):
        """Test Flask API connection"""
        try:
            response = requests.get(f"{self.api_base}/test", timeout=5)
            if response.status_code == 200:
                print("✅ Flask API connection successful!")
                messagebox.showinfo("Success", "✅ Connected to Flask API successfully!")
            else:
                raise Exception("API not responding")
        except Exception as e:
            print(f"❌ Flask API connection failed: {e}")
            messagebox.showerror("API Error", 
                               f"❌ Cannot connect to Flask API!\n\n"
                               f"Please ensure Flask server is running:\n"
                               f"python flask_app.py\n\n"
                               f"Error: {e}")
            return False
        return True
    
    def configure_perfect_styles(self):
        """Configure perfect professional TTK styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Perfect notebook styling
        style.configure('Perfect.TNotebook', 
                       background=self.colors['dark'],
                       borderwidth=0,
                       tabmargins=[0, 0, 0, 0])
        
        style.configure('Perfect.TNotebook.Tab', 
                       background=self.colors['secondary'],
                       foreground=self.colors['text_light'],
                       padding=[25, 15],
                       font=self.fonts['button'],
                       borderwidth=0,
                       focuscolor='none')
        
        style.map('Perfect.TNotebook.Tab',
                 background=[('selected', self.colors['primary']),
                           ('active', self.colors['info']),
                           ('!active', self.colors['secondary'])],
                 foreground=[('selected', self.colors['text_light']),
                           ('active', self.colors['text_light'])])
        
        # Perfect treeview styling
        style.configure('Perfect.Treeview',
                       background=self.colors['card_bg'],
                       foreground=self.colors['text_primary'],
                       fieldbackground=self.colors['card_bg'],
                       font=self.fonts['body'],
                       borderwidth=0,
                       relief='flat',
                       rowheight=35)
        
        style.configure('Perfect.Treeview.Heading',
                       background=self.colors['primary'],
                       foreground=self.colors['text_light'],
                       font=self.fonts['subheading'],
                       borderwidth=0,
                       relief='flat')
        
        style.map('Perfect.Treeview',
                 background=[('selected', self.colors['info']),
                           ('focus', self.colors['card_hover'])])
        
        # Perfect combobox styling
        style.configure('Perfect.TCombobox',
                       fieldbackground=self.colors['card_bg'],
                       background=self.colors['card_bg'],
                       borderwidth=2,
                       relief='solid',
                       bordercolor=self.colors['border'],
                       font=self.fonts['body'])
        
        style.map('Perfect.TCombobox',
                 bordercolor=[('focus', self.colors['primary']),
                            ('active', self.colors['info'])])
    
    def create_hover_effect(self, widget, enter_color, leave_color):
        """Create smooth hover effects for widgets"""
        def on_enter(event):
            widget.configure(bg=enter_color)
        
        def on_leave(event):
            widget.configure(bg=leave_color)
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
    
    def create_perfect_button(self, parent, text, command, bg_color, hover_color=None, **kwargs):
        """Create a perfect modern button with hover effects"""
        if hover_color is None:
            # Darken the color for hover effect
            hover_color = self.darken_color(bg_color, 0.1)
        
        button = tk.Button(parent, 
                          text=text,
                          command=command,
                          bg=bg_color,
                          fg=self.colors['text_light'],
                          font=self.fonts['button'],
                          relief='flat',
                          bd=0,
                          cursor='hand2',
                          padx=25,
                          pady=12,
                          **kwargs)
        
        self.create_hover_effect(button, hover_color, bg_color)
        return button
    
    def darken_color(self, color, factor):
        """Darken a hex color by a factor"""
        if color.startswith('#'):
            color = color[1:]
        
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        darkened = tuple(int(c * (1 - factor)) for c in rgb)
        return f"#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}"
    
    def create_gradient_frame(self, parent, width, height, color1, color2):
        """Create a gradient background frame"""
        canvas = tk.Canvas(parent, width=width, height=height, highlightthickness=0)
        
        # Create gradient effect
        for i in range(height):
            ratio = i / height
            r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
            r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
            
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            
            color = f"#{r:02x}{g:02x}{b:02x}"
            canvas.create_line(0, i, width, i, fill=color)
        
        return canvas
    
    def create_perfect_metric_card(self, parent, icon, title, value, color, row, col):
        """Create a perfect metric card with advanced styling"""
        # Main card container with shadow effect
        card_container = tk.Frame(parent, bg=self.colors['light'])
        card_container.grid(row=row, column=col, padx=15, pady=15, sticky='ew')
        
        # Card with rounded corners effect (simulated with borders)
        card = tk.Frame(card_container, bg=color, relief='flat', bd=0)
        card.pack(fill='both', expand=True, padx=3, pady=3)
        
        # Card content with perfect spacing
        content = tk.Frame(card, bg=color)
        content.pack(fill='both', expand=True, padx=30, pady=25)
        
        # Icon with perfect positioning
        icon_label = tk.Label(content, text=icon, 
                             font=self.fonts['icon'], 
                             bg=color, fg='white')
        icon_label.pack(pady=(0, 10))
        
        # Metric value with perfect typography
        metric_label = tk.Label(content, text=value, 
                               font=self.fonts['metric'], 
                               bg=color, fg='white')
        metric_label.pack()
        
        # Title with perfect spacing
        title_label = tk.Label(content, text=title, 
                              font=self.fonts['subheading'], 
                              bg=color, fg='white')
        title_label.pack(pady=(8, 0))
        
        # Add subtle hover effect
        hover_color = self.darken_color(color, 0.1)
        self.create_hover_effect(card, hover_color, color)
        
        return {
            'card': card,
            'metric_label': metric_label,
            'title_label': title_label,
            'icon_label': icon_label
        }
    
    def create_perfect_form_field(self, parent, label_text, row, col):
        """Create a perfect form field label"""
        label = tk.Label(parent, text=label_text, 
                        font=self.fonts['subheading'], 
                        bg=self.colors['card_bg'],
                        fg=self.colors['text_primary'])
        label.grid(row=row, column=col, sticky='w', pady=15, padx=15)
        return label
    
    def create_perfect_entry(self, parent, row, col, width=25):
        """Create a perfect entry widget with enhanced styling"""
        entry = tk.Entry(parent, width=width, 
                        font=self.fonts['body'],
                        relief='solid', 
                        bd=2,
                        highlightthickness=0,
                        borderwidth=2,
                        bg=self.colors['card_bg'],
                        fg=self.colors['text_primary'])
        entry.grid(row=row, column=col, padx=15, pady=15, sticky='ew')
        
        # Add focus effects
        def on_focus_in(event):
            entry.configure(relief='solid', bd=2)
        
        def on_focus_out(event):
            entry.configure(relief='solid', bd=1)
        
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
        
        return entry
    
    def create_perfect_sort_category(self, parent, title, options, column):
        """Create a perfect sorting category with options"""
        category_frame = tk.Frame(parent, bg=self.colors['light'], relief='flat', bd=0)
        category_frame.grid(row=0, column=column, padx=15, pady=15, sticky='nsew')
        
        # Category header
        header_frame = tk.Frame(category_frame, bg=self.colors['primary'], relief='flat', bd=0)
        header_frame.pack(fill='x')
        
        header_content = tk.Frame(header_frame, bg=self.colors['primary'])
        header_content.pack(fill='x', padx=20, pady=15)
        
        tk.Label(header_content, text=title, 
                font=self.fonts['subheading'], 
                bg=self.colors['primary'], 
                fg=self.colors['text_light']).pack()
        
        # Options container
        options_frame = tk.Frame(category_frame, bg=self.colors['card_bg'], relief='flat', bd=0)
        options_frame.pack(fill='both', expand=True)
        
        options_content = tk.Frame(options_frame, bg=self.colors['card_bg'])
        options_content.pack(fill='x', padx=20, pady=20)
        
        # Create option buttons
        for option in options:
            btn = self.create_perfect_button(
                options_content, option['text'], 
                option['command'], option['color']
            )
            btn.configure(font=self.fonts['body'], padx=20, pady=8)
            btn.pack(fill='x', pady=5)
    
    def get_date_sort_options(self):
        """Get date sorting options"""
        return [
            {
                'text': '📅 Medical Records - Latest First',
                'command': lambda: self.quick_sort_by_criteria('records', 'visit_date', 'desc'),
                'color': self.colors['success']
            },
            {
                'text': '📅 Medical Records - Oldest First',
                'command': lambda: self.quick_sort_by_criteria('records', 'visit_date', 'asc'),
                'color': self.colors['info']
            },
            {
                'text': '📅 Appointments - Upcoming',
                'command': lambda: self.quick_sort_by_criteria('appointments', 'appointment_date', 'desc'),
                'color': self.colors['accent']
            },
            {
                'text': '📅 Appointments - Past',
                'command': lambda: self.quick_sort_by_criteria('appointments', 'appointment_date', 'asc'),
                'color': self.colors['warning']
            },
            {
                'text': '📅 Patients - Youngest',
                'command': lambda: self.quick_sort_by_criteria('patients', 'date_of_birth', 'desc'),
                'color': self.colors['primary']
            },
            {
                'text': '📅 Patients - Oldest',
                'command': lambda: self.quick_sort_by_criteria('patients', 'date_of_birth', 'asc'),
                'color': self.colors['secondary']
            }
        ]
    
    def get_name_sort_options(self):
        """Get name sorting options"""
        return [
            {
                'text': '👤 Patients - First Name A→Z',
                'command': lambda: self.quick_sort_by_criteria('patients', 'first_name', 'asc'),
                'color': self.colors['success']
            },
            {
                'text': '👤 Patients - First Name Z→A',
                'command': lambda: self.quick_sort_by_criteria('patients', 'first_name', 'desc'),
                'color': self.colors['info']
            },
            {
                'text': '👤 Patients - Last Name A→Z',
                'command': lambda: self.quick_sort_by_criteria('patients', 'last_name', 'asc'),
                'color': self.colors['accent']
            },
            {
                'text': '👤 Patients - Last Name Z→A',
                'command': lambda: self.quick_sort_by_criteria('patients', 'last_name', 'desc'),
                'color': self.colors['warning']
            },
            {
                'text': '🏥 Records - Diagnosis A→Z',
                'command': lambda: self.quick_sort_by_criteria('records', 'diagnosis', 'asc'),
                'color': self.colors['primary']
            },
            {
                'text': '🩺 Records - Specialization A→Z',
                'command': lambda: self.quick_sort_by_criteria('records', 'specialization', 'asc'),
                'color': self.colors['secondary']
            }
        ]
    
    def get_id_sort_options(self):
        """Get ID sorting options"""
        return [
            {
                'text': '🔢 Patients - ID Ascending',
                'command': lambda: self.quick_sort_by_criteria('patients', 'patient_id', 'asc'),
                'color': self.colors['success']
            },
            {
                'text': '🔢 Patients - ID Descending',
                'command': lambda: self.quick_sort_by_criteria('patients', 'patient_id', 'desc'),
                'color': self.colors['info']
            },
            {
                'text': '📋 Records - ID Ascending',
                'command': lambda: self.quick_sort_by_criteria('records', 'record_id', 'asc'),
                'color': self.colors['accent']
            },
            {
                'text': '📋 Records - ID Descending',
                'command': lambda: self.quick_sort_by_criteria('records', 'record_id', 'desc'),
                'color': self.colors['warning']
            },
            {
                'text': '📅 Appointments - ID Ascending',
                'command': lambda: self.quick_sort_by_criteria('appointments', 'appointment_id', 'asc'),
                'color': self.colors['primary']
            },
            {
                'text': '📅 Appointments - ID Descending',
                'command': lambda: self.quick_sort_by_criteria('appointments', 'appointment_id', 'desc'),
                'color': self.colors['secondary']
            }
        ]

    def api_request(self, endpoint, method='GET', data=None):
        """Make API request"""
        try:
            url = f"{self.api_base}/{endpoint}"
            
            if method == 'GET':
                response = requests.get(url, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, timeout=10)
            elif method == 'PUT':
                response = requests.put(url, json=data, timeout=10)
            else:
                raise Exception(f"Unsupported method: {method}")
            
            if response.status_code == 200:
                return response.json()
            else:
                error_data = response.json() if response.content else {'message': 'Unknown error'}
                raise Exception(error_data.get('message', 'API request failed'))
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error: {e}")
        except Exception as e:
            raise Exception(str(e))
    
    def create_perfect_widgets(self):
        """Create perfect professional GUI with advanced styling"""
        # Perfect gradient title bar
        title_frame = tk.Frame(self.root, height=120, bg=self.colors['primary'])
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        # Simplified perfect background (removing gradient for now)
        # gradient_canvas = self.create_gradient_frame(title_frame, 1600, 120, 
        #                                            self.colors['gradient_start'], 
        #                                            self.colors['gradient_end'])
        # gradient_canvas.pack(fill='both', expand=True)
        
        # Perfect title overlay
        title_overlay = tk.Frame(title_frame, bg=self.colors['primary'])
        title_overlay.place(relx=0.5, rely=0.5, anchor='center')
        
        # Main title with perfect typography
        main_title = tk.Label(title_overlay, 
                             text="🏥 MedFlow Pro", 
                             font=self.fonts['title'], 
                             fg=self.colors['text_light'], 
                             bg=self.colors['primary'])
        main_title.pack()
        
        # Subtitle with perfect spacing
        subtitle = tk.Label(title_overlay, 
                           text="Advanced Hospital Management System • Real-time Analytics • Professional Healthcare", 
                           font=self.fonts['subtitle'], 
                           fg='#e0e7ff', 
                           bg=self.colors['primary'])
        subtitle.pack(pady=(5, 0))
        
        # Perfect main container
        main_container = tk.Frame(self.root, bg=self.colors['light'])
        main_container.pack(fill='both', expand=True)
        
        # Perfect navigation bar
        nav_frame = tk.Frame(main_container, bg=self.colors['dark'], height=60)
        nav_frame.pack(fill='x')
        nav_frame.pack_propagate(False)
        
        # Perfect notebook with custom styling
        notebook_container = tk.Frame(main_container, bg=self.colors['light'])
        notebook_container.pack(fill='both', expand=True, padx=0, pady=0)
        
        self.notebook = ttk.Notebook(notebook_container, style='Perfect.TNotebook')
        self.notebook.pack(fill='both', expand=True)
        
        # Create perfect tabs
        self.create_perfect_dashboard_tab()
        self.create_perfect_patients_tab()
        # Simplified tabs for now
        self.create_appointments_tab()
        self.create_medical_records_tab()
        self.create_data_sorting_tab()
        
        # Perfect status bar with indicators
        status_frame = tk.Frame(self.root, bg=self.colors['primary'], height=40)
        status_frame.pack(side='bottom', fill='x')
        status_frame.pack_propagate(False)
        
        # Status content
        status_content = tk.Frame(status_frame, bg=self.colors['primary'])
        status_content.pack(fill='both', expand=True, padx=20, pady=8)
        
        # Connection indicator
        connection_frame = tk.Frame(status_content, bg=self.colors['primary'])
        connection_frame.pack(side='left')
        
        self.status_var = tk.StringVar()
        self.status_var.set("🟢 System Online")
        
        status_indicator = tk.Label(connection_frame, 
                                   textvariable=self.status_var,
                                   font=self.fonts['subheading'],
                                   fg=self.colors['text_light'], 
                                   bg=self.colors['primary'])
        status_indicator.pack(side='left')
        
        # System info
        system_info = tk.Label(status_content, 
                              text="Flask API Connected • Database Active • Real-time Sync",
                              font=self.fonts['small'],
                              fg='#bfdbfe', 
                              bg=self.colors['primary'])
        system_info.pack(side='right')
    
    def create_perfect_dashboard_tab(self):
        """Create perfect dashboard with advanced analytics"""
        dashboard_frame = tk.Frame(self.notebook, bg=self.colors['light'])
        self.notebook.add(dashboard_frame, text="📊 Analytics Dashboard")
        
        # Perfect scrollable container
        canvas = tk.Canvas(dashboard_frame, bg=self.colors['light'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(dashboard_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['light'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Perfect header section
        header_section = tk.Frame(scrollable_frame, bg=self.colors['card_bg'], relief='flat', bd=0)
        header_section.pack(fill='x', padx=25, pady=25)
        
        # Perfect header with gradient accent
        header_content = tk.Frame(header_section, bg=self.colors['card_bg'])
        header_content.pack(fill='x', padx=40, pady=30)
        
        # Main dashboard title
        title_frame = tk.Frame(header_content, bg=self.colors['card_bg'])
        title_frame.pack(fill='x')
        
        tk.Label(title_frame, text="📊 Real-Time Analytics Dashboard", 
                font=self.fonts['heading'], 
                bg=self.colors['card_bg'], 
                fg=self.colors['text_primary']).pack(anchor='w')
        
        tk.Label(title_frame, text="Comprehensive hospital metrics • Live data visualization • Performance insights", 
                font=self.fonts['body'], 
                bg=self.colors['card_bg'], 
                fg=self.colors['text_secondary']).pack(anchor='w', pady=(8,0))
        
        # Perfect metrics grid
        metrics_container = tk.Frame(scrollable_frame, bg=self.colors['light'])
        metrics_container.pack(fill='x', padx=25, pady=(0,25))
        
        # Perfect metric cards with advanced design
        cards_grid = tk.Frame(metrics_container, bg=self.colors['light'])
        cards_grid.pack(fill='x', padx=20, pady=20)
        
        # Configure grid weights for perfect responsive layout
        for i in range(4):
            cards_grid.grid_columnconfigure(i, weight=1)
        
        # Create stats_frame for compatibility
        stats_frame = cards_grid
        
        # Perfect Patient Card with hover effects
        patient_card = self.create_perfect_metric_card(
            cards_grid, "👥", "Total Patients", "0", 
            self.colors['info'], 0, 0
        )
        self.patient_count_label = patient_card['metric_label']
        
        # Perfect Doctor Card
        doctor_card = self.create_perfect_metric_card(
            cards_grid, "👨‍⚕️", "Active Doctors", "0", 
            self.colors['success'], 0, 1
        )
        self.doctor_count_label = doctor_card['metric_label']
        
        # Perfect Appointment Card
        apt_card = self.create_perfect_metric_card(
            cards_grid, "📅", "Today's Appointments", "0", 
            self.colors['accent'], 0, 2
        )
        self.apt_count_label = apt_card['metric_label']
        
        # Perfect Room Card
        room_card = self.create_perfect_metric_card(
            cards_grid, "🏨", "Available Rooms", "0", 
            self.colors['warning'], 0, 3
        )
        self.room_count_label = room_card['metric_label']
        
        # Configure grid weights
        for i in range(4):
            stats_frame.grid_columnconfigure(i, weight=1)
        
        # Perfect action buttons
        actions_frame = tk.Frame(scrollable_frame, bg=self.colors['card_bg'], relief='flat', bd=0)
        actions_frame.pack(fill='x', padx=25, pady=(0,25))
        
        actions_content = tk.Frame(actions_frame, bg=self.colors['card_bg'])
        actions_content.pack(fill='x', padx=40, pady=25)
        
        # Button container
        button_container = tk.Frame(actions_content, bg=self.colors['card_bg'])
        button_container.pack()
        
        # Perfect refresh button with icon
        refresh_btn = self.create_perfect_button(
            button_container, "🔄 Refresh Analytics", 
            self.refresh_dashboard, self.colors['primary']
        )
        refresh_btn.pack(side='left', padx=10)
        
        # Perfect export button
        export_btn = self.create_perfect_button(
            button_container, "📊 Export Report", 
            lambda: messagebox.showinfo("Export", "Report export feature coming soon!"), 
            self.colors['success']
        )
        export_btn.pack(side='left', padx=10)
        
        # Perfect settings button
        settings_btn = self.create_perfect_button(
            button_container, "⚙️ Settings", 
            lambda: messagebox.showinfo("Settings", "Dashboard settings coming soon!"), 
            self.colors['warning']
        )
        settings_btn.pack(side='left', padx=10)
        
        # Perfect info panel
        info_panel = tk.Frame(actions_content, bg='#f0f9ff', relief='flat', bd=0)
        info_panel.pack(fill='x', pady=(20,0))
        
        info_content = tk.Frame(info_panel, bg='#f0f9ff')
        info_content.pack(fill='x', padx=20, pady=15)
        
        tk.Label(info_content, text="💡 Real-time Updates", 
                font=self.fonts['subheading'], 
                bg='#f0f9ff', fg=self.colors['primary']).pack(anchor='w')
        
        tk.Label(info_content, text="Dashboard automatically refreshes when you add patients, book appointments, or update records", 
                font=self.fonts['body'], 
                bg='#f0f9ff', fg=self.colors['text_secondary']).pack(anchor='w', pady=(5,0))
        
        # Perfect appointments section
        apt_section = tk.Frame(scrollable_frame, bg=self.colors['card_bg'], relief='flat', bd=0)
        apt_section.pack(fill='both', expand=True, padx=25, pady=(0,25))
        
        # Perfect section header
        apt_header = tk.Frame(apt_section, bg=self.colors['card_bg'])
        apt_header.pack(fill='x', padx=40, pady=25)
        
        tk.Label(apt_header, text="📅 Today's Appointments Overview", 
                font=self.fonts['heading'], 
                bg=self.colors['card_bg'], 
                fg=self.colors['text_primary']).pack(anchor='w')
        
        tk.Label(apt_header, text="Real-time appointment tracking • Patient management • Schedule optimization", 
                font=self.fonts['body'], 
                bg=self.colors['card_bg'], 
                fg=self.colors['text_secondary']).pack(anchor='w', pady=(8,0))
        
        # Perfect appointments table container
        table_container = tk.Frame(apt_section, bg=self.colors['card_bg'])
        table_container.pack(fill='both', expand=True, padx=40, pady=(0,25))
        
        # Perfect treeview with enhanced styling
        tree_frame = tk.Frame(table_container, bg=self.colors['card_bg'])
        tree_frame.pack(fill='both', expand=True)
        
        self.apt_tree = ttk.Treeview(tree_frame, 
                                    columns=('Time', 'Patient', 'Doctor', 'Status', 'Reason'), 
                                    show='headings', 
                                    height=15,
                                    style='Perfect.Treeview')
        
        # Perfect column configuration
        columns_config = {
            'Time': {'width': 100, 'text': '🕐 Time'},
            'Patient': {'width': 200, 'text': '👤 Patient'},
            'Doctor': {'width': 200, 'text': '👨‍⚕️ Doctor'},
            'Status': {'width': 120, 'text': '📊 Status'},
            'Reason': {'width': 250, 'text': '📝 Reason'}
        }
        
        for col, config in columns_config.items():
            self.apt_tree.heading(col, text=config['text'])
            self.apt_tree.column(col, width=config['width'], minwidth=80)
        
        # Perfect scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.apt_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.apt_tree.xview)
        
        self.apt_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack with perfect layout
        self.apt_tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Pack scrollable canvas
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Load initial data
        self.refresh_dashboard()
    
    def create_perfect_patients_tab(self):
        """Create perfect patients management with advanced features"""
        patients_frame = tk.Frame(self.notebook, bg=self.colors['light'])
        self.notebook.add(patients_frame, text="👥 Patient Management")
        
        # Perfect patient notebook with custom styling
        patient_notebook = ttk.Notebook(patients_frame, style='Perfect.TNotebook')
        patient_notebook.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Perfect add patient tab
        add_frame = tk.Frame(patient_notebook, bg=self.colors['light'])
        patient_notebook.add(add_frame, text="➕ Register Patient")
        
        # Perfect scrollable form
        canvas = tk.Canvas(add_frame, bg=self.colors['light'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(add_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['light'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Perfect form container
        form_frame = tk.Frame(scrollable_frame, bg=self.colors['card_bg'], relief='flat', bd=0)
        form_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Perfect form header
        header_frame = tk.Frame(form_frame, bg=self.colors['card_bg'])
        header_frame.pack(fill='x', padx=40, pady=30)
        
        tk.Label(header_frame, text="👥 Patient Registration", 
                font=self.fonts['heading'], 
                bg=self.colors['card_bg'], 
                fg=self.colors['text_primary']).pack(anchor='w')
        
        tk.Label(header_frame, text="Complete patient information • Medical history • Contact details", 
                font=self.fonts['body'], 
                bg=self.colors['card_bg'], 
                fg=self.colors['text_secondary']).pack(anchor='w', pady=(8,0))
        
        # Perfect form fields with advanced styling
        fields_container = tk.Frame(form_frame, bg=self.colors['card_bg'])
        fields_container.pack(fill='x', padx=40, pady=20)
        
        # Create perfect form grid
        fields_frame = tk.Frame(fields_container, bg=self.colors['card_bg'])
        fields_frame.pack(fill='x')
        
        # Configure grid weights
        fields_frame.grid_columnconfigure(1, weight=1)
        fields_frame.grid_columnconfigure(3, weight=1)
        
        # Perfect form fields with enhanced styling
        row = 0
        
        # First Name
        self.create_perfect_form_field(fields_frame, "First Name*", row, 0)
        self.first_name_entry = self.create_perfect_entry(fields_frame, row, 1)
        
        # Last Name
        self.create_perfect_form_field(fields_frame, "Last Name*", row, 2)
        self.last_name_entry = self.create_perfect_entry(fields_frame, row, 3)
        
        row += 1
        
        # Date of Birth
        self.create_perfect_form_field(fields_frame, "Date of Birth*", row, 0)
        self.dob_entry = DateEntry(fields_frame, width=25, 
                                  background=self.colors['card_bg'],
                                  foreground=self.colors['text_primary'], 
                                  borderwidth=2,
                                  relief='solid',
                                  maxdate=date.today(),
                                  font=self.fonts['body'],
                                  date_pattern='dd/mm/yyyy')
        self.dob_entry.grid(row=row, column=1, padx=15, pady=15, sticky='ew')
        
        # Gender
        self.create_perfect_form_field(fields_frame, "Gender*", row, 2)
        self.gender_combo = ttk.Combobox(fields_frame, 
                                        values=["Male", "Female", "Other"], 
                                        width=25, 
                                        font=self.fonts['body'],
                                        style='Perfect.TCombobox')
        self.gender_combo.grid(row=row, column=3, padx=15, pady=15, sticky='ew')
        
        row += 1
        
        # Phone
        self.create_perfect_form_field(fields_frame, "Phone Number", row, 0)
        self.phone_entry = self.create_perfect_entry(fields_frame, row, 1)
        
        # Email
        self.create_perfect_form_field(fields_frame, "Email Address", row, 2)
        self.email_entry = self.create_perfect_entry(fields_frame, row, 3)
        
        row += 1
        
        # Blood Type
        self.create_perfect_form_field(fields_frame, "Blood Type", row, 0)
        self.blood_combo = ttk.Combobox(fields_frame, 
                                       values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"], 
                                       width=25, 
                                       font=self.fonts['body'],
                                       style='Perfect.TCombobox')
        self.blood_combo.grid(row=row, column=1, padx=15, pady=15, sticky='ew')
        

        
        # Perfect action buttons
        button_section = tk.Frame(form_frame, bg=self.colors['card_bg'])
        button_section.pack(fill='x', padx=40, pady=30)
        
        # Button container with perfect spacing
        btn_container = tk.Frame(button_section, bg=self.colors['card_bg'])
        btn_container.pack()
        
        # Perfect register button
        register_btn = self.create_perfect_button(
            btn_container, "🚀 Register Patient", 
            self.register_patient, self.colors['success']
        )
        register_btn.configure(padx=40, pady=15, font=self.fonts['button'])
        register_btn.pack(side='left', padx=15)
        
        # Perfect clear button
        clear_btn = self.create_perfect_button(
            btn_container, "🔄 Clear Form", 
            self.clear_patient_form, self.colors['warning']
        )
        clear_btn.configure(padx=40, pady=15, font=self.fonts['button'])
        clear_btn.pack(side='left', padx=15)
        
        # Perfect preview button
        preview_btn = self.create_perfect_button(
            btn_container, "👁️ Preview", 
            lambda: messagebox.showinfo("Preview", "Form preview feature coming soon!"), 
            self.colors['info']
        )
        preview_btn.configure(padx=40, pady=15, font=self.fonts['button'])
        preview_btn.pack(side='left', padx=15)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Create search patients tab (simplified for now)
        # self.create_perfect_search_tab(patient_notebook)
    
    def create_perfect_search_tab(self, parent):
        """Create perfect search patients tab"""
        search_frame = tk.Frame(parent, bg=self.colors['light'])
        parent.add(search_frame, text="🔍 Search Patients")
        
        # Perfect search interface
        search_container = tk.Frame(search_frame, bg=self.colors['card_bg'], relief='flat', bd=0)
        search_container.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Search header
        header = tk.Frame(search_container, bg=self.colors['card_bg'])
        header.pack(fill='x', padx=40, pady=30)
        
        tk.Label(header, text="🔍 Patient Search & Management", 
                font=self.fonts['heading'], 
                bg=self.colors['card_bg'], 
                fg=self.colors['text_primary']).pack(anchor='w')
        
        tk.Label(header, text="Advanced search • Patient records • Quick access", 
                font=self.fonts['body'], 
                bg=self.colors['card_bg'], 
                fg=self.colors['text_secondary']).pack(anchor='w', pady=(8,0))
        
        # Search controls
        search_controls = tk.Frame(search_container, bg=self.colors['card_bg'])
        search_controls.pack(fill='x', padx=40, pady=20)
        
        tk.Label(search_controls, text="Search:", 
                font=self.fonts['subheading'], 
                bg=self.colors['card_bg'],
                fg=self.colors['text_primary']).pack(side='left', padx=(0,15))
        
        self.search_entry = self.create_perfect_entry_inline(search_controls, width=40)
        self.search_entry.pack(side='left', padx=10)
        self.search_entry.bind('<Return>', lambda e: self.search_patients())
        
        # Perfect search buttons
        search_btn = self.create_perfect_button(
            search_controls, "🔍 Search", 
            self.search_patients, self.colors['primary']
        )
        search_btn.pack(side='left', padx=10)
        
        load_all_btn = self.create_perfect_button(
            search_controls, "📋 Load All", 
            self.load_all_patients, self.colors['info']
        )
        load_all_btn.pack(side='left', padx=10)
        
        # Results table
        results_frame = tk.Frame(search_container, bg=self.colors['card_bg'])
        results_frame.pack(fill='both', expand=True, padx=40, pady=(0,30))
        
        self.patients_tree = ttk.Treeview(results_frame, 
                                         columns=('ID', 'Name', 'Phone', 'Email', 'DOB', 'Gender'), 
                                         show='headings', 
                                         height=20,
                                         style='Perfect.Treeview')
        
        # Configure columns
        columns_config = {
            'ID': {'width': 80, 'text': '🆔 ID'},
            'Name': {'width': 200, 'text': '👤 Full Name'},
            'Phone': {'width': 150, 'text': '📞 Phone'},
            'Email': {'width': 200, 'text': '📧 Email'},
            'DOB': {'width': 120, 'text': '📅 Birth Date'},
            'Gender': {'width': 100, 'text': '⚧ Gender'}
        }
        
        for col, config in columns_config.items():
            self.patients_tree.heading(col, text=config['text'])
            self.patients_tree.column(col, width=config['width'], minwidth=80)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(results_frame, orient='vertical', command=self.patients_tree.yview)
        h_scrollbar = ttk.Scrollbar(results_frame, orient='horizontal', command=self.patients_tree.xview)
        
        self.patients_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.patients_tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
    
    def create_perfect_entry_inline(self, parent, width=25):
        """Create a perfect inline entry widget"""
        entry = tk.Entry(parent, width=width, 
                        font=self.fonts['body'],
                        relief='solid', 
                        bd=2,
                        highlightthickness=0,
                        bg=self.colors['card_bg'],
                        fg=self.colors['text_primary'])
        return entry
    
    def create_perfect_appointments_tab(self):
        """Create perfect appointments tab (simplified)"""
        apt_frame = tk.Frame(self.notebook, bg=self.colors['light'])
        self.notebook.add(apt_frame, text="📅 Appointments")
        
        # Placeholder content
        placeholder = tk.Label(apt_frame, 
                              text="📅 Perfect Appointments Interface\nComing Soon with Enhanced Features!", 
                              font=self.fonts['heading'],
                              bg=self.colors['light'],
                              fg=self.colors['text_primary'])
        placeholder.pack(expand=True)
    
    def create_perfect_medical_records_tab(self):
        """Create perfect medical records tab (simplified)"""
        records_frame = tk.Frame(self.notebook, bg=self.colors['light'])
        self.notebook.add(records_frame, text="📋 Medical Records")
        
        # Placeholder content
        placeholder = tk.Label(records_frame, 
                              text="📋 Perfect Medical Records Interface\nAdvanced Patient History & Analytics!", 
                              font=self.fonts['heading'],
                              bg=self.colors['light'],
                              fg=self.colors['text_primary'])
        placeholder.pack(expand=True)
    
    def create_perfect_data_sorting_tab(self):
        """Create perfect data sorting tab (simplified)"""
        sorting_frame = tk.Frame(self.notebook, bg=self.colors['light'])
        self.notebook.add(sorting_frame, text="🔄 Analytics")
        
        # Placeholder content
        placeholder = tk.Label(sorting_frame, 
                              text="🔄 Perfect Data Analytics Interface\nAdvanced Sorting & Visualization Tools!", 
                              font=self.fonts['heading'],
                              bg=self.colors['light'],
                              fg=self.colors['text_primary'])
        placeholder.pack(expand=True)
        
        # Search patients tab
        search_frame = ttk.Frame(patient_notebook)
        patient_notebook.add(search_frame, text="🔍 Search Patients")
        
        # Search section
        search_section = tk.Frame(search_frame, bg='white', relief='raised', bd=2)
        search_section.pack(fill='x', padx=10, pady=10)
        
        tk.Label(search_section, text="🔍 Search Patients", 
                font=('Arial', 14, 'bold'), bg='white', fg='#2c3e50').pack(pady=10)
        
        search_controls = tk.Frame(search_section, bg='white')
        search_controls.pack(pady=10)
        
        tk.Label(search_controls, text="Search:", font=('Arial', 11, 'bold'), 
                bg='white').pack(side='left', padx=5)
        self.search_entry = tk.Entry(search_controls, width=30, font=('Arial', 11))
        self.search_entry.pack(side='left', padx=5)
        self.search_entry.bind('<Return>', lambda e: self.search_patients())
        
        search_btn = tk.Button(search_controls, text="🔍 Search", 
                             command=self.search_patients, bg='#2ecc71', fg='white',
                             font=('Arial', 11, 'bold'), padx=15)
        search_btn.pack(side='left', padx=5)
        
        load_all_btn = tk.Button(search_controls, text="📋 Load All", 
                               command=self.load_all_patients, bg='#f39c12', fg='white',
                               font=('Arial', 11, 'bold'), padx=15)
        load_all_btn.pack(side='left', padx=5)
        
        refresh_btn = tk.Button(search_controls, text="🔄 Refresh", 
                              command=self.refresh_patient_search, bg='#3498db', fg='white',
                              font=('Arial', 11, 'bold'), padx=15)
        refresh_btn.pack(side='left', padx=5)
        
        # Results
        results_frame = tk.Frame(search_frame, bg='white', relief='raised', bd=2)
        results_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(results_frame, text="Search Results", 
                font=('Arial', 12, 'bold'), bg='white', fg='#2c3e50').pack(pady=5)
        
        self.patients_tree = ttk.Treeview(results_frame, 
                                         columns=('ID', 'Name', 'Phone', 'Email', 'DOB', 'Gender'), 
                                         show='headings', height=15)
        
        self.patients_tree.heading('ID', text='ID')
        self.patients_tree.heading('Name', text='Full Name')
        self.patients_tree.heading('Phone', text='Phone')
        self.patients_tree.heading('Email', text='Email')
        self.patients_tree.heading('DOB', text='Date of Birth')
        self.patients_tree.heading('Gender', text='Gender')
        
        self.patients_tree.column('ID', width=50)
        self.patients_tree.column('Name', width=180)
        self.patients_tree.column('Phone', width=120)
        self.patients_tree.column('Email', width=180)
        self.patients_tree.column('DOB', width=100)
        self.patients_tree.column('Gender', width=80)
        
        # Scrollbar for patients
        patients_scrollbar = ttk.Scrollbar(results_frame, orient='vertical', command=self.patients_tree.yview)
        self.patients_tree.configure(yscrollcommand=patients_scrollbar.set)
        
        self.patients_tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        patients_scrollbar.pack(side='right', fill='y', pady=10)
    
    def create_appointments_tab(self):
        """Create enhanced appointments tab"""
        apt_frame = tk.Frame(self.notebook, bg=self.colors['light'])
        self.notebook.add(apt_frame, text="📅 Appointments")
        
        # Enhanced book appointment section
        book_section = tk.Frame(apt_frame, bg=self.colors['card_bg'], relief='flat', bd=0)
        book_section.pack(fill='x', padx=20, pady=20)
        
        # Modern header
        header_frame = tk.Frame(book_section, bg=self.colors['card_bg'])
        header_frame.pack(fill='x', padx=30, pady=20)
        
        tk.Label(header_frame, text="📝 Book New Appointment", 
                font=('Segoe UI', 20, 'bold'), 
                bg=self.colors['card_bg'], 
                fg=self.colors['text_primary']).pack(anchor='w')
        
        tk.Label(header_frame, text="Schedule appointments with available doctors", 
                font=('Segoe UI', 11), 
                bg=self.colors['card_bg'], 
                fg='#6c757d').pack(anchor='w', pady=(5,0))
        
        # Form
        apt_form = tk.Frame(book_section, bg='white')
        apt_form.pack(padx=30, pady=20)
        
        # Patient ID
        tk.Label(apt_form, text="Patient ID*:", font=('Arial', 11, 'bold'), 
                bg='white').grid(row=0, column=0, sticky='w', pady=8, padx=5)
        
        patient_id_frame = tk.Frame(apt_form, bg='white')
        patient_id_frame.grid(row=0, column=1, padx=15, pady=8, sticky='w')
        
        self.apt_patient_id = tk.Entry(patient_id_frame, width=20, font=('Arial', 11))
        self.apt_patient_id.pack(side='left')
        
        validate_patient_btn = tk.Button(patient_id_frame, text="✓ Validate", 
                                       command=self.validate_patient_id, bg='#f39c12', fg='white',
                                       font=('Arial', 9, 'bold'), padx=8)
        validate_patient_btn.pack(side='left', padx=5)
        
        # Doctor
        tk.Label(apt_form, text="Doctor*:", font=('Arial', 11, 'bold'), 
                bg='white').grid(row=1, column=0, sticky='w', pady=8, padx=5)
        self.apt_doctor_combo = ttk.Combobox(apt_form, width=27, state='readonly')
        self.apt_doctor_combo.grid(row=1, column=1, padx=15, pady=8)
        
        # Date
        tk.Label(apt_form, text="Date*:", font=('Arial', 11, 'bold'), 
                bg='white').grid(row=2, column=0, sticky='w', pady=8, padx=5)
        self.apt_date = DateEntry(apt_form, width=12, background='darkblue',
                                 foreground='white', borderwidth=2, mindate=date.today())
        self.apt_date.grid(row=2, column=1, padx=15, pady=8, sticky='w')
        
        # Time
        tk.Label(apt_form, text="Time*:", font=('Arial', 11, 'bold'), 
                bg='white').grid(row=3, column=0, sticky='w', pady=8, padx=5)
        time_frame = tk.Frame(apt_form, bg='white')
        time_frame.grid(row=3, column=1, padx=15, pady=8, sticky='w')
        
        self.apt_hour = ttk.Combobox(time_frame, values=[f"{i:02d}" for i in range(8, 18)], width=5)
        self.apt_hour.pack(side='left')
        tk.Label(time_frame, text=":", bg='white', font=('Arial', 11)).pack(side='left')
        self.apt_minute = ttk.Combobox(time_frame, values=["00", "15", "30", "45"], width=5)
        self.apt_minute.pack(side='left')
        
        # Reason
        tk.Label(apt_form, text="Reason:", font=('Arial', 11, 'bold'), 
                bg='white').grid(row=4, column=0, sticky='w', pady=8, padx=5)
        self.apt_reason = tk.Text(apt_form, width=30, height=3, font=('Arial', 11))
        self.apt_reason.grid(row=4, column=1, padx=15, pady=8)
        
        # Enhanced book button
        button_frame = tk.Frame(book_section, bg=self.colors['card_bg'])
        button_frame.pack(pady=25)
        
        book_btn = tk.Button(button_frame, text="✅ Book Appointment", 
                           command=self.book_appointment, 
                           bg=self.colors['success'], fg='white',
                           font=('Segoe UI', 14, 'bold'), 
                           padx=40, pady=15,
                           relief='flat', bd=0,
                           cursor='hand2')
        book_btn.pack()
        
        # Load doctors
        self.load_doctors()
    
    def create_medical_records_tab(self):
        """Create perfect medical records tab with enhanced functionality"""
        records_frame = tk.Frame(self.notebook, bg=self.colors['light'])
        self.notebook.add(records_frame, text="📋 Medical Records")
        
        # Perfect scrollable container
        canvas = tk.Canvas(records_frame, bg=self.colors['light'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(records_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['light'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Perfect header section
        header_section = tk.Frame(scrollable_frame, bg=self.colors['card_bg'], relief='flat', bd=0)
        header_section.pack(fill='x', padx=25, pady=25)
        
        header_content = tk.Frame(header_section, bg=self.colors['card_bg'])
        header_content.pack(fill='x', padx=40, pady=30)
        
        tk.Label(header_content, text="📋 Patient Medical Records", 
                font=self.fonts['heading'], 
                bg=self.colors['card_bg'], 
                fg=self.colors['text_primary']).pack(anchor='w')
        
        tk.Label(header_content, text="Comprehensive medical history • Treatment records • Patient health analytics", 
                font=self.fonts['body'], 
                bg=self.colors['card_bg'], 
                fg=self.colors['text_secondary']).pack(anchor='w', pady=(8,0))
        
        # Perfect search section
        search_section = tk.Frame(scrollable_frame, bg=self.colors['card_bg'], relief='flat', bd=0)
        search_section.pack(fill='x', padx=25, pady=(0,25))
        
        search_content = tk.Frame(search_section, bg=self.colors['card_bg'])
        search_content.pack(fill='x', padx=40, pady=25)
        
        # Search header
        search_header = tk.Frame(search_content, bg=self.colors['card_bg'])
        search_header.pack(fill='x', pady=(0,20))
        
        tk.Label(search_header, text="🔍 Patient Search", 
                font=self.fonts['subheading'], 
                bg=self.colors['card_bg'], 
                fg=self.colors['text_primary']).pack(anchor='w')
        
        # Search controls with perfect styling
        search_controls = tk.Frame(search_content, bg=self.colors['card_bg'])
        search_controls.pack(fill='x', pady=10)
        
        # Patient ID input
        id_frame = tk.Frame(search_controls, bg=self.colors['card_bg'])
        id_frame.pack(side='left', padx=(0,20))
        
        tk.Label(id_frame, text="Patient ID:", 
                font=self.fonts['subheading'], 
                bg=self.colors['card_bg'],
                fg=self.colors['text_primary']).pack(anchor='w')
        
        self.records_patient_id = tk.Entry(id_frame, width=15, 
                                          font=self.fonts['body'],
                                          relief='solid', bd=2,
                                          bg=self.colors['card_bg'],
                                          fg=self.colors['text_primary'])
        self.records_patient_id.pack(pady=(5,0))
        self.records_patient_id.bind('<Return>', lambda e: self.load_medical_records())
        
        # Action buttons
        buttons_frame = tk.Frame(search_controls, bg=self.colors['card_bg'])
        buttons_frame.pack(side='left', padx=20)
        
        # Validate Patient button
        validate_btn = self.create_perfect_button(
            buttons_frame, "✓ Validate Patient", 
            self.validate_patient_for_records, self.colors['info']
        )
        validate_btn.pack(pady=2)
        
        # Load Records button
        load_btn = self.create_perfect_button(
            buttons_frame, "📋 Load Records", 
            self.load_medical_records, self.colors['success']
        )
        load_btn.pack(pady=2)
        
        # Clear button
        clear_btn = self.create_perfect_button(
            buttons_frame, "🗑️ Clear", 
            self.clear_medical_records, self.colors['warning']
        )
        clear_btn.pack(pady=2)
        
        # Patient info display
        self.patient_info_frame = tk.Frame(search_content, bg='#f0f9ff', relief='flat', bd=0)
        self.patient_info_frame.pack(fill='x', pady=(20,0))
        
        self.patient_info_label = tk.Label(self.patient_info_frame, 
                                          text="💡 Enter a Patient ID and click 'Validate Patient' to verify", 
                                          font=self.fonts['body'], 
                                          bg='#f0f9ff', 
                                          fg=self.colors['primary'])
        self.patient_info_label.pack(pady=15)
        
        # Perfect results section
        results_section = tk.Frame(scrollable_frame, bg=self.colors['card_bg'], relief='flat', bd=0)
        results_section.pack(fill='both', expand=True, padx=25, pady=(0,25))
        
        results_content = tk.Frame(results_section, bg=self.colors['card_bg'])
        results_content.pack(fill='both', expand=True, padx=40, pady=30)
        
        # Results header
        results_header = tk.Frame(results_content, bg=self.colors['card_bg'])
        results_header.pack(fill='x', pady=(0,20))
        
        tk.Label(results_header, text="📊 Medical Records", 
                font=self.fonts['subheading'], 
                bg=self.colors['card_bg'], 
                fg=self.colors['text_primary']).pack(side='left')
        
        # Records count label
        self.records_count_label = tk.Label(results_header, 
                                           text="", 
                                           font=self.fonts['body'], 
                                           bg=self.colors['card_bg'], 
                                           fg=self.colors['text_secondary'])
        self.records_count_label.pack(side='right')
        
        # Perfect records table
        table_frame = tk.Frame(results_content, bg=self.colors['card_bg'])
        table_frame.pack(fill='both', expand=True)
        
        self.records_tree = ttk.Treeview(table_frame, 
                                        columns=('Date', 'Doctor', 'Specialization', 'Diagnosis', 'Treatment', 'Prescription'), 
                                        show='headings', 
                                        height=18,
                                        style='Perfect.Treeview')
        
        # Perfect column configuration
        columns_config = {
            'Date': {'width': 120, 'text': '📅 Visit Date'},
            'Doctor': {'width': 180, 'text': '👨‍⚕️ Doctor'},
            'Specialization': {'width': 150, 'text': '🏥 Specialization'},
            'Diagnosis': {'width': 250, 'text': '🔍 Diagnosis'},
            'Treatment': {'width': 250, 'text': '💊 Treatment'},
            'Prescription': {'width': 200, 'text': '📝 Prescription'}
        }
        
        for col, config in columns_config.items():
            self.records_tree.heading(col, text=config['text'])
            self.records_tree.column(col, width=config['width'], minwidth=100)
        
        # Perfect scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.records_tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient='horizontal', command=self.records_tree.xview)
        
        self.records_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Bind double-click to show detailed record
        self.records_tree.bind('<Double-1>', self.show_detailed_record)
        
        # Pack with perfect layout
        self.records_tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def refresh_dashboard(self):
        """Refresh dashboard data"""
        def refresh_thread():
            try:
                # Update status on main thread
                self.root.after(0, lambda: self.status_var.set("Refreshing dashboard..."))
                
                response = self.api_request('dashboard')
                
                if response['status'] == 'success':
                    data = response['data']
                    
                    # Update GUI elements on main thread
                    def update_gui():
                        # Update metrics
                        self.patient_count_label.config(text=str(data['patient_count']))
                        self.doctor_count_label.config(text=str(data['doctor_count']))
                        self.apt_count_label.config(text=str(data['appointment_count']))
                        self.room_count_label.config(text=str(data['available_rooms']))
                        
                        # Update appointments tree
                        self.apt_tree.delete(*self.apt_tree.get_children())
                        for apt in data['today_appointments']:
                            time_str = str(apt['appointment_time']) if apt['appointment_time'] else 'N/A'
                            self.apt_tree.insert('', 'end', values=(
                                time_str,
                                f"{apt['first_name']} {apt['last_name']}",
                                f"Dr. {apt['doctor_first_name']} {apt['doctor_last_name']}",
                                apt['status'],
                                apt.get('reason', 'N/A')[:50] + '...' if apt.get('reason', '') and len(apt.get('reason', '')) > 50 else apt.get('reason', 'N/A')
                            ))
                        
                        self.status_var.set("Dashboard refreshed successfully")
                    
                    self.root.after(0, update_gui)
                else:
                    raise Exception(response.get('message', 'Unknown error'))
                    
            except Exception as e:
                def show_error():
                    messagebox.showerror("Error", f"Failed to refresh dashboard: {e}")
                    self.status_var.set("Dashboard refresh failed")
                
                self.root.after(0, show_error)
        
        # Run in thread to prevent GUI freezing
        threading.Thread(target=refresh_thread, daemon=True).start()
    
    def register_patient(self):
        """Register new patient"""
        def register_thread():
            try:
                # Validate required fields (get values on main thread)
                first_name = self.first_name_entry.get()
                last_name = self.last_name_entry.get()
                gender = self.gender_combo.get()
                
                if not all([first_name, last_name, gender]):
                    self.root.after(0, lambda: messagebox.showerror("Error", "Please fill in all required fields (*)"))
                    return
                
                self.root.after(0, lambda: self.status_var.set("Registering patient..."))
                
                # Prepare patient data
                patient_data = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'date_of_birth': self.dob_entry.get_date().isoformat(),
                    'gender': gender,
                    'phone': self.phone_entry.get() or None,
                    'email': self.email_entry.get() or None,
                    'blood_type': self.blood_combo.get() or None
                }
                
                # Register patient
                response = self.api_request('patients', method='POST', data=patient_data)
                
                if response['status'] == 'success':
                    def success_callback():
                        messagebox.showinfo("Success", f"✅ Patient registered successfully!\nPatient ID: {response['patient_id']}")
                        self.clear_patient_form()
                        self.refresh_dashboard()
                        self.status_var.set("Patient registered successfully")
                    
                    self.root.after(0, success_callback)
                else:
                    raise Exception(response.get('message', 'Registration failed'))
                    
            except Exception as e:
                def error_callback():
                    messagebox.showerror("Error", f"Registration failed: {e}")
                    self.status_var.set("Patient registration failed")
                
                self.root.after(0, error_callback)
        
        threading.Thread(target=register_thread, daemon=True).start()
    
    def clear_patient_form(self):
        """Clear patient form"""
        self.first_name_entry.delete(0, 'end')
        self.last_name_entry.delete(0, 'end')
        self.phone_entry.delete(0, 'end')
        self.email_entry.delete(0, 'end')
        self.gender_combo.set('')
        self.blood_combo.set('')
        self.dob_entry.set_date(date.today())
    
    def search_patients(self):
        """Search patients"""
        def search_thread():
            try:
                search_term = self.search_entry.get()
                if not search_term:
                    self.root.after(0, lambda: messagebox.showwarning("Warning", "Please enter a search term"))
                    return
                
                self.root.after(0, lambda: self.status_var.set("Searching patients..."))
                
                response = self.api_request('patients/search', method='POST', data={'search_term': search_term})
                
                if response['status'] == 'success':
                    def update_results():
                        self.patients_tree.delete(*self.patients_tree.get_children())
                        
                        for patient in response['data']:
                            self.patients_tree.insert('', 'end', values=(
                                patient['patient_id'],
                                f"{patient['first_name']} {patient['last_name']}",
                                patient['phone'] or 'N/A',
                                patient['email'] or 'N/A',
                                patient['date_of_birth'],
                                patient.get('gender', 'N/A')
                            ))
                        
                        self.status_var.set(f"Found {len(response['data'])} patients")
                    
                    self.root.after(0, update_results)
                else:
                    raise Exception(response.get('message', 'Search failed'))
                    
            except Exception as e:
                def error_callback():
                    messagebox.showerror("Error", f"Search failed: {e}")
                    self.status_var.set("Patient search failed")
                
                self.root.after(0, error_callback)
        
        threading.Thread(target=search_thread, daemon=True).start()
    
    def load_all_patients(self):
        """Load all patients"""
        def load_thread():
            try:
                self.root.after(0, lambda: self.status_var.set("Loading all patients..."))
                
                response = self.api_request('patients')
                
                if response['status'] == 'success':
                    def update_patients():
                        self.patients_tree.delete(*self.patients_tree.get_children())
                        
                        for patient in response['data']:
                            self.patients_tree.insert('', 'end', values=(
                                patient['patient_id'],
                                f"{patient['first_name']} {patient['last_name']}",
                                patient['phone'] or 'N/A',
                                patient['email'] or 'N/A',
                                patient['date_of_birth'],
                                patient.get('gender', 'N/A')
                            ))
                        
                        self.status_var.set(f"Loaded {len(response['data'])} patients")
                    
                    self.root.after(0, update_patients)
                else:
                    raise Exception(response.get('message', 'Failed to load patients'))
                    
            except Exception as e:
                def error_callback():
                    messagebox.showerror("Error", f"Failed to load patients: {e}")
                    self.status_var.set("Failed to load patients")
                
                self.root.after(0, error_callback)
        
        threading.Thread(target=load_thread, daemon=True).start()
    
    def refresh_patient_search(self):
        """Refresh patient search results"""
        def refresh_thread():
            try:
                self.root.after(0, lambda: self.status_var.set("Refreshing patient data..."))
                
                # Clear current search
                search_term = self.search_entry.get()
                
                if search_term:
                    # Re-run the current search
                    response = self.api_request('patients/search', method='POST', data={'search_term': search_term})
                    
                    if response['status'] == 'success':
                        def update_search_results():
                            self.patients_tree.delete(*self.patients_tree.get_children())
                            
                            for patient in response['data']:
                                self.patients_tree.insert('', 'end', values=(
                                    patient['patient_id'],
                                    f"{patient['first_name']} {patient['last_name']}",
                                    patient['phone'] or 'N/A',
                                    patient['email'] or 'N/A',
                                    patient['date_of_birth'],
                                    patient.get('gender', 'N/A')
                                ))
                            
                            self.status_var.set(f"Refreshed: Found {len(response['data'])} patients")
                        
                        self.root.after(0, update_search_results)
                    else:
                        raise Exception(response.get('message', 'Refresh failed'))
                else:
                    # Load all patients if no search term
                    response = self.api_request('patients')
                    
                    if response['status'] == 'success':
                        def update_all_results():
                            self.patients_tree.delete(*self.patients_tree.get_children())
                            
                            for patient in response['data']:
                                self.patients_tree.insert('', 'end', values=(
                                    patient['patient_id'],
                                    f"{patient['first_name']} {patient['last_name']}",
                                    patient['phone'] or 'N/A',
                                    patient['email'] or 'N/A',
                                    patient['date_of_birth'],
                                    patient.get('gender', 'N/A')
                                ))
                            
                            self.status_var.set(f"Refreshed: Loaded {len(response['data'])} patients")
                        
                        self.root.after(0, update_all_results)
                    else:
                        raise Exception(response.get('message', 'Refresh failed'))
                        
            except Exception as e:
                def error_callback():
                    messagebox.showerror("Error", f"Refresh failed: {e}")
                    self.status_var.set("Patient refresh failed")
                
                self.root.after(0, error_callback)
        
        threading.Thread(target=refresh_thread, daemon=True).start()
    
    def load_doctors(self):
        """Load doctors for appointment booking"""
        def load_thread():
            try:
                response = self.api_request('doctors')
                
                if response['status'] == 'success':
                    doctor_options = [f"Dr. {doctor['first_name']} {doctor['last_name']} ({doctor['specialization']}) - ID: {doctor['doctor_id']}" 
                                    for doctor in response['data']]
                    self.apt_doctor_combo['values'] = doctor_options
                    
            except Exception as e:
                print(f"Failed to load doctors: {e}")
        
        threading.Thread(target=load_thread, daemon=True).start()
    
    def book_appointment(self):
        """Book appointment"""
        def book_thread():
            try:
                # Get values on main thread
                patient_id = self.apt_patient_id.get()
                doctor_combo = self.apt_doctor_combo.get()
                hour = self.apt_hour.get()
                minute = self.apt_minute.get()
                
                # Validate required fields
                if not all([patient_id, doctor_combo, hour, minute]):
                    self.root.after(0, lambda: messagebox.showerror("Error", "Please fill in all required fields"))
                    return
                
                self.root.after(0, lambda: self.status_var.set("Booking appointment..."))
                
                # Extract doctor ID
                doctor_id = int(doctor_combo.split("ID: ")[1])
                
                # Prepare appointment data
                appointment_time = f"{hour}:{minute}:00"
                appointment_data = {
                    'patient_id': int(patient_id),
                    'doctor_id': doctor_id,
                    'appointment_date': self.apt_date.get_date().isoformat(),
                    'appointment_time': appointment_time,
                    'reason': self.apt_reason.get('1.0', 'end-1c')
                }
                
                # Book appointment
                response = self.api_request('appointments', method='POST', data=appointment_data)
                
                if response['status'] == 'success':
                    def success_callback():
                        messagebox.showinfo("Success", "✅ Appointment booked successfully!")
                        self.refresh_dashboard()
                        # Clear form
                        self.apt_patient_id.delete(0, 'end')
                        self.apt_doctor_combo.set('')
                        self.apt_hour.set('')
                        self.apt_minute.set('')
                        self.apt_reason.delete('1.0', 'end')
                        self.status_var.set("Appointment booked successfully")
                    
                    self.root.after(0, success_callback)
                else:
                    raise Exception(response.get('message', 'Booking failed'))
                    
            except ValueError:
                self.root.after(0, lambda: messagebox.showerror("Error", "Please enter a valid Patient ID"))
            except Exception as e:
                def error_callback():
                    messagebox.showerror("Error", f"Booking failed: {e}")
                    self.status_var.set("Appointment booking failed")
                
                self.root.after(0, error_callback)
        
        threading.Thread(target=book_thread, daemon=True).start()
    
    def validate_patient_for_records(self):
        """Validate patient ID before loading records"""
        def validate_thread():
            try:
                patient_id = self.records_patient_id.get().strip()
                if not patient_id:
                    self.root.after(0, lambda: messagebox.showwarning("Warning", "Please enter a Patient ID"))
                    return
                
                self.root.after(0, lambda: self.status_var.set(f"Validating Patient ID {patient_id}..."))
                
                # Validate patient exists
                response = self.api_request(f'validate/patient/{patient_id}')
                
                if response['status'] == 'success':
                    if response['exists']:
                        patient = response['patient']
                        def show_patient_info():
                            info_text = f"✅ Patient Found: {patient['first_name']} {patient['last_name']} (ID: {patient['patient_id']})"
                            self.patient_info_label.config(text=info_text, fg=self.colors['success'])
                            self.status_var.set("✅ Patient validated successfully")
                        
                        self.root.after(0, show_patient_info)
                    else:
                        def show_not_found():
                            self.patient_info_label.config(text=f"❌ Patient ID {patient_id} not found in database", 
                                                          fg=self.colors['accent'])
                            self.status_var.set("❌ Patient not found")
                        
                        self.root.after(0, show_not_found)
                else:
                    raise Exception(response.get('message', 'Validation failed'))
                    
            except ValueError:
                self.root.after(0, lambda: messagebox.showerror("Error", "Please enter a valid numeric Patient ID"))
            except Exception as e:
                def error_callback():
                    messagebox.showerror("Error", f"Validation failed: {e}")
                    self.status_var.set("❌ Validation failed")
                
                self.root.after(0, error_callback)
        
        threading.Thread(target=validate_thread, daemon=True).start()
    
    def load_medical_records(self):
        """Load medical records for a patient with enhanced display"""
        def load_thread():
            try:
                patient_id = self.records_patient_id.get().strip()
                if not patient_id:
                    self.root.after(0, lambda: messagebox.showwarning("Warning", "Please enter a Patient ID"))
                    return
                
                self.root.after(0, lambda: self.status_var.set(f"Loading medical records for Patient ID {patient_id}..."))
                
                # First validate patient
                validate_response = self.api_request(f'validate/patient/{patient_id}')
                
                if validate_response['status'] == 'success' and not validate_response['exists']:
                    def show_not_found():
                        messagebox.showerror("Patient Not Found", 
                                           f"❌ Patient ID {patient_id} does not exist in the database.\n\n"
                                           f"Please check the Patient ID and try again.")
                        self.patient_info_label.config(text=f"❌ Patient ID {patient_id} not found", 
                                                      fg=self.colors['accent'])
                        self.status_var.set("❌ Patient not found")
                    
                    self.root.after(0, show_not_found)
                    return
                
                # Load medical records
                response = self.api_request(f'patients/{patient_id}/medical-records')
                
                if response['status'] == 'success':
                    patient = validate_response['patient']
                    records = response['data']
                    
                    def update_records():
                        # Clear existing records
                        self.records_tree.delete(*self.records_tree.get_children())
                        
                        # Update patient info
                        info_text = f"📋 Records for: {patient['first_name']} {patient['last_name']} (ID: {patient['patient_id']})"
                        self.patient_info_label.config(text=info_text, fg=self.colors['success'])
                        
                        # Update records count
                        self.records_count_label.config(text=f"Total Records: {len(records)}")
                        
                        if records:
                            # Populate records
                            for record in records:
                                # Format date
                                visit_date = str(record.get('visit_date', 'N/A'))
                                if visit_date != 'N/A':
                                    try:
                                        from datetime import datetime
                                        date_obj = datetime.strptime(visit_date.split()[0], '%Y-%m-%d')
                                        visit_date = date_obj.strftime('%d/%m/%Y')
                                    except:
                                        pass
                                
                                # Truncate long text for display
                                diagnosis = record.get('diagnosis', 'N/A') or 'N/A'
                                treatment = record.get('treatment', 'N/A') or 'N/A'
                                prescription = record.get('prescription', 'N/A') or 'N/A'
                                
                                diagnosis_display = diagnosis[:40] + '...' if len(diagnosis) > 40 else diagnosis
                                treatment_display = treatment[:40] + '...' if len(treatment) > 40 else treatment
                                prescription_display = prescription[:30] + '...' if len(prescription) > 30 else prescription
                                
                                self.records_tree.insert('', 'end', values=(
                                    visit_date,
                                    f"Dr. {record['doctor_first_name']} {record['doctor_last_name']}",
                                    record['specialization'],
                                    diagnosis_display,
                                    treatment_display,
                                    prescription_display
                                ))
                            
                            self.status_var.set(f"✅ Loaded {len(records)} medical records for {patient['first_name']} {patient['last_name']}")
                            
                            # Show success message
                            messagebox.showinfo("Records Loaded", 
                                              f"✅ Successfully loaded {len(records)} medical records for:\n\n"
                                              f"Patient: {patient['first_name']} {patient['last_name']}\n"
                                              f"Patient ID: {patient['patient_id']}\n\n"
                                              f"Double-click any record for detailed view.")
                        else:
                            self.status_var.set(f"No medical records found for {patient['first_name']} {patient['last_name']}")
                            messagebox.showinfo("No Records", 
                                              f"No medical records found for:\n\n"
                                              f"Patient: {patient['first_name']} {patient['last_name']}\n"
                                              f"Patient ID: {patient['patient_id']}")
                    
                    self.root.after(0, update_records)
                else:
                    raise Exception(response.get('message', 'Failed to load records'))
                    
            except ValueError:
                self.root.after(0, lambda: messagebox.showerror("Error", "Please enter a valid numeric Patient ID"))
            except Exception as e:
                def error_callback():
                    messagebox.showerror("Error", f"Failed to load medical records: {e}")
                    self.status_var.set("❌ Failed to load medical records")
                
                self.root.after(0, error_callback)
        
        threading.Thread(target=load_thread, daemon=True).start()
    
    def clear_medical_records(self):
        """Clear medical records display"""
        self.records_tree.delete(*self.records_tree.get_children())
        self.records_patient_id.delete(0, 'end')
        self.patient_info_label.config(text="💡 Enter a Patient ID and click 'Validate Patient' to verify", 
                                      fg=self.colors['primary'])
        self.records_count_label.config(text="")
        self.status_var.set("🗑️ Medical records cleared")
    
    def show_detailed_record(self, event):
        """Show detailed medical record in a popup"""
        selection = self.records_tree.selection()
        if not selection:
            return
        
        item = self.records_tree.item(selection[0])
        values = item['values']
        
        if not values:
            return
        
        # Get the full record data
        patient_id = self.records_patient_id.get().strip()
        if not patient_id:
            return
        
        def get_full_record():
            try:
                response = self.api_request(f'patients/{patient_id}/medical-records')
                if response['status'] == 'success':
                    records = response['data']
                    # Find the matching record by date and doctor
                    visit_date = values[0]  # Date from display
                    doctor_name = values[1]  # Doctor from display
                    
                    for record in records:
                        record_date = str(record.get('visit_date', ''))
                        if record_date:
                            try:
                                from datetime import datetime
                                date_obj = datetime.strptime(record_date.split()[0], '%Y-%m-%d')
                                formatted_date = date_obj.strftime('%d/%m/%Y')
                                if formatted_date == visit_date:
                                    self.root.after(0, lambda: self.display_detailed_record(record))
                                    return
                            except:
                                pass
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to load detailed record: {e}"))
        
        threading.Thread(target=get_full_record, daemon=True).start()
    
    def display_detailed_record(self, record):
        """Display detailed medical record in a popup window"""
        detail_window = tk.Toplevel(self.root)
        detail_window.title("📋 Detailed Medical Record")
        detail_window.geometry("800x600")
        detail_window.configure(bg=self.colors['card_bg'])
        detail_window.transient(self.root)
        detail_window.grab_set()
        
        # Header
        header_frame = tk.Frame(detail_window, bg=self.colors['primary'])
        header_frame.pack(fill='x')
        
        header_content = tk.Frame(header_frame, bg=self.colors['primary'])
        header_content.pack(fill='x', padx=30, pady=20)
        
        tk.Label(header_content, text="📋 Medical Record Details", 
                font=self.fonts['heading'], 
                bg=self.colors['primary'], 
                fg=self.colors['text_light']).pack(anchor='w')
        
        # Content
        content_frame = tk.Frame(detail_window, bg=self.colors['card_bg'])
        content_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Record details
        details = [
            ("📅 Visit Date", record.get('visit_date', 'N/A')),
            ("👨‍⚕️ Doctor", f"Dr. {record['doctor_first_name']} {record['doctor_last_name']}"),
            ("🏥 Specialization", record.get('specialization', 'N/A')),
            ("🔍 Diagnosis", record.get('diagnosis', 'N/A')),
            ("💊 Treatment", record.get('treatment', 'N/A')),
            ("📝 Prescription", record.get('prescription', 'N/A')),
            ("📋 Notes", record.get('notes', 'N/A'))
        ]
        
        for label, value in details:
            detail_frame = tk.Frame(content_frame, bg=self.colors['card_bg'])
            detail_frame.pack(fill='x', pady=10)
            
            tk.Label(detail_frame, text=label, 
                    font=self.fonts['subheading'], 
                    bg=self.colors['card_bg'], 
                    fg=self.colors['text_primary']).pack(anchor='w')
            
            # Use Text widget for long content
            if label in ["🔍 Diagnosis", "💊 Treatment", "📝 Prescription", "📋 Notes"]:
                text_widget = tk.Text(detail_frame, height=3, width=70, 
                                     font=self.fonts['body'],
                                     bg='#f8f9fa', 
                                     fg=self.colors['text_primary'],
                                     relief='solid', bd=1,
                                     wrap='word')
                text_widget.pack(fill='x', pady=(5,0))
                text_widget.insert('1.0', value or 'N/A')
                text_widget.config(state='disabled')
            else:
                tk.Label(detail_frame, text=value or 'N/A', 
                        font=self.fonts['body'], 
                        bg=self.colors['card_bg'], 
                        fg=self.colors['text_secondary']).pack(anchor='w', padx=20, pady=(5,0))
        
        # Close button
        close_btn = self.create_perfect_button(
            content_frame, "✖️ Close", 
            detail_window.destroy, self.colors['accent']
        )
        close_btn.pack(pady=20)
    

    
    def validate_patient_id(self):
        """Validate patient ID"""
        def validate_thread():
            try:
                patient_id = self.apt_patient_id.get()
                if not patient_id:
                    self.root.after(0, lambda: messagebox.showwarning("Warning", "Please enter a Patient ID"))
                    return
                
                response = self.api_request(f'validate/patient/{patient_id}')
                
                if response['status'] == 'success':
                    if response['exists']:
                        patient = response['patient']
                        self.root.after(0, lambda: messagebox.showinfo("Valid Patient", 
                                      f"✅ Patient found!\n\nID: {patient['patient_id']}\nName: {patient['first_name']} {patient['last_name']}"))
                    else:
                        self.root.after(0, lambda: messagebox.showerror("Invalid Patient", 
                                      f"❌ {response['message']}\n\nPlease check the Patient ID or register a new patient first."))
                else:
                    raise Exception(response.get('message', 'Validation failed'))
                    
            except ValueError:
                self.root.after(0, lambda: messagebox.showerror("Error", "Please enter a valid numeric Patient ID"))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Validation failed: {e}"))
        
        threading.Thread(target=validate_thread, daemon=True).start()
    
    def create_data_sorting_tab(self):
        """Create perfect Quick Sort tab with advanced functionality"""
        sorting_frame = tk.Frame(self.notebook, bg=self.colors['light'])
        self.notebook.add(sorting_frame, text="🔄 Quick Sort Analytics")
        
        # Perfect scrollable container
        canvas = tk.Canvas(sorting_frame, bg=self.colors['light'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(sorting_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['light'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Perfect header section
        header_section = tk.Frame(scrollable_frame, bg=self.colors['card_bg'], relief='flat', bd=0)
        header_section.pack(fill='x', padx=25, pady=25)
        
        header_content = tk.Frame(header_section, bg=self.colors['card_bg'])
        header_content.pack(fill='x', padx=40, pady=30)
        
        tk.Label(header_content, text="🔄 Advanced Quick Sort Analytics", 
                font=self.fonts['heading'], 
                bg=self.colors['card_bg'], 
                fg=self.colors['text_primary']).pack(anchor='w')
        
        tk.Label(header_content, text="High-performance O(n log n) sorting • Real-time data analysis • Multiple criteria", 
                font=self.fonts['body'], 
                bg=self.colors['card_bg'], 
                fg=self.colors['text_secondary']).pack(anchor='w', pady=(8,0))
        
        # Perfect sorting controls section
        controls_section = tk.Frame(scrollable_frame, bg=self.colors['card_bg'], relief='flat', bd=0)
        controls_section.pack(fill='x', padx=25, pady=(0,25))
        
        controls_content = tk.Frame(controls_section, bg=self.colors['card_bg'])
        controls_content.pack(fill='x', padx=40, pady=30)
        
        # Quick sort categories
        categories_frame = tk.Frame(controls_content, bg=self.colors['card_bg'])
        categories_frame.pack(fill='x')
        
        # Configure grid for three columns
        for i in range(3):
            categories_frame.grid_columnconfigure(i, weight=1)
        
        # Create perfect sorting categories
        self.create_perfect_sort_category(categories_frame, "📅 Date Sorting", 
                                        self.get_date_sort_options(), 0)
        self.create_perfect_sort_category(categories_frame, "👤 Name Sorting", 
                                        self.get_name_sort_options(), 1)
        self.create_perfect_sort_category(categories_frame, "🔢 ID Sorting", 
                                        self.get_id_sort_options(), 2)
        
        # Perfect results section
        results_section = tk.Frame(scrollable_frame, bg=self.colors['card_bg'], relief='flat', bd=0)
        results_section.pack(fill='both', expand=True, padx=25, pady=(0,25))
        
        results_content = tk.Frame(results_section, bg=self.colors['card_bg'])
        results_content.pack(fill='both', expand=True, padx=40, pady=30)
        
        # Results header
        results_header = tk.Frame(results_content, bg=self.colors['card_bg'])
        results_header.pack(fill='x', pady=(0,20))
        
        tk.Label(results_header, text="📊 Sort Results", 
                font=self.fonts['heading'], 
                bg=self.colors['card_bg'], 
                fg=self.colors['text_primary']).pack(side='left')
        
        # Clear button
        clear_btn = self.create_perfect_button(
            results_header, "🗑️ Clear Results", 
            self.clear_sort_results, self.colors['warning']
        )
        clear_btn.pack(side='right')
        
        # Results info
        self.sort_info_label = tk.Label(results_content, 
                                       text="🔄 Select a sorting option above to see results", 
                                       font=self.fonts['body'], 
                                       bg=self.colors['card_bg'], 
                                       fg=self.colors['text_secondary'])
        self.sort_info_label.pack(pady=(0,15))
        
        # Perfect results table
        table_frame = tk.Frame(results_content, bg=self.colors['card_bg'])
        table_frame.pack(fill='both', expand=True)
        
        self.sort_results_tree = ttk.Treeview(table_frame, 
                                             show='headings', 
                                             height=20,
                                             style='Perfect.Treeview')
        
        # Perfect scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.sort_results_tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient='horizontal', command=self.sort_results_tree.xview)
        
        self.sort_results_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack with perfect layout
        self.sort_results_tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    

    

    

    

    
    def quick_sort_by_criteria(self, data_type, sort_field, order):
        """Perform quick sort with specific criteria"""
        def sort_thread():
            try:
                self.root.after(0, lambda: self.status_var.set(f"Quick sorting {data_type} by {sort_field}..."))
                
                # Determine endpoint and data structure
                if data_type == 'records':
                    endpoint = 'records/sorted'
                    data_type_display = 'Medical Records'
                elif data_type == 'patients':
                    endpoint = 'patients/sorted'
                    data_type_display = 'Patients'
                elif data_type == 'appointments':
                    endpoint = 'appointments/sorted'
                    data_type_display = 'Appointments'
                
                # Make API request
                request_data = {
                    'sort_by': sort_field,
                    'order': order
                }
                
                response = self.api_request(endpoint, method='POST', data=request_data)
                
                if response['status'] == 'success':
                    def update_results():
                        self.display_sort_results(response['data'], response['sort_info'], data_type_display)
                        self.status_var.set(f"✅ Quick Sort completed: {response['sort_info']['record_count']} records")
                    
                    self.root.after(0, update_results)
                else:
                    raise Exception(response.get('message', 'Sort failed'))
                    
            except Exception as e:
                def error_callback():
                    messagebox.showerror("Error", f"Quick Sort failed: {e}")
                    self.status_var.set("❌ Quick Sort failed")
                
                self.root.after(0, error_callback)
        
        threading.Thread(target=sort_thread, daemon=True).start()
    
    
    def display_sort_results(self, data, sort_info, data_type):
        """Display sorted results in treeview"""
        # Clear existing results
        self.sort_results_tree.delete(*self.sort_results_tree.get_children())
        
        if not data:
            self.sort_info_label.config(text="No data found to sort", fg='#e74c3c')
            return
        
        # Configure columns based on data type
        if data_type == "Medical Records":
            columns = ('Record ID', 'Patient', 'Doctor', 'Visit Date', 'Diagnosis', 'Specialization')
            self.sort_results_tree['columns'] = columns
            
            for col in columns:
                self.sort_results_tree.heading(col, text=col)
                self.sort_results_tree.column(col, width=120)
            
            # Populate data
            for record in data:
                visit_date = str(record.get('visit_date', 'N/A')).split()[0] if record.get('visit_date') else 'N/A'
                self.sort_results_tree.insert('', 'end', values=(
                    record.get('record_id', 'N/A'),
                    f"{record.get('patient_first_name', '')} {record.get('patient_last_name', '')}",
                    f"Dr. {record.get('doctor_first_name', '')} {record.get('doctor_last_name', '')}",
                    visit_date,
                    record.get('diagnosis', 'N/A')[:30] + '...' if len(str(record.get('diagnosis', ''))) > 30 else record.get('diagnosis', 'N/A'),
                    record.get('specialization', 'N/A')
                ))
        
        elif data_type == "Patients":
            columns = ('Patient ID', 'Name', 'Date of Birth', 'Gender', 'Phone', 'Email')
            self.sort_results_tree['columns'] = columns
            
            for col in columns:
                self.sort_results_tree.heading(col, text=col)
                self.sort_results_tree.column(col, width=120)
            
            # Populate data
            for patient in data:
                dob = str(patient.get('date_of_birth', 'N/A')).split()[0] if patient.get('date_of_birth') else 'N/A'
                self.sort_results_tree.insert('', 'end', values=(
                    patient.get('patient_id', 'N/A'),
                    f"{patient.get('first_name', '')} {patient.get('last_name', '')}",
                    dob,
                    patient.get('gender', 'N/A'),
                    patient.get('phone', 'N/A'),
                    patient.get('email', 'N/A')
                ))
        
        elif data_type == "Appointments":
            columns = ('Appointment ID', 'Patient', 'Doctor', 'Date', 'Time', 'Status')
            self.sort_results_tree['columns'] = columns
            
            for col in columns:
                self.sort_results_tree.heading(col, text=col)
                self.sort_results_tree.column(col, width=120)
            
            # Populate data
            for appointment in data:
                apt_date = str(appointment.get('appointment_date', 'N/A')).split()[0] if appointment.get('appointment_date') else 'N/A'
                self.sort_results_tree.insert('', 'end', values=(
                    appointment.get('appointment_id', 'N/A'),
                    f"{appointment.get('patient_first_name', '')} {appointment.get('patient_last_name', '')}",
                    f"Dr. {appointment.get('doctor_first_name', '')} {appointment.get('doctor_last_name', '')}",
                    apt_date,
                    appointment.get('appointment_time', 'N/A'),
                    appointment.get('status', 'N/A')
                ))
        
        # Update info label with perfect styling
        info_text = (f"✅ {sort_info['message']}\n"
                    f"📊 Algorithm: {sort_info['algorithm']} | "
                    f"Records: {sort_info['record_count']} | "
                    f"Field: {sort_info['sort_by']} | "
                    f"Order: {sort_info['order'].title()}ending")
        
        self.sort_info_label.config(text=info_text, fg=self.colors['success'], font=self.fonts['body'])
    
    def clear_sort_results(self):
        """Clear sort results with perfect styling"""
        self.sort_results_tree.delete(*self.sort_results_tree.get_children())
        self.sort_info_label.config(text="🔄 Select a sorting option above to see results", 
                                   fg=self.colors['text_secondary'], 
                                   font=self.fonts['body'])
        self.status_var.set("🗑️ Sort results cleared")

def main():
    root = tk.Tk()
    app = HospitalFlaskGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
`

---


## create_hospital_database.py

### Database Setup Script

`python
import mysql.connector
from mysql.connector import Error
from datetime import datetime, date, timedelta
import random

def create_complete_database():
    """Create complete hospital database with sample data"""
    
    connection = None
    try:
        # Connect to MySQL
        connection = mysql.connector.connect(
            host="localhost",
            user="amaanraza",
            password="Amaan123!"
        )
        
        cursor = connection.cursor()
        
        # Create database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS hospital_management")
        cursor.execute("USE hospital_management")
        print("✅ Database 'hospital_management' created/selected")
        
        # Drop existing tables to recreate with fresh data
        tables_to_drop = ['billing', 'medical_records', 'appointments', 'rooms', 'doctors', 'patients']
        for table in tables_to_drop:
            cursor.execute(f"DROP TABLE IF EXISTS {table}")
        
        # Create patients table
        patients_table = """
        CREATE TABLE patients (
            patient_id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            date_of_birth DATE NOT NULL,
            gender ENUM('Male', 'Female', 'Other') NOT NULL,
            phone VARCHAR(15),
            email VARCHAR(100),
            address TEXT,
            emergency_contact_name VARCHAR(100),
            emergency_contact_phone VARCHAR(15),
            blood_type VARCHAR(5),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """
        
        # Create doctors table
        doctors_table = """
        CREATE TABLE doctors (
            doctor_id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            specialization VARCHAR(100) NOT NULL,
            phone VARCHAR(15),
            email VARCHAR(100),
            license_number VARCHAR(50) UNIQUE,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """
        
        # Create appointments table
        appointments_table = """
        CREATE TABLE appointments (
            appointment_id INT AUTO_INCREMENT PRIMARY KEY,
            patient_id INT NOT NULL,
            doctor_id INT NOT NULL,
            appointment_date DATE NOT NULL,
            appointment_time TIME NOT NULL,
            status ENUM('Scheduled', 'In Progress', 'Completed', 'Cancelled') DEFAULT 'Scheduled',
            reason TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
            FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE
        )
        """
        
        # Create medical records table
        medical_records_table = """
        CREATE TABLE medical_records (
            record_id INT AUTO_INCREMENT PRIMARY KEY,
            patient_id INT NOT NULL,
            doctor_id INT NOT NULL,
            visit_date DATE NOT NULL,
            diagnosis TEXT,
            treatment TEXT,
            prescription TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
            FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE
        )
        """
        
        # Create rooms table
        rooms_table = """
        CREATE TABLE rooms (
            room_id INT AUTO_INCREMENT PRIMARY KEY,
            room_number VARCHAR(10) UNIQUE NOT NULL,
            room_type ENUM('General', 'Private', 'ICU', 'Emergency') NOT NULL,
            bed_count INT DEFAULT 1,
            is_occupied BOOLEAN DEFAULT FALSE,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """
        
        # Create billing table
        billing_table = """
        CREATE TABLE billing (
            bill_id INT AUTO_INCREMENT PRIMARY KEY,
            patient_id INT NOT NULL,
            appointment_id INT,
            amount DECIMAL(10,2) NOT NULL,
            description TEXT,
            status ENUM('Pending', 'Paid', 'Cancelled') DEFAULT 'Pending',
            bill_date DATE NOT NULL,
            due_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
            FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id) ON DELETE SET NULL
        )
        """
        
        # Execute table creation
        tables = [
            ("patients", patients_table),
            ("doctors", doctors_table),
            ("appointments", appointments_table),
            ("medical_records", medical_records_table),
            ("rooms", rooms_table),
            ("billing", billing_table)
        ]
        
        for table_name, table_query in tables:
            cursor.execute(table_query)
            print(f"✅ Table '{table_name}' created successfully")
        
        # Insert sample data
        insert_sample_patients(cursor)
        insert_sample_doctors(cursor)
        insert_sample_rooms(cursor)
        insert_sample_appointments(cursor)
        insert_sample_medical_records(cursor)
        
        connection.commit()
        print("\n🎉 Hospital database created successfully with sample data!")
        
        # Display summary
        display_database_summary(cursor)
        
    except Error as e:
        print(f"❌ Error: {e}")
    
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def insert_sample_patients(cursor):
    """Insert sample Indian patients with authentic names"""
    
    patients_data = [
        ('Rajesh', 'Sharma', '1985-03-15', 'Male', '+91-9876543210', 'rajesh.sharma@email.com', 'A-101, Sector 15, Noida, UP', 'Sunita Sharma', '+91-9876543211', 'O+'),
        ('Priya', 'Patel', '1990-07-22', 'Female', '+91-9876543212', 'priya.patel@email.com', 'B-205, Andheri West, Mumbai, MH', 'Amit Patel', '+91-9876543213', 'A+'),
        ('Arjun', 'Singh', '1978-11-08', 'Male', '+91-9876543214', 'arjun.singh@email.com', 'C-301, Lajpat Nagar, New Delhi', 'Kavita Singh', '+91-9876543215', 'B+'),
        ('Sneha', 'Reddy', '1995-02-14', 'Female', '+91-9876543216', 'sneha.reddy@email.com', 'D-402, Banjara Hills, Hyderabad, TS', 'Ravi Reddy', '+91-9876543217', 'AB+'),
        ('Vikram', 'Gupta', '1982-09-30', 'Male', '+91-9876543218', 'vikram.gupta@email.com', 'E-503, Salt Lake, Kolkata, WB', 'Meera Gupta', '+91-9876543219', 'O-'),
        ('Ananya', 'Iyer', '1988-12-05', 'Female', '+91-9876543220', 'ananya.iyer@email.com', 'F-604, Koramangala, Bangalore, KA', 'Suresh Iyer', '+91-9876543221', 'A-'),
        ('Rohit', 'Joshi', '1975-06-18', 'Male', '+91-9876543222', 'rohit.joshi@email.com', 'G-705, Pune Camp, Pune, MH', 'Pooja Joshi', '+91-9876543223', 'B-'),
        ('Deepika', 'Nair', '1992-04-25', 'Female', '+91-9876543224', 'deepika.nair@email.com', 'H-806, Kochi Marine Drive, Kerala', 'Arun Nair', '+91-9876543225', 'AB-'),
        ('Karan', 'Malhotra', '1980-01-12', 'Male', '+91-9876543226', 'karan.malhotra@email.com', 'I-907, Chandigarh Sector 17', 'Simran Malhotra', '+91-9876543227', 'O+'),
        ('Riya', 'Agarwal', '1993-08-07', 'Female', '+91-9876543228', 'riya.agarwal@email.com', 'J-108, Jaipur Pink City, RJ', 'Manish Agarwal', '+91-9876543229', 'A+'),
        ('Siddharth', 'Kapoor', '1987-05-20', 'Male', '+91-9876543230', 'siddharth.kapoor@email.com', 'K-209, Lucknow Gomti Nagar, UP', 'Neha Kapoor', '+91-9876543231', 'B+'),
        ('Ishita', 'Bansal', '1991-10-03', 'Female', '+91-9876543232', 'ishita.bansal@email.com', 'L-310, Gurgaon Cyber City, HR', 'Rahul Bansal', '+91-9876543233', 'O-'),
        ('Aarav', 'Chopra', '1984-07-16', 'Male', '+91-9876543234', 'aarav.chopra@email.com', 'M-411, Ahmedabad Satellite, GJ', 'Tanya Chopra', '+91-9876543235', 'A-'),
        ('Kavya', 'Menon', '1989-03-28', 'Female', '+91-9876543236', 'kavya.menon@email.com', 'N-512, Chennai T.Nagar, TN', 'Vivek Menon', '+91-9876543237', 'B-'),
        ('Aryan', 'Sinha', '1976-12-11', 'Male', '+91-9876543238', 'aryan.sinha@email.com', 'O-613, Patna Boring Road, BR', 'Shreya Sinha', '+91-9876543239', 'AB+'),
        ('Diya', 'Verma', '1994-05-03', 'Female', '+91-9876543240', 'diya.verma@email.com', 'P-714, Indore Vijay Nagar, MP', 'Ajay Verma', '+91-9876543241', 'O+'),
        ('Nikhil', 'Pandey', '1986-09-17', 'Male', '+91-9876543242', 'nikhil.pandey@email.com', 'Q-815, Varanasi Cantonment, UP', 'Priyanka Pandey', '+91-9876543243', 'A+'),
        ('Aditi', 'Saxena', '1992-11-29', 'Female', '+91-9876543244', 'aditi.saxena@email.com', 'R-916, Bhopal New Market, MP', 'Rohit Saxena', '+91-9876543245', 'B+'),
        ('Harsh', 'Tiwari', '1983-02-08', 'Male', '+91-9876543246', 'harsh.tiwari@email.com', 'S-117, Kanpur Civil Lines, UP', 'Anjali Tiwari', '+91-9876543247', 'AB-'),
        ('Nisha', 'Bhatt', '1990-06-21', 'Female', '+91-9876543248', 'nisha.bhatt@email.com', 'T-218, Surat Diamond City, GJ', 'Kiran Bhatt', '+91-9876543249', 'O-'),
        
        # Additional 10 patients (IDs 21-30)
        ('Manish', 'Kumar', '1988-04-12', 'Male', '+91-9876543250', 'manish.kumar@email.com', 'U-319, Dehradun Clock Tower, UK', 'Sunita Kumar', '+91-9876543251', 'A+'),
        ('Pooja', 'Sharma', '1991-08-25', 'Female', '+91-9876543252', 'pooja.sharma@email.com', 'V-420, Jaipur Malviya Nagar, RJ', 'Rajesh Sharma', '+91-9876543253', 'B+'),
        ('Amit', 'Verma', '1979-11-30', 'Male', '+91-9876543254', 'amit.verma@email.com', 'W-521, Agra Sadar Bazaar, UP', 'Rekha Verma', '+91-9876543255', 'O+'),
        ('Neha', 'Singh', '1993-01-18', 'Female', '+91-9876543256', 'neha.singh@email.com', 'X-622, Ranchi Main Road, JH', 'Sunil Singh', '+91-9876543257', 'AB+'),
        ('Rahul', 'Gupta', '1985-06-08', 'Male', '+91-9876543258', 'rahul.gupta@email.com', 'Y-723, Nashik College Road, MH', 'Priya Gupta', '+91-9876543259', 'A-'),
        ('Swati', 'Jain', '1989-09-14', 'Female', '+91-9876543260', 'swati.jain@email.com', 'Z-824, Udaipur City Palace, RJ', 'Anil Jain', '+91-9876543261', 'B-'),
        ('Vishal', 'Yadav', '1981-12-22', 'Male', '+91-9876543262', 'vishal.yadav@email.com', 'AA-925, Meerut Cantonment, UP', 'Kavita Yadav', '+91-9876543263', 'O-'),
        ('Anjali', 'Mishra', '1994-03-05', 'Female', '+91-9876543264', 'anjali.mishra@email.com', 'BB-126, Varanasi Godowlia, UP', 'Deepak Mishra', '+91-9876543265', 'AB-'),
        ('Suresh', 'Pandey', '1977-07-19', 'Male', '+91-9876543266', 'suresh.pandey@email.com', 'CC-227, Allahabad Civil Lines, UP', 'Geeta Pandey', '+91-9876543267', 'A+'),
        ('Ritu', 'Agarwal', '1992-10-11', 'Female', '+91-9876543268', 'ritu.agarwal@email.com', 'DD-328, Jodhpur Ratanada, RJ', 'Mohit Agarwal', '+91-9876543269', 'B+')
    ]
    
    insert_patients_query = """
    INSERT INTO patients (first_name, last_name, date_of_birth, gender, phone, email, address, emergency_contact_name, emergency_contact_phone, blood_type)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.executemany(insert_patients_query, patients_data)
    print(f"✅ {len(patients_data)} sample patients inserted")

def insert_sample_doctors(cursor):
    """Insert sample Indian doctors"""
    
    doctors_data = [
        ('Dr. Rajesh', 'Sharma', 'Cardiology', '+91-9876501001', 'dr.rajesh.sharma@hospital.com', 'MCI001'),
        ('Dr. Priya', 'Gupta', 'Pediatrics', '+91-9876501002', 'dr.priya.gupta@hospital.com', 'MCI002'),
        ('Dr. Amit', 'Singh', 'Orthopedics', '+91-9876501003', 'dr.amit.singh@hospital.com', 'MCI003'),
        ('Dr. Sunita', 'Reddy', 'Neurology', '+91-9876501004', 'dr.sunita.reddy@hospital.com', 'MCI004'),
        ('Dr. Vikram', 'Patel', 'General Medicine', '+91-9876501005', 'dr.vikram.patel@hospital.com', 'MCI005'),
        ('Dr. Kavya', 'Iyer', 'Dermatology', '+91-9876501006', 'dr.kavya.iyer@hospital.com', 'MCI006'),
        ('Dr. Arjun', 'Malhotra', 'Psychiatry', '+91-9876501007', 'dr.arjun.malhotra@hospital.com', 'MCI007'),
        ('Dr. Deepika', 'Agarwal', 'Gynecology', '+91-9876501008', 'dr.deepika.agarwal@hospital.com', 'MCI008'),
        ('Dr. Rohit', 'Kapoor', 'Surgery', '+91-9876501009', 'dr.rohit.kapoor@hospital.com', 'MCI009'),
        ('Dr. Ananya', 'Nair', 'Radiology', '+91-9876501010', 'dr.ananya.nair@hospital.com', 'MCI010'),
        ('Dr. Karan', 'Joshi', 'Pulmonology', '+91-9876501011', 'dr.karan.joshi@hospital.com', 'MCI011'),
        ('Dr. Riya', 'Chopra', 'Endocrinology', '+91-9876501012', 'dr.riya.chopra@hospital.com', 'MCI012')
    ]
    
    insert_doctors_query = """
    INSERT INTO doctors (first_name, last_name, specialization, phone, email, license_number)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.executemany(insert_doctors_query, doctors_data)
    print(f"✅ {len(doctors_data)} sample doctors inserted")

def insert_sample_rooms(cursor):
    """Insert sample rooms"""
    
    rooms_data = [
        ('101', 'General', 2, False),
        ('102', 'General', 2, False),
        ('103', 'General', 2, True),
        ('201', 'Private', 1, False),
        ('202', 'Private', 1, True),
        ('203', 'Private', 1, False),
        ('301', 'ICU', 1, False),
        ('302', 'ICU', 1, True),
        ('303', 'ICU', 1, False),
        ('401', 'Emergency', 1, False),
        ('402', 'Emergency', 1, False)
    ]
    
    insert_rooms_query = """
    INSERT INTO rooms (room_number, room_type, bed_count, is_occupied)
    VALUES (%s, %s, %s, %s)
    """
    cursor.executemany(insert_rooms_query, rooms_data)
    print(f"✅ {len(rooms_data)} sample rooms inserted")

def insert_sample_appointments(cursor):
    """Insert sample appointments"""
    
    today = date.today()
    tomorrow = today + timedelta(days=1)
    yesterday = today - timedelta(days=1)
    
    appointments_data = [
        (1, 1, today, '09:00:00', 'Scheduled', 'Regular checkup'),
        (2, 2, today, '10:30:00', 'Scheduled', 'Child vaccination'),
        (3, 3, today, '14:00:00', 'Completed', 'Knee pain consultation'),
        (4, 4, today, '15:30:00', 'Scheduled', 'Headache evaluation'),
        (5, 5, tomorrow, '09:30:00', 'Scheduled', 'Annual physical'),
        (6, 1, tomorrow, '11:00:00', 'Scheduled', 'Follow-up visit'),
        (7, 6, tomorrow, '13:30:00', 'Scheduled', 'Skin examination'),
        (8, 7, yesterday, '10:00:00', 'Completed', 'Therapy session'),
        (9, 8, yesterday, '14:30:00', 'Completed', 'Routine gynecological exam'),
        (10, 9, yesterday, '16:00:00', 'Completed', 'Pre-surgery consultation')
    ]
    
    insert_appointments_query = """
    INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, status, reason)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.executemany(insert_appointments_query, appointments_data)
    print(f"✅ {len(appointments_data)} sample appointments inserted")

def insert_sample_medical_records(cursor):
    """Insert comprehensive medical records with detailed Indian health conditions"""
    
    records_data = [
        # Rajesh Sharma (Patient ID: 1) - Comprehensive Cardiology Records
        (1, 1, '2024-11-05', 'Acute Myocardial Infarction (STEMI)', 'Emergency PCI with stent placement, dual antiplatelet therapy', 'Clopidogrel 75mg + Aspirin 75mg daily, Atorvastatin 40mg, Metoprolol 25mg BD', 'Patient presented with severe chest pain. ECG showed ST elevation in leads II, III, aVF. Troponin I: 15.2 ng/ml. Emergency cardiac catheterization performed. RCA 95% stenosis treated with drug-eluting stent. Post-procedure stable.'),
        (1, 1, '2024-10-15', 'Hypertension with Type 2 Diabetes Mellitus', 'Optimization of antihypertensive and antidiabetic therapy', 'Amlodipine 5mg OD, Telmisartan 40mg OD, Metformin 500mg BD, Glimepiride 2mg OD', 'BP: 160/95 mmHg, FBS: 145 mg/dl, PPBS: 210 mg/dl, HbA1c: 8.2%. Fundoscopy shows mild diabetic retinopathy. Advised diabetic diet, regular exercise. Nephrology referral for microalbuminuria.'),
        (1, 1, '2024-09-20', 'Unstable Angina', 'Medical management, risk stratification', 'Aspirin 75mg, Clopidogrel 75mg, Atorvastatin 20mg, Metoprolol 12.5mg BD', 'Chest pain on exertion for 2 weeks. ECG shows T-wave inversions in V4-V6. Troponin negative. 2D Echo: RWMA in inferior wall, EF: 45%. TMT positive at 6 METS. Advised lifestyle modifications.'),
        (1, 5, '2024-08-10', 'Annual Comprehensive Health Checkup', 'Preventive care assessment', 'Continue current cardiac medications, add Vitamin D3 supplements', 'Complete metabolic panel: Cholesterol 220 mg/dl, LDL 140 mg/dl, HDL 35 mg/dl, Triglycerides 180 mg/dl. Vitamin D: 18 ng/ml (deficient). PSA: 2.1 ng/ml (normal). Advised annual cardiac follow-up.'),
        (1, 1, '2024-07-05', 'Heart Failure with Reduced Ejection Fraction', 'ACE inhibitor therapy, diuretics', 'Enalapril 2.5mg BD, Furosemide 20mg OD, Spironolactone 25mg OD', 'NYHA Class II symptoms. 2D Echo: Global hypokinesia, EF: 35%. BNP: 450 pg/ml. Chest X-ray shows cardiomegaly. Advised salt restriction, fluid monitoring.'),
        
        # Priya Patel (Patient ID: 2) - Pediatric Records
        (2, 2, '2024-11-01', 'Dengue Hemorrhagic Fever', 'Intensive monitoring, platelet transfusion', 'Paracetamol 15mg/kg QID, ORS, Platelet concentrate 1 unit', 'Day 5 of fever. Platelet count: 25,000/μl, Hematocrit: 45%. Tourniquet test positive. Capillary fragility increased. No bleeding manifestations. Admitted for close monitoring. IV fluids as per WHO protocol.'),
        (2, 2, '2024-09-15', 'Acute Bronchiolitis', 'Supportive care, bronchodilator therapy', 'Salbutamol nebulization 2.5mg TDS, Prednisolone 1mg/kg for 3 days', 'Age: 3 years. Presented with cough, wheeze, difficulty breathing for 3 days. O2 saturation: 94% on room air. Chest X-ray: hyperinflation, no consolidation. RSV antigen positive. Improved with treatment.'),
        (2, 2, '2024-07-20', 'Routine Immunization - MMR and Varicella', 'Vaccination as per IAP schedule', 'MMR vaccine 0.5ml SC, Varicella vaccine 0.5ml SC', 'Age: 15 months. Weight: 10.5 kg (50th percentile). Height: 78 cm (25th percentile). Development appropriate for age. No adverse reactions post-vaccination. Next visit at 18 months.'),
        (2, 2, '2024-06-10', 'Acute Gastroenteritis with Dehydration', 'Oral rehydration therapy, probiotics', 'ORS 75ml/kg over 4 hours, Zinc 10mg OD for 14 days, Probiotics', 'Loose stools 8-10 times/day for 2 days. Mild dehydration (5%). No blood/mucus in stools. Stool routine: pus cells 2-3/hpf. Rotavirus antigen negative. Improved with ORT.'),
        (2, 2, '2024-04-15', 'Iron Deficiency Anemia', 'Iron supplementation, dietary counseling', 'Ferrous sulfate drops 3mg/kg/day, Vitamin C 25mg OD', 'Pallor noted during routine check-up. Hb: 8.5 g/dl, MCV: 65 fl, Serum ferritin: 8 ng/ml. Dietary history reveals inadequate iron intake. Mother counseled about iron-rich foods.'),
        
        # Arjun Singh (Patient ID: 3) - Orthopedic Records
        (3, 3, '2024-10-25', 'Lumbar Disc Herniation L4-L5 with Radiculopathy', 'Conservative management, epidural steroid injection', 'Pregabalin 75mg BD, Diclofenac 50mg BD, Thiocolchicoside 4mg BD', 'Chronic low back pain radiating to right leg for 6 months. MRI: L4-L5 disc herniation compressing right L5 nerve root. SLR test positive at 30°. Neurological deficit: weakness in EHL. Epidural injection planned.'),
        (3, 3, '2024-09-10', 'Bilateral Knee Osteoarthritis Grade II', 'Intra-articular hyaluronic acid injection', 'Glucosamine 1500mg + Chondroitin 1200mg OD, Topical diclofenac gel', 'Bilateral knee pain for 2 years, worse on climbing stairs. X-ray: joint space narrowing, osteophytes. No effusion. ROM: flexion 120°. Kellgren-Lawrence Grade II. Physiotherapy advised.'),
        (3, 5, '2024-08-05', 'Mechanical Low Back Pain', 'Physiotherapy, ergonomic advice', 'Thiocolchicoside 4mg BD for 5 days, Hot fomentation', 'Acute onset back pain after lifting heavy object. No radicular symptoms. SLR negative. Paraspinal muscle spasm present. X-ray lumbar spine normal. Workplace ergonomic assessment recommended.'),
        (3, 3, '2024-06-20', 'Right Shoulder Impingement Syndrome', 'Subacromial steroid injection, physiotherapy', 'Methylprednisolone 40mg injection, Physiotherapy exercises', 'Right shoulder pain for 3 months, worse with overhead activities. Hawkins test positive, Neer sign positive. MRI: subacromial bursitis, no rotator cuff tear. Injection given under ultrasound guidance.'),
        (3, 3, '2024-04-10', 'Cervical Spondylosis with Myelopathy', 'Cervical collar, neuroprotective agents', 'Methylcobalamin 1500mcg OD, Pregabalin 75mg BD, Soft cervical collar', 'Neck pain with bilateral hand numbness for 4 months. MRI cervical spine: C5-C6 disc osteophyte complex causing cord compression. Hoffmann sign positive. Surgical consultation advised.'),
        
        # Sneha Reddy (Patient ID: 4) - Neurology Records
        (4, 4, '2024-11-02', 'Migraine with Aura (Episodic)', 'Prophylactic therapy initiated', 'Propranolol 40mg BD, Sumatriptan 50mg SOS, Topiramate 25mg OD', 'Recurrent headaches for 5 years, 4-5 episodes/month. Typical migraine with visual aura lasting 20-30 minutes. Headache unilateral, throbbing, photophobia present. MRI brain normal. Trigger diary maintained.'),
        (4, 4, '2024-09-18', 'Tension-Type Headache (Chronic)', 'Tricyclic antidepressant, stress management', 'Amitriptyline 25mg at bedtime, relaxation techniques', 'Daily headaches for 6 months, band-like, bilateral. Associated with work stress. No nausea/vomiting. Neurological examination normal. Stress management counseling provided.'),
        (4, 8, '2024-08-12', 'Generalized Anxiety Disorder', 'Cognitive behavioral therapy, anxiolytic', 'Escitalopram 10mg OD, Clonazepam 0.25mg SOS', 'Excessive worry, restlessness, sleep disturbance for 8 months. GAD-7 score: 15 (severe anxiety). No panic attacks. Thyroid function normal. CBT sessions scheduled.'),
        (4, 4, '2024-06-15', 'Carpal Tunnel Syndrome (Bilateral)', 'Wrist splints, nerve conduction study', 'Pregabalin 75mg BD, Wrist splints at night', 'Bilateral hand numbness and tingling for 4 months, worse at night. Tinel and Phalen signs positive. NCS: prolonged distal latency of median nerve. Conservative management advised.'),
        (4, 4, '2024-03-20', 'Benign Paroxysmal Positional Vertigo', 'Canalith repositioning maneuver', 'Betahistine 16mg TDS for 1 week', 'Episodic vertigo triggered by head movements for 2 weeks. Dix-Hallpike test positive with rotatory nystagmus. No hearing loss. Epley maneuver performed with symptom resolution.'),
        
        # Vikram Gupta (Patient ID: 5) - General Medicine Records
        (5, 5, '2024-10-30', 'Acute Gastroenteritis with Moderate Dehydration', 'IV fluid therapy, antimotility agents', 'DNS 1L + KCl 20mEq over 8 hours, Loperamide 2mg BD, Probiotics', 'Acute onset diarrhea 6-8 times/day with vomiting for 2 days. Moderate dehydration (6-9%). Stool routine: pus cells 4-6/hpf. Stool culture pending. IV rehydration initiated.'),
        (5, 5, '2024-09-25', 'Allergic Rhinitis (Seasonal)', 'Antihistamines, intranasal corticosteroids', 'Cetirizine 10mg OD, Fluticasone nasal spray 2 puffs BD', 'Seasonal sneezing, nasal congestion, watery discharge for 3 weeks. Nasal examination: pale, boggy turbinates. Eosinophil count: 8%. Skin prick test: positive for grass pollen.'),
        (5, 5, '2024-08-15', 'Viral Hepatitis A', 'Supportive care, liver function monitoring', 'Ursodeoxycholic acid 300mg BD, Multivitamins', 'Jaundice, dark urine, clay-colored stools for 1 week. LFT: Bilirubin 8.5 mg/dl, ALT 450 U/L, AST 380 U/L. HAV IgM positive. Advised rest, high-calorie diet.'),
        (5, 5, '2024-06-10', 'Urinary Tract Infection (Cystitis)', 'Antibiotic therapy based on culture sensitivity', 'Nitrofurantoin 100mg BD for 5 days, increased fluid intake', 'Dysuria, frequency, urgency for 3 days. Urine routine: pus cells 15-20/hpf, bacteria present. Urine culture: E.coli >10^5 CFU/ml, sensitive to nitrofurantoin.'),
        (5, 5, '2024-04-20', 'Peptic Ulcer Disease (Duodenal)', 'H. pylori eradication therapy', 'Pantoprazole 40mg BD, Clarithromycin 500mg BD, Amoxicillin 1g BD for 14 days', 'Epigastric pain, worse when hungry, relieved by food. H. pylori stool antigen positive. Upper GI endoscopy: duodenal ulcer 8mm. Triple therapy initiated.'),
        
        # Ananya Iyer (Patient ID: 6) - Dermatology Records
        (6, 6, '2024-11-01', 'Atopic Dermatitis (Moderate to Severe)', 'Topical immunomodulators, systemic antihistamines', 'Tacrolimus 0.1% ointment BD, Cetirizine 10mg OD, Moisturizer TDS', 'Chronic eczematous lesions on flexural areas for 2 years. SCORAD index: 45. Serum IgE: 850 IU/ml. Patch test negative. Advised cotton clothing, avoid harsh soaps.'),
        (6, 6, '2024-09-20', 'Acne Vulgaris (Moderate)', 'Topical retinoids and antibiotics', 'Tretinoin 0.025% gel at night, Clindamycin 1% gel in morning', 'Inflammatory papules and pustules on face for 6 months. Grade II acne. No scarring. Comedones present. Advised gentle cleansing, oil-free moisturizer.'),
        (6, 6, '2024-07-15', 'Melasma (Facial)', 'Topical depigmenting agents, sun protection', 'Hydroquinone 2% + Tretinoin 0.025% + Fluocinolone 0.01% cream', 'Bilateral facial hyperpigmentation for 8 months, worse after sun exposure. MASI score: 12. Wood lamp examination: epidermal type. Strict sun protection advised.'),
        (6, 6, '2024-05-10', 'Seborrheic Dermatitis', 'Antifungal shampoo, topical corticosteroids', 'Ketoconazole 2% shampoo twice weekly, Fluocinolone 0.01% lotion', 'Scaly, erythematous patches on scalp and face for 3 months. KOH examination: spores and hyphae of Malassezia. Good response to antifungal therapy.'),
        (6, 6, '2024-02-25', 'Psoriasis Vulgaris (Mild)', 'Topical corticosteroids, vitamin D analogues', 'Clobetasol 0.05% ointment BD for 2 weeks, then Calcipotriol ointment', 'Well-demarcated erythematous plaques with silvery scales on elbows and knees. PASI score: 8. Family history positive. Advised stress management.'),
        
        # Rohit Joshi (Patient ID: 7) - Pulmonology Records
        (7, 11, '2024-10-28', 'Acute Exacerbation of Bronchial Asthma', 'Systemic corticosteroids, nebulization', 'Prednisolone 40mg OD for 5 days, Salbutamol + Ipratropium nebulization QID', 'Acute breathlessness, wheeze for 2 days. Peak flow: 60% of predicted. Chest examination: bilateral wheeze. Chest X-ray normal. Trigger: viral URTI.'),
        (7, 11, '2024-09-15', 'Chronic Cough (Post-infectious)', 'Bronchodilators, cough suppressants', 'Montelukast 10mg OD, Dextromethorphan 15mg TDS', 'Persistent dry cough for 6 weeks following viral URTI. Chest X-ray normal. Spirometry: mild obstruction. Methacholine challenge test positive.'),
        (7, 11, '2024-07-20', 'Allergic Bronchopulmonary Aspergillosis', 'Systemic corticosteroids, antifungal therapy', 'Prednisolone 0.5mg/kg for 4 weeks, Itraconazole 200mg BD', 'Recurrent wheeze, productive cough with brownish sputum. Chest X-ray: fleeting infiltrates. Total IgE: 2500 IU/ml, Aspergillus-specific IgE positive.'),
        (7, 11, '2024-05-10', 'Pneumonia (Community-acquired)', 'Antibiotic therapy, supportive care', 'Azithromycin 500mg OD for 5 days, Paracetamol 650mg TDS', 'Fever, productive cough, chest pain for 4 days. Chest X-ray: right lower lobe consolidation. CURB-65 score: 1. Outpatient management.'),
        (7, 11, '2024-02-15', 'Chronic Obstructive Pulmonary Disease (GOLD Stage II)', 'Bronchodilator therapy, pulmonary rehabilitation', 'Tiotropium 18mcg OD, Formoterol + Budesonide 12/400 BD', 'Progressive breathlessness for 2 years. Smoking history: 20 pack-years. Spirometry: FEV1 65% predicted. mMRC grade 2 dyspnea.'),
        
        # Deepika Nair (Patient ID: 8) - Gynecology Records
        (8, 8, '2024-10-26', 'Polycystic Ovary Syndrome with Insulin Resistance', 'Hormonal therapy, insulin sensitizers', 'Metformin 500mg BD, Combined OCP (Ethinyl estradiol + Drospirenone)', 'Irregular periods, hirsutism, weight gain for 2 years. BMI: 28 kg/m². Ultrasound: bilateral polycystic ovaries. HOMA-IR: 4.2. Lifestyle modification counseled.'),
        (8, 8, '2024-08-20', 'Routine Gynecological Examination', 'Preventive screening', 'Folic acid 5mg OD, Calcium + Vitamin D supplements', 'Annual check-up. Pap smear: NILM. Breast examination normal. Mammography recommended at age 40. Contraceptive counseling provided.'),
        (8, 8, '2024-06-15', 'Dysfunctional Uterine Bleeding', 'Hormonal regulation', 'Tranexamic acid 500mg TDS during menses, Iron supplements', 'Heavy menstrual bleeding for 4 months. Hemoglobin: 9.2 g/dl. Ultrasound pelvis: normal uterus and ovaries. Thyroid function normal.'),
        (8, 8, '2024-04-10', 'Urinary Tract Infection (Recurrent)', 'Antibiotic therapy, prophylaxis counseling', 'Nitrofurantoin 100mg BD for 7 days, Cranberry extract', 'Third episode of UTI in 6 months. Urine culture: E.coli sensitive to nitrofurantoin. Post-coital prophylaxis and hygiene measures advised.'),
        (8, 8, '2024-01-20', 'Ovarian Cyst (Functional)', 'Conservative management, follow-up', 'Oral contraceptive pills for 3 months', 'Right-sided pelvic pain for 2 weeks. Ultrasound: 4cm simple ovarian cyst. No complications. Repeat scan after 3 months showed resolution.'),
        
        # Karan Malhotra (Patient ID: 9) - Psychiatry Records
        (9, 7, '2024-10-24', 'Major Depressive Disorder (Moderate)', 'Antidepressant therapy, psychotherapy', 'Sertraline 50mg OD, Cognitive Behavioral Therapy sessions', 'Low mood, anhedonia, sleep disturbance for 3 months. PHQ-9 score: 16. Work-related stress. No suicidal ideation. Family history of depression.'),
        (9, 7, '2024-09-10', 'Generalized Anxiety Disorder', 'SSRI therapy, relaxation techniques', 'Escitalopram 10mg OD, Progressive muscle relaxation', 'Excessive worry, restlessness, fatigue for 6 months. GAD-7 score: 18. Panic attacks twice weekly. Caffeine restriction advised.'),
        (9, 7, '2024-07-05', 'Adjustment Disorder with Mixed Anxiety and Depression', 'Supportive psychotherapy, short-term anxiolytic', 'Lorazepam 0.5mg SOS, Counseling sessions', 'Emotional distress following job loss 2 months ago. Sleep disturbance, irritability. No previous psychiatric history. Stress management techniques taught.'),
        (9, 7, '2024-04-15', 'Alcohol Use Disorder (Mild)', 'Motivational interviewing, naltrexone', 'Naltrexone 50mg OD, Thiamine 100mg OD', 'Increased alcohol consumption for 1 year. AUDIT score: 12. No withdrawal symptoms. Liver function tests normal. Alcoholics Anonymous referral.'),
        (9, 7, '2024-01-10', 'Insomnia (Chronic)', 'Sleep hygiene, short-term hypnotic', 'Zolpidem 5mg at bedtime for 2 weeks, Sleep hygiene education', 'Difficulty initiating and maintaining sleep for 4 months. Sleep latency: 2 hours. Epworth sleepiness scale: 12. Caffeine and screen time restrictions advised.'),
        
        # Riya Agarwal (Patient ID: 10) - Endocrinology Records
        (10, 12, '2024-10-22', 'Primary Hypothyroidism', 'Levothyroxine replacement therapy', 'Levothyroxine 75mcg OD on empty stomach', 'Fatigue, weight gain, cold intolerance for 6 months. TSH: 25 mIU/L, Free T4: 0.6 ng/dl. Anti-TPO antibodies positive. Hashimoto thyroiditis confirmed.'),
        (10, 12, '2024-09-05', 'Polycystic Ovary Syndrome with Metabolic Syndrome', 'Insulin sensitizer, lifestyle modification', 'Metformin 500mg BD, Atorvastatin 10mg OD', 'Irregular periods, central obesity, acanthosis nigricans. Fasting glucose: 110 mg/dl, OGTT: IGT. Lipid profile: dyslipidemia. HOMA-IR: 5.1.'),
        (10, 12, '2024-07-10', 'Vitamin D Deficiency', 'High-dose vitamin D supplementation', 'Cholecalciferol 60,000 IU weekly for 8 weeks', 'Bone pain, muscle weakness for 3 months. Serum 25(OH)D: 12 ng/ml (severe deficiency). Calcium and phosphorus normal. PTH: 85 pg/ml (elevated).'),
        (10, 12, '2024-04-20', 'Prediabetes (Impaired Glucose Tolerance)', 'Lifestyle intervention, metformin', 'Metformin 500mg BD, Dietary counseling', 'Family history of diabetes. BMI: 27 kg/m². OGTT: fasting 105 mg/dl, 2-hour 155 mg/dl. HbA1c: 6.2%. Diabetes prevention program enrolled.'),
        (10, 12, '2024-01-15', 'Subclinical Hypothyroidism', 'Monitoring, no treatment', 'Recheck thyroid function in 3 months', 'Routine screening. TSH: 8.5 mIU/L, Free T4: 1.2 ng/dl (normal). No symptoms. Anti-TPO antibodies negative. Close monitoring advised.'),
        
        # Siddharth Kapoor (Patient ID: 11) - Comprehensive Hematology & General Medicine Records
        (11, 5, '2024-11-03', 'Iron Deficiency Anemia (Severe) with Gastrointestinal Bleeding', 'Parenteral iron therapy, upper GI endoscopy', 'Iron sucrose 200mg IV weekly x 5 doses, Pantoprazole 40mg BD, Sucralfate 1g QID', 'Severe fatigue, pallor, melena for 2 months. Hemoglobin: 6.8 g/dl, MCV: 62 fl, Serum ferritin: 8 ng/ml. Stool occult blood positive. Upper GI endoscopy shows duodenal ulcer with active bleeding. Blood transfusion 2 units given.'),
        (11, 5, '2024-09-20', 'Chronic Kidney Disease Stage 3A', 'ACE inhibitor, phosphate binders, dietary counseling', 'Enalapril 5mg BD, Calcium carbonate 500mg TDS, Sodium bicarbonate 500mg BD', 'Hypertension, proteinuria, pedal edema for 1 year. Serum creatinine: 2.1 mg/dl, eGFR: 35 ml/min. Urine protein: 2+ persistent. Ultrasound: bilateral medical renal disease. Nephrology follow-up scheduled.'),
        (11, 5, '2024-08-15', 'Hypertensive Crisis', 'Antihypertensive therapy, cardiac evaluation', 'Amlodipine 10mg OD, Telmisartan 80mg OD, Metoprolol 50mg BD', 'Severe headache, blurred vision, BP: 220/120 mmHg. Fundoscopy: Grade III hypertensive retinopathy. 2D Echo: LVH with diastolic dysfunction. Gradual BP reduction achieved.'),
        (11, 5, '2024-06-10', 'Type 2 Diabetes Mellitus with Diabetic Nephropathy', 'Insulin therapy, ACE inhibitor', 'Human insulin 30/70 mix 20 units BD, Enalapril 5mg BD', 'Polyuria, polydipsia, weight loss for 3 months. FBS: 280 mg/dl, HbA1c: 11.2%. Microalbuminuria: 150 mg/g creatinine. Diabetic diet counseling provided.'),
        (11, 5, '2024-03-25', 'Acute Coronary Syndrome (NSTEMI)', 'Dual antiplatelet therapy, statin', 'Aspirin 75mg + Clopidogrel 75mg OD, Atorvastatin 80mg OD, Metoprolol 25mg BD', 'Chest pain at rest for 6 hours. ECG: T-wave inversions in V4-V6. Troponin I: 8.5 ng/ml. 2D Echo: regional wall motion abnormality. Coronary angiography planned.'),
        
        # Ishita Bansal (Patient ID: 12) - Comprehensive Cardiology Records
        (12, 1, '2024-11-01', 'Rheumatic Heart Disease with Severe Mitral Stenosis', 'Balloon mitral valvotomy, anticoagulation', 'Warfarin 5mg OD (target INR 2-3), Benzathine penicillin 1.2 MU IM monthly, Furosemide 40mg OD', 'History of rheumatic fever at age 12. Progressive dyspnea NYHA Class III for 2 years. Echo: severe mitral stenosis, valve area 0.8 cm². Left atrial enlargement. Successful balloon valvotomy performed. Post-procedure valve area: 1.8 cm².'),
        (12, 1, '2024-09-15', 'Atrial Fibrillation with Rapid Ventricular Response', 'Rate control, anticoagulation, cardioversion', 'Digoxin 0.25mg OD, Metoprolol 50mg BD, Warfarin as per INR', 'Palpitations, breathlessness for 1 week. ECG: atrial fibrillation, ventricular rate 140/min. CHA2DS2-VASc score: 4. DC cardioversion performed. Sinus rhythm restored.'),
        (12, 1, '2024-07-20', 'Congestive Heart Failure (NYHA Class II)', 'Diuretics, ACE inhibitor, beta-blocker', 'Furosemide 40mg OD, Enalapril 5mg BD, Carvedilol 3.125mg BD', 'Pedal edema, orthopnea for 3 months. 2D Echo: dilated left atrium, EF: 55%. BNP: 680 pg/ml. Chest X-ray: cardiomegaly, pulmonary congestion.'),
        (12, 1, '2024-05-10', 'Infective Endocarditis (Mitral Valve)', 'Antibiotic therapy, echocardiographic monitoring', 'Penicillin G 4 MU IV QID + Gentamicin 80mg IV BD for 6 weeks', 'Fever, new murmur, splinter hemorrhages for 2 weeks. Blood culture: Streptococcus viridans. TEE: mitral valve vegetation 8mm. Duke criteria: definite endocarditis.'),
        (12, 1, '2024-02-28', 'Pulmonary Hypertension (Secondary)', 'Pulmonary vasodilator therapy', 'Sildenafil 25mg TDS, Bosentan 62.5mg BD', 'Progressive breathlessness, chest pain on exertion. Right heart catheterization: mean PAP 45 mmHg. 6-minute walk test: 280 meters. WHO functional class III.'),
        
        # Aarav Chopra (Patient ID: 13) - Comprehensive Infectious Disease & General Medicine Records
        (13, 5, '2024-10-28', 'Enteric Fever (Typhoid) with Complications', 'IV antibiotic therapy, supportive care', 'Ceftriaxone 2g IV OD for 10 days, Dexamethasone 8mg IV TDS for 3 days', 'High-grade fever, altered sensorium, abdominal distension for 10 days. Widal test: TO 1:640, TH 1:320. Blood culture: S. typhi (sensitive to ceftriaxone). Complications: typhoid encephalopathy, hepatomegaly.'),
        (13, 5, '2024-08-15', 'Acute Viral Hepatitis E with Acute Liver Failure', 'Intensive monitoring, supportive management', 'Ursodeoxycholic acid 300mg BD, Lactulose 30ml TDS, Vitamin K 10mg IV', 'Jaundice, confusion, bleeding tendency for 2 weeks. HEV IgM positive. Bilirubin: 25 mg/dl, ALT: 1200 U/L, INR: 2.8. Hepatic encephalopathy Grade II. Liver transplant evaluation.'),
        (13, 5, '2024-06-20', 'Scrub Typhus', 'Doxycycline therapy, supportive care', 'Doxycycline 100mg BD for 7 days, Paracetamol 650mg TDS', 'Fever, headache, myalgia, eschar on thigh for 1 week. IgM ELISA for Orientia tsutsugamushi positive. Platelet count: 80,000/μl. Good response to doxycycline.'),
        (13, 5, '2024-04-10', 'Leptospirosis (Weil Disease)', 'Penicillin therapy, dialysis support', 'Penicillin G 1.5 MU IV QID for 7 days, Hemodialysis', 'Fever, jaundice, oliguria following flood exposure. Leptospira IgM positive. Creatinine: 8.5 mg/dl, Bilirubin: 15 mg/dl. Acute kidney injury requiring dialysis.'),
        (13, 5, '2024-01-15', 'Chikungunya Fever with Polyarthritis', 'Symptomatic treatment, physiotherapy', 'Paracetamol 650mg TDS, Diclofenac 50mg BD, Physiotherapy', 'Fever, severe joint pains for 1 week. Chikungunya IgM positive. Polyarthritis involving wrists, ankles, knees. Chronic phase arthritis developed.'),
        
        # Kavya Menon (Patient ID: 14) - Comprehensive Dermatology Records
        (14, 6, '2024-11-02', 'Vitiligo (Generalized) with Thyroid Association', 'Topical immunomodulators, phototherapy, thyroid treatment', 'Tacrolimus 0.1% ointment BD, NB-UVB therapy 3x/week, Levothyroxine 50mcg OD', 'Progressive depigmented patches for 3 years involving face, hands, feet (30% BSA). Wood lamp: chalk-white fluorescence. Thyroid function: TSH 12 mIU/L, Anti-TPO positive. Associated autoimmune thyroiditis.'),
        (14, 6, '2024-09-10', 'Alopecia Areata (Extensive)', 'Systemic corticosteroids, topical immunotherapy', 'Prednisolone 40mg OD tapering over 8 weeks, Diphenylcyclopropenone (DPCP) sensitization', 'Sudden extensive hair loss (60% scalp) over 3 months. Pull test positive. Dermoscopy: exclamation mark hairs, black dots. Nail pitting present. Psychological counseling provided.'),
        (14, 6, '2024-07-05', 'Systemic Lupus Erythematosus (Cutaneous)', 'Antimalarials, topical corticosteroids', 'Hydroxychloroquine 400mg OD, Clobetasol 0.05% cream BD', 'Butterfly rash, photosensitivity, oral ulcers for 6 months. ANA positive (1:320, homogeneous), Anti-dsDNA positive. Skin biopsy: interface dermatitis. Ophthalmology clearance for HCQ.'),
        (14, 6, '2024-04-20', 'Pemphigus Vulgaris', 'Systemic immunosuppression', 'Prednisolone 60mg OD, Azathioprine 100mg OD, Topical clobetasol', 'Painful oral ulcers, flaccid bullae on trunk for 2 months. Nikolsky sign positive. Skin biopsy: intraepidermal bulla. Direct immunofluorescence: IgG intercellular deposits.'),
        (14, 6, '2024-01-30', 'Chronic Urticaria with Angioedema', 'Antihistamines, leukotriene antagonist', 'Cetirizine 10mg BD, Montelukast 10mg OD, Prednisolone 20mg OD for 1 week', 'Daily wheals and facial swelling for 8 weeks. Autologous serum skin test positive. Thyroid function normal. Chronic spontaneous urticaria diagnosed.'),
        
        # Aryan Sinha (Patient ID: 15) - Comprehensive Neurology Records
        (15, 4, '2024-10-25', 'Generalized Tonic-Clonic Epilepsy with Status Epilepticus', 'Antiepileptic drugs, ICU management', 'Phenytoin 300mg OD, Levetiracetam 1000mg BD, Lorazepam 4mg IV stat', 'Prolonged seizure lasting 45 minutes. EEG: continuous seizure activity. Phenytoin level subtherapeutic (8 mcg/ml). Status epilepticus managed with IV lorazepam and phenytoin loading. Seizure control achieved.'),
        (15, 4, '2024-08-15', 'Post-stroke Hemiparesis with Spasticity', 'Antispasticity agents, physiotherapy', 'Baclofen 10mg TDS, Aspirin 75mg + Clopidogrel 75mg OD, Physiotherapy', 'Left MCA stroke 8 months ago. Right hemiparesis with spasticity (Modified Ashworth Scale: 3). MRI: chronic infarct. Botulinum toxin injection planned for spasticity.'),
        (15, 4, '2024-06-10', 'Migraine with Medication Overuse Headache', 'Withdrawal therapy, prophylaxis', 'Topiramate 50mg BD, Amitriptyline 25mg HS, Gradual analgesic withdrawal', 'Daily headaches for 6 months, overusing analgesics (>15 days/month). Headache diary shows medication overuse pattern. Withdrawal symptoms managed with supportive care.'),
        (15, 4, '2024-03-20', 'Peripheral Neuropathy (Diabetic)', 'Neuropathic pain management, glycemic control', 'Pregabalin 150mg BD, Methylcobalamin 1500mcg OD, Insulin optimization', 'Burning feet, numbness for 1 year. Diabetes for 10 years, poor control. NCS: sensorimotor axonal neuropathy. Vibration sense absent. Diabetic foot care education.'),
        (15, 4, '2024-01-05', 'Transient Ischemic Attack', 'Antiplatelet therapy, risk factor modification', 'Aspirin 75mg + Clopidogrel 75mg OD, Atorvastatin 40mg OD', 'Sudden onset right-sided weakness, speech difficulty lasting 2 hours. Complete recovery within 24 hours. MRI: no acute infarct. Carotid Doppler: 40% stenosis. ABCD2 score: 5.'),
        
        # Diya Verma (Patient ID: 16) - Comprehensive Pulmonology Records
        (16, 11, '2024-11-01', 'Pulmonary Tuberculosis (MDR-TB)', 'Second-line anti-TB therapy', 'Bedaquiline 400mg OD x 2 weeks then 200mg TIW, Linezolid 600mg OD, Levofloxacin 750mg OD, Cycloserine 500mg BD', 'Productive cough, hemoptysis, weight loss for 3 months. Previous ATT failure. Gene Xpert: MTB detected, rifampicin resistant. Drug susceptibility: resistant to INH, RIF. Sputum culture: M. tuberculosis (MDR).'),
        (16, 11, '2024-08-20', 'Pleural Effusion (Tuberculous) with Empyema', 'Chest tube drainage, anti-TB therapy', 'ATT as per DOTS protocol, Chest tube insertion, Prednisolone 40mg OD', 'Right-sided chest pain, fever, breathlessness for 4 weeks. Chest X-ray: massive right pleural effusion. Pleural fluid: pus, ADA >100 U/L. Pleural biopsy: caseating granulomas. Chest tube drainage 1.2L pus.'),
        (16, 11, '2024-06-15', 'Pneumothorax (Spontaneous) Secondary to TB', 'Chest tube insertion, pleurodesis', 'Chest tube insertion, Chemical pleurodesis with talc', 'Sudden onset breathlessness, chest pain. Chest X-ray: 60% right pneumothorax. History of pulmonary TB. CT chest: underlying lung fibrosis, blebs. Recurrent pneumothorax prevented with pleurodesis.'),
        (16, 11, '2024-04-10', 'Chronic Obstructive Pulmonary Disease (GOLD Stage III)', 'Bronchodilator therapy, pulmonary rehabilitation', 'Tiotropium 18mcg OD, Formoterol + Budesonide 12/400 BD, Theophylline 200mg BD', 'Progressive breathlessness for 3 years. Smoking: 30 pack-years. Spirometry: FEV1 40% predicted, FEV1/FVC: 0.55. mMRC grade 3 dyspnea. Pulmonary rehabilitation enrolled.'),
        (16, 11, '2024-01-25', 'Lung Cancer (Adenocarcinoma) Stage IIIA', 'Chemotherapy, radiation therapy', 'Carboplatin + Paclitaxel chemotherapy, Concurrent radiotherapy', 'Persistent cough, weight loss, hemoptysis for 2 months. CT chest: right upper lobe mass 4cm, mediastinal lymphadenopathy. Bronchoscopy biopsy: adenocarcinoma. PET scan: Stage IIIA. Oncology referral.'),
        
        # Nikhil Pandey (Patient ID: 17) - Comprehensive Infectious Disease & General Medicine Records
        (17, 5, '2024-10-30', 'Plasmodium Falciparum Malaria (Severe)', 'Artesunate therapy, intensive monitoring', 'Artesunate 2.4mg/kg IV stat then 2.4mg/kg at 12, 24 hours, Doxycycline 100mg BD', 'High-grade fever, altered sensorium, oliguria for 3 days. Peripheral smear: P. falciparum (parasitemia 8%). Cerebral malaria, acute kidney injury. ICU admission. Rapid recovery with artesunate.'),
        (17, 5, '2024-08-25', 'Acute Gastroenteritis (Cholera)', 'Aggressive rehydration, antibiotic therapy', 'ORS 2L over 4 hours, Doxycycline 300mg stat then 100mg BD for 3 days', 'Profuse watery diarrhea (rice-water stools) 15-20 times/day, vomiting, severe dehydration. Stool culture: Vibrio cholerae O1. Rapid stool antigen positive. Severe dehydration corrected with ORS.'),
        (17, 5, '2024-06-15', 'Japanese Encephalitis', 'Supportive care, antiviral therapy', 'Acyclovir 10mg/kg IV TDS for 10 days, Mannitol 100ml IV QID', 'Fever, headache, altered sensorium, seizures for 5 days. CSF: lymphocytic pleocytosis. JE IgM positive. MRI brain: thalamic hyperintensities. Neurological sequelae: memory impairment.'),
        (17, 5, '2024-04-05', 'Kala-azar (Visceral Leishmaniasis)', 'Amphotericin B therapy', 'Liposomal Amphotericin B 3mg/kg IV on days 1-5, 14, 21', 'Prolonged fever, splenomegaly, pancytopenia for 2 months. rK39 antigen positive. Bone marrow: LD bodies seen. Splenic aspiration: Leishmania donovani. Complete cure achieved.'),
        (17, 5, '2024-01-20', 'Rickettsial Fever (Indian Tick Typhus)', 'Doxycycline therapy', 'Doxycycline 100mg BD for 7 days, Supportive care', 'Fever, headache, myalgia, eschar on leg for 1 week. Weil-Felix test: OX-2 positive (1:320). Good response to doxycycline. Rural area exposure history positive.'),
        
        # Aditi Saxena (Patient ID: 18) - Comprehensive Gynecology & Urology Records
        (18, 8, '2024-11-03', 'Pelvic Inflammatory Disease (Chronic)', 'Antibiotic therapy, pain management', 'Doxycycline 100mg BD + Metronidazole 400mg BD for 14 days, Ibuprofen 400mg TDS', 'Chronic pelvic pain, dyspareunia, irregular bleeding for 6 months. Pelvic examination: cervical motion tenderness, adnexal mass. Ultrasound: tubo-ovarian complex. Chlamydia PCR positive.'),
        (18, 8, '2024-09-20', 'Recurrent Urinary Tract Infection with Pyelonephritis', 'IV antibiotic therapy, prophylaxis', 'Ceftriaxone 1g IV BD for 7 days, then Nitrofurantoin 50mg HS for 6 months', 'Fifth UTI episode with fever, flank pain. Urine culture: E. coli (ESBL producer). IVU: mild hydronephrosis. Cystoscopy normal. Immunological workup normal.'),
        (18, 8, '2024-07-15', 'Endometriosis (Ovarian)', 'Hormonal suppression, laparoscopic surgery', 'GnRH agonist (Leuprolide) 3.75mg IM monthly, Laparoscopic cystectomy', 'Severe dysmenorrhea, chronic pelvic pain for 2 years. MRI pelvis: bilateral endometriomas (chocolate cysts). CA-125: 85 U/ml. Laparoscopic excision performed.'),
        (18, 8, '2024-05-10', 'Bacterial Vaginosis with Candidiasis (Mixed)', 'Antifungal and antibiotic therapy', 'Fluconazole 150mg stat, Metronidazole 400mg BD for 7 days', 'Vaginal discharge, itching, dysuria for 2 weeks. Wet mount: clue cells, budding yeast. Whiff test positive. pH: 5.5. Mixed infection treated successfully.'),
        (18, 8, '2024-02-28', 'Cervical Intraepithelial Neoplasia (CIN II)', 'Loop electrosurgical excision procedure (LEEP)', 'LEEP procedure, HPV vaccination', 'Abnormal Pap smear: HSIL. Colposcopy: acetowhite lesions. Biopsy: CIN II. HPV 16 positive. LEEP performed with clear margins. Follow-up Pap smears scheduled.'),
        
        # Harsh Tiwari (Patient ID: 19) - Comprehensive Orthopedics Records
        (19, 3, '2024-10-28', 'Osteoporotic Vertebral Compression Fractures (Multiple)', 'Vertebroplasty, bisphosphonate therapy', 'Alendronate 70mg weekly, Calcium 1000mg + Vitamin D3 800 IU BD, Vertebroplasty T12, L1', 'Severe back pain following minor trauma. MRI: acute compression fractures T12, L1 with 50% height loss. DEXA: T-score -3.5 (severe osteoporosis). Bilateral vertebroplasty performed with cement augmentation.'),
        (19, 3, '2024-08-15', 'Bilateral Hip Osteoarthritis (End-stage)', 'Total hip replacement (staged)', 'Right total hip replacement, Celecoxib 200mg OD, Physiotherapy', 'Severe bilateral hip pain, limping for 5 years. X-ray: complete joint space loss, subchondral sclerosis. Harris Hip Score: 35. Right THR performed. Left THR planned after 6 months.'),
        (19, 3, '2024-06-10', 'Rheumatoid Arthritis with Joint Deformities', 'Disease-modifying therapy, biologics', 'Methotrexate 15mg weekly, Folic acid 5mg weekly, Adalimumab 40mg SC fortnightly', 'Symmetrical polyarthritis for 10 years. Swan neck deformities, ulnar deviation. RF positive, Anti-CCP positive. DAS28 score: 6.2 (high activity). Biologic therapy initiated.'),
        (19, 3, '2024-03-25', 'Lumbar Spinal Stenosis with Neurogenic Claudication', 'Decompressive laminectomy', 'Laminectomy L3-L5, Pregabalin 150mg BD, Physiotherapy', 'Bilateral leg pain, numbness on walking 100 meters for 2 years. MRI: severe central stenosis L3-L5. Neurogenic claudication confirmed. Multilevel decompression performed.'),
        (19, 3, '2024-01-10', 'Frozen Shoulder (Adhesive Capsulitis)', 'Intra-articular steroid injection, physiotherapy', 'Triamcinolone 40mg intra-articular injection, Intensive physiotherapy', 'Progressive shoulder stiffness, pain for 8 months. ROM severely restricted (flexion 60°, abduction 45°). MRI: capsular thickening. Stage 2 adhesive capsulitis. Good response to injection.'),
        
        # Nisha Bhatt (Patient ID: 20) - Comprehensive Obstetrics & Endocrinology Records
        (20, 12, '2024-11-05', 'Gestational Diabetes Mellitus (32 weeks) with Macrosomia', 'Insulin therapy, fetal monitoring, delivery planning', 'Human insulin Regular 8 units + NPH 12 units BD, Fetal biophysical profile weekly', 'OGTT abnormal at 24 weeks. Poor glycemic control on diet. Fasting: 110 mg/dl, PPBS: 180 mg/dl. Ultrasound: EFW 2.8 kg (>95th percentile). Insulin initiated. Delivery planned at 38 weeks.'),
        (20, 12, '2024-09-20', 'Pregnancy-Induced Hypertension (28 weeks)', 'Antihypertensive therapy, fetal surveillance', 'Methyldopa 250mg TDS, Aspirin 75mg OD, Bed rest', 'BP: 150/95 mmHg on routine antenatal visit. No proteinuria. Fundoscopy normal. 24-hour urine protein: 200mg. Fetal Doppler studies normal. Close monitoring for preeclampsia.'),
        (20, 12, '2024-07-15', 'Hypothyroidism in Pregnancy (20 weeks)', 'Levothyroxine optimization', 'Levothyroxine 100mcg OD (increased from 75mcg)', 'Routine thyroid screening. TSH: 4.5 mIU/L (elevated for pregnancy). Free T4: 1.0 ng/dl. Pre-pregnancy hypothyroidism. Dose increased. Target TSH <2.5 mIU/L in pregnancy.'),
        (20, 12, '2024-05-10', 'Threatened Abortion (12 weeks)', 'Bed rest, progesterone support', 'Micronized progesterone 200mg BD vaginally, Bed rest, Folic acid 5mg OD', 'Vaginal spotting for 2 days at 12 weeks gestation. Pelvic examination: closed cervix. Ultrasound: viable fetus, appropriate growth. Subchorionic hematoma noted. Bleeding stopped with treatment.'),
        (20, 12, '2024-02-28', 'Polycystic Ovary Syndrome with Infertility', 'Ovulation induction, lifestyle modification', 'Clomiphene citrate 50mg OD (days 2-6), Metformin 500mg BD', 'Primary infertility for 2 years. Irregular cycles, hirsutism. Ultrasound: bilateral polycystic ovaries. AMH: 8.5 ng/ml. Ovulation induction cycles. Conceived after 3 cycles.'),
        
        # Manish Kumar (Patient ID: 21) - Comprehensive General Medicine & Gastroenterology Records
        (21, 5, '2024-11-04', 'Inflammatory Bowel Disease (Ulcerative Colitis)', 'Immunosuppressive therapy, colonoscopy monitoring', 'Mesalamine 800mg TDS, Prednisolone 40mg OD tapering, Azathioprine 100mg OD', 'Bloody diarrhea, abdominal pain for 3 months. Colonoscopy: pancolitis with ulcerations. Biopsy: chronic inflammatory changes. Mayo score: 8 (moderate-severe). Steroid induction therapy initiated.'),
        (21, 5, '2024-09-20', 'Chronic Liver Disease (NASH Cirrhosis)', 'Hepatoprotective therapy, lifestyle modification', 'Ursodeoxycholic acid 300mg BD, Vitamin E 400 IU OD, Lactulose 30ml BD', 'Fatigue, abdominal distension for 6 months. LFT: elevated transaminases. Ultrasound: coarse echotexture, ascites. Fibroscan: F4 fibrosis. Child-Pugh Class B. Alcohol cessation counseling.'),
        (21, 5, '2024-07-15', 'Portal Hypertension with Esophageal Varices', 'Beta-blocker prophylaxis, endoscopic surveillance', 'Propranolol 40mg BD, Pantoprazole 40mg OD', 'Upper GI bleeding episode. Emergency endoscopy: Grade II esophageal varices with red signs. Band ligation performed. Secondary prophylaxis with propranolol initiated.'),
        (21, 5, '2024-05-10', 'Hepatic Encephalopathy Grade II', 'Lactulose therapy, protein restriction', 'Lactulose 30ml QID, Rifaximin 400mg BD, Low protein diet', 'Confusion, asterixis, altered sleep pattern. Ammonia level: 85 μmol/L (elevated). West Haven criteria: Grade II. Precipitating factor: constipation. Good response to lactulose.'),
        (21, 5, '2024-02-25', 'Spontaneous Bacterial Peritonitis', 'Antibiotic therapy, albumin infusion', 'Ceftriaxone 2g IV OD for 5 days, Albumin 1.5g/kg IV', 'Fever, abdominal pain, worsening ascites. Ascitic fluid: neutrophils >250/μl. Culture: E. coli sensitive to ceftriaxone. Complete resolution with treatment.'),
        
        # Pooja Sharma (Patient ID: 22) - Comprehensive Gynecology & Obstetrics Records
        (22, 8, '2024-11-02', 'Endometrial Hyperplasia (Complex with Atypia)', 'Hormonal therapy, hysteroscopic evaluation', 'Megestrol acetate 160mg OD, Hysteroscopic guided biopsy', 'Heavy menstrual bleeding, postmenopausal bleeding. Endometrial thickness: 18mm. Biopsy: complex hyperplasia with atypia. High risk for malignancy. Hysterectomy counseling provided.'),
        (22, 8, '2024-09-15', 'Uterine Fibroids (Multiple Intramural)', 'Medical management, MRI monitoring', 'GnRH agonist (Leuprolide) 3.75mg IM monthly, Iron supplements', 'Menorrhagia, pelvic pressure for 8 months. MRI pelvis: multiple intramural fibroids, largest 8cm. Hemoglobin: 7.8 g/dl. Medical management trial before surgery.'),
        (22, 8, '2024-07-20', 'Ovarian Cyst (Dermoid) with Torsion', 'Emergency laparoscopic cystectomy', 'Laparoscopic right ovarian cystectomy, Postoperative analgesics', 'Acute severe pelvic pain for 6 hours. Ultrasound: 6cm right ovarian cyst with absent flow. Emergency laparoscopy: ovarian torsion with dermoid cyst. Detorsion and cystectomy performed.'),
        (22, 8, '2024-05-05', 'Pelvic Inflammatory Disease (Chronic)', 'Antibiotic therapy, partner treatment', 'Doxycycline 100mg BD + Metronidazole 400mg BD for 14 days', 'Chronic pelvic pain, dyspareunia for 4 months. Pelvic examination: adnexal tenderness, cervical motion tenderness. Chlamydia PCR positive. Partner treatment advised.'),
        (22, 8, '2024-01-30', 'Cervical Dysplasia (CIN III)', 'LEEP procedure, HPV testing', 'LEEP procedure, HPV vaccination series', 'Abnormal Pap smear: HSIL. Colposcopy: dense acetowhite lesions. Biopsy: CIN III (carcinoma in situ). HPV 16/18 positive. LEEP performed with clear margins.'),
        
        # Amit Verma (Patient ID: 23) - Comprehensive Cardiology & Interventional Records
        (23, 1, '2024-11-01', 'ST-Elevation Myocardial Infarction (Anterior Wall)', 'Primary PCI, dual antiplatelet therapy', 'Aspirin 75mg + Clopidogrel 75mg OD, Atorvastatin 80mg OD, Metoprolol 25mg BD', 'Severe chest pain for 2 hours. ECG: ST elevation V1-V6. Troponin I: 25 ng/ml. Emergency PCI: LAD 100% occlusion treated with DES. Door-to-balloon time: 45 minutes.'),
        (23, 1, '2024-08-20', 'Cardiogenic Shock', 'Inotropic support, IABP insertion', 'Dobutamine 10mcg/kg/min, IABP support, Furosemide 40mg IV BD', 'Post-MI cardiogenic shock. BP: 80/50 mmHg, CI: 1.8 L/min/m². 2D Echo: severe LV dysfunction, EF: 25%. IABP inserted. Gradual weaning after 72 hours.'),
        (23, 1, '2024-06-15', 'Ventricular Tachycardia (Sustained)', 'Antiarrhythmic therapy, ICD implantation', 'Amiodarone 200mg BD, ICD implantation', 'Palpitations, syncope. Holter: sustained VT episodes. EPS: inducible VT. ICD implanted for secondary prevention. No inappropriate shocks at follow-up.'),
        (23, 1, '2024-04-10', 'Heart Failure with Reduced Ejection Fraction', 'Guideline-directed medical therapy', 'Enalapril 10mg BD, Carvedilol 6.25mg BD, Spironolactone 25mg OD', 'NYHA Class III symptoms. 2D Echo: global hypokinesia, EF: 30%. BNP: 850 pg/ml. Optimal medical therapy initiated. Cardiac rehabilitation enrolled.'),
        (23, 1, '2024-01-25', 'Coronary Artery Disease (Triple Vessel)', 'CABG surgery, postoperative care', 'CABG (LIMA-LAD, SVG-RCA, SVG-OM), Dual antiplatelet therapy', 'Chronic stable angina, positive stress test. Coronary angiography: triple vessel disease. SYNTAX score: 28. CABG performed. Postoperative course uneventful.'),
        
        # Neha Singh (Patient ID: 24) - Comprehensive Endocrinology & Metabolism Records
        (24, 12, '2024-10-30', 'Type 1 Diabetes Mellitus with Diabetic Ketoacidosis', 'Insulin therapy, electrolyte correction', 'Human insulin Regular IV infusion, then Multiple daily injections', 'Polyuria, polydipsia, weight loss for 2 weeks. Blood glucose: 450 mg/dl, pH: 7.1, ketones: 4+. DKA management with IV insulin. Transitioned to basal-bolus regimen.'),
        (24, 12, '2024-08-25', 'Diabetic Nephropathy (Stage 3 CKD)', 'ACE inhibitor, protein restriction', 'Enalapril 10mg BD, Protein restriction 0.8g/kg/day', 'Proteinuria, hypertension. Serum creatinine: 1.8 mg/dl, eGFR: 45 ml/min. Urine ACR: 300 mg/g. Diabetic retinopathy present. Nephrology follow-up.'),
        (24, 12, '2024-06-20', 'Diabetic Retinopathy (Proliferative)', 'Laser photocoagulation, anti-VEGF therapy', 'Panretinal photocoagulation, Bevacizumab intravitreal injection', 'Blurred vision, floaters. Fundoscopy: neovascularization, vitreous hemorrhage. Fluorescein angiography: extensive ischemia. Urgent ophthalmology intervention.'),
        (24, 12, '2024-04-15', 'Hyperthyroidism (Graves Disease)', 'Antithyroid therapy, beta-blocker', 'Carbimazole 20mg BD, Propranolol 40mg BD', 'Palpitations, weight loss, tremors for 3 months. TSH: <0.01 mIU/L, Free T4: 4.5 ng/dl. TSI positive. Thyroid scan: diffuse uptake. Remission achieved in 18 months.'),
        (24, 12, '2024-01-20', 'Addison Disease (Primary Adrenal Insufficiency)', 'Corticosteroid replacement therapy', 'Hydrocortisone 20mg morning + 10mg evening, Fludrocortisone 0.1mg OD', 'Fatigue, hyperpigmentation, salt craving. Cortisol: 2 μg/dl, ACTH: 180 pg/ml. Synacthen test: no response. Adrenal antibodies positive. Steroid replacement initiated.'),
        
        # Rahul Gupta (Patient ID: 25) - Comprehensive Nephrology & Urology Records
        (25, 5, '2024-11-03', 'Chronic Kidney Disease Stage 5 (End-stage)', 'Hemodialysis, transplant evaluation', 'Hemodialysis 3x/week, Erythropoietin 4000 IU SC weekly', 'Progressive CKD for 5 years. Serum creatinine: 8.5 mg/dl, eGFR: 8 ml/min. Uremic symptoms. Hemodialysis initiated via AV fistula. Transplant workup started.'),
        (25, 5, '2024-09-18', 'Acute Glomerulonephritis (Post-infectious)', 'Immunosuppressive therapy, supportive care', 'Prednisolone 60mg OD, Furosemide 40mg BD, ACE inhibitor', 'Hematuria, proteinuria, hypertension following URTI. Renal biopsy: acute proliferative GN. C3 low, ASO elevated. Good response to steroids.'),
        (25, 5, '2024-07-10', 'Nephrotic Syndrome (Minimal Change Disease)', 'Corticosteroid therapy, diuretics', 'Prednisolone 1mg/kg OD, Furosemide 40mg BD, Albumin infusion', 'Generalized edema, proteinuria for 6 weeks. 24-hour urine protein: 8g. Serum albumin: 1.8 g/dl. Renal biopsy: minimal change disease. Complete remission achieved.'),
        (25, 5, '2024-05-05', 'Renal Stone Disease (Recurrent Calcium Oxalate)', 'Lithotripsy, metabolic evaluation', 'ESWL, Potassium citrate 15mEq BD, Increased fluid intake', 'Severe flank pain, hematuria. CT KUB: 8mm right renal pelvis stone. ESWL performed. Stone analysis: calcium oxalate. Metabolic workup: hypercalciuria.'),
        (25, 5, '2024-02-20', 'Acute Kidney Injury (ATN)', 'Supportive care, dialysis', 'Hemodialysis, Fluid balance monitoring', 'Oliguria following sepsis. Serum creatinine: 6.2 mg/dl (baseline 1.2). Urine microscopy: muddy brown casts. Dialysis for 2 weeks. Complete recovery of renal function.'),
        
        # Swati Jain (Patient ID: 26) - Comprehensive Hematology & Oncology Records
        (26, 5, '2024-10-28', 'Acute Lymphoblastic Leukemia (B-cell ALL)', 'Chemotherapy protocol, supportive care', 'Induction chemotherapy (UKALL protocol), Allopurinol 300mg OD', 'Fever, bleeding, fatigue for 3 weeks. CBC: WBC 85,000/μl with 90% blasts. Bone marrow: B-cell ALL, Philadelphia negative. Induction chemotherapy initiated.'),
        (26, 5, '2024-08-15', 'Febrile Neutropenia', 'Broad-spectrum antibiotics, G-CSF', 'Piperacillin-tazobactam 4.5g IV TDS, Filgrastim 300mcg SC OD', 'Fever during chemotherapy cycle. ANC: 200/μl. Blood cultures pending. Empirical antibiotic therapy. Fever resolved, neutrophil recovery achieved.'),
        (26, 5, '2024-06-10', 'Tumor Lysis Syndrome', 'Aggressive hydration, rasburicase', 'Rasburicase 0.2mg/kg IV, Aggressive hydration, Allopurinol', 'Hyperuricemia, hyperkalemia post-chemotherapy. Uric acid: 15 mg/dl, K+: 6.2 mEq/L. LDH: 2500 U/L. TLS management with rasburicase. Metabolic normalization achieved.'),
        (26, 5, '2024-04-05', 'Chronic Myeloid Leukemia (Chronic Phase)', 'Tyrosine kinase inhibitor therapy', 'Imatinib 400mg OD, Regular monitoring', 'Splenomegaly, high WBC count. CBC: WBC 150,000/μl. BCR-ABL positive. Chronic phase CML. Imatinib therapy initiated. Molecular response monitoring.'),
        (26, 5, '2024-01-15', 'Iron Deficiency Anemia (Severe)', 'Iron replacement therapy, source investigation', 'Iron sucrose 200mg IV weekly, Upper and lower GI endoscopy', 'Severe fatigue, pallor. Hemoglobin: 5.2 g/dl, ferritin: 5 ng/ml. Menorrhagia history. Iron replacement therapy. Gynecology referral for menorrhagia management.'),
        
        # Vishal Yadav (Patient ID: 27) - Comprehensive Respiratory & Critical Care Records
        (27, 11, '2024-11-01', 'Acute Respiratory Distress Syndrome (ARDS)', 'Mechanical ventilation, prone positioning', 'Lung protective ventilation, Prone positioning 16h/day', 'Severe pneumonia with respiratory failure. PaO2/FiO2: 120. Bilateral infiltrates on chest X-ray. Intubated, mechanical ventilation. Prone positioning protocol. Gradual improvement.'),
        (27, 11, '2024-09-20', 'Pulmonary Embolism (Massive)', 'Thrombolytic therapy, anticoagulation', 'Alteplase 100mg IV over 2 hours, Heparin infusion', 'Sudden breathlessness, chest pain, syncope. CTPA: bilateral pulmonary emboli with RV strain. D-dimer: 5000 ng/ml. Thrombolysis performed. Clinical improvement.'),
        (27, 11, '2024-07-15', 'Interstitial Lung Disease (IPF)', 'Antifibrotic therapy, oxygen support', 'Pirfenidone 801mg TDS, Oxygen 2L/min, Pulmonary rehabilitation', 'Progressive breathlessness for 2 years. HRCT: honeycombing, traction bronchiectasis. PFT: restrictive pattern. Lung biopsy: usual interstitial pneumonia. Antifibrotic therapy.'),
        (27, 11, '2024-05-10', 'Pneumothorax (Tension)', 'Emergency chest tube insertion', 'Chest tube insertion, Underwater seal drainage', 'Sudden severe breathlessness, chest pain. Examination: absent breath sounds, tracheal deviation. Chest X-ray: complete pneumothorax. Emergency chest tube insertion. Lung re-expansion achieved.'),
        (27, 11, '2024-02-25', 'Lung Cancer (Squamous Cell Carcinoma)', 'Chemotherapy, radiation therapy', 'Carboplatin + Paclitaxel, Concurrent radiotherapy', 'Persistent cough, hemoptysis, weight loss. CT chest: right hilar mass 5cm. Bronchoscopy biopsy: squamous cell carcinoma. Stage IIIA. Concurrent chemoradiotherapy.'),
        
        # Anjali Mishra (Patient ID: 28) - Comprehensive Psychiatry & Neurology Records
        (28, 7, '2024-10-26', 'Bipolar Disorder Type I (Manic Episode)', 'Mood stabilizer therapy, antipsychotic', 'Lithium 900mg OD, Olanzapine 10mg HS, Valproate 500mg BD', 'Elevated mood, decreased sleep, grandiosity for 2 weeks. YMRS score: 28 (severe mania). Hospitalization required. Mood stabilizer combination therapy. Euthymia achieved in 6 weeks.'),
        (28, 7, '2024-08-20', 'Treatment-Resistant Depression', 'Augmentation therapy, ECT', 'Venlafaxine 225mg OD, Aripiprazole 10mg OD, ECT course', 'Persistent depression despite multiple antidepressants. HAM-D score: 24. Failed 3 adequate trials. Augmentation with aripiprazole. ECT course (12 sessions) with good response.'),
        (28, 7, '2024-06-15', 'Panic Disorder with Agoraphobia', 'SSRI therapy, CBT', 'Sertraline 100mg OD, Cognitive Behavioral Therapy', 'Recurrent panic attacks, avoidance behavior for 8 months. Panic Disorder Severity Scale: 18. Agoraphobic avoidance present. SSRI therapy with CBT. Significant improvement.'),
        (28, 7, '2024-04-10', 'Obsessive-Compulsive Disorder', 'SSRI therapy, ERP', 'Fluoxetine 60mg OD, Exposure and Response Prevention therapy', 'Contamination obsessions, washing compulsions for 2 years. Y-BOCS score: 28 (severe). Functional impairment significant. High-dose SSRI with ERP therapy. Gradual improvement.'),
        (28, 7, '2024-01-05', 'Schizoaffective Disorder (Bipolar Type)', 'Antipsychotic, mood stabilizer', 'Risperidone 4mg BD, Lithium 600mg BD', 'Psychotic symptoms with mood episodes. Auditory hallucinations, delusions during mood episodes. DSM-5 criteria met. Combination therapy with antipsychotic and mood stabilizer.'),
        
        # Suresh Pandey (Patient ID: 29) - Comprehensive Gastroenterology & Hepatology Records
        (29, 5, '2024-11-02', 'Hepatocellular Carcinoma (HCC)', 'Transarterial chemoembolization, sorafenib', 'TACE procedure, Sorafenib 400mg BD', 'Right upper quadrant pain, weight loss. CT abdomen: 6cm liver mass with arterial enhancement. AFP: 850 ng/ml. Biopsy: HCC. Barcelona Clinic Liver Cancer Stage B. TACE performed.'),
        (29, 5, '2024-09-18', 'Chronic Pancreatitis', 'Pancreatic enzyme replacement, pain management', 'Pancreatin 25,000 units with meals, Tramadol 50mg TDS', 'Chronic abdominal pain, steatorrhea for 2 years. CT abdomen: pancreatic calcifications, ductal dilatation. Fecal elastase: <100 μg/g. Diabetes mellitus developed. Enzyme replacement therapy.'),
        (29, 5, '2024-07-10', 'Acute Pancreatitis (Severe)', 'Conservative management, ICU care', 'NPO, IV fluids, Pain management, Nutritional support', 'Severe epigastric pain, vomiting. Lipase: 1200 U/L (>3x normal). CT: pancreatic necrosis 40%. Ranson score: 4. ICU management. Complications: pseudocyst formation.'),
        (29, 5, '2024-05-05', 'Crohn Disease (Ileocolonic)', 'Immunosuppressive therapy, nutritional support', 'Azathioprine 150mg OD, Mesalamine 1g TDS, Nutritional counseling', 'Diarrhea, abdominal pain, weight loss for 6 months. Colonoscopy: skip lesions, cobblestone appearance. Biopsy: transmural inflammation. CDAI score: 280. Immunosuppressive therapy.'),
        (29, 5, '2024-02-20', 'Gastrointestinal Bleeding (Upper)', 'Endoscopic therapy, PPI therapy', 'Endoscopic clipping, Pantoprazole 40mg IV BD', 'Hematemesis, melena for 2 days. Hemoglobin: 7.5 g/dl. Upper GI endoscopy: duodenal ulcer with active bleeding (Forrest Ia). Endoscopic clipping performed. Bleeding controlled.'),
        
        # Ritu Agarwal (Patient ID: 30) - Comprehensive Rheumatology & Immunology Records
        (30, 5, '2024-10-30', 'Systemic Lupus Erythematosus (Active)', 'Immunosuppressive therapy, hydroxychloroquine', 'Prednisolone 40mg OD, Mycophenolate 1g BD, Hydroxychloroquine 400mg OD', 'Malar rash, arthritis, proteinuria for 3 months. ANA: 1:640 (homogeneous), Anti-dsDNA: 180 IU/ml. Complement low. SLEDAI score: 12. Active lupus nephritis Class IV.'),
        (30, 5, '2024-08-25', 'Lupus Nephritis (Class IV)', 'Pulse cyclophosphamide, plasmapheresis', 'Cyclophosphamide 750mg/m² IV monthly, Plasmapheresis', 'Rapidly progressive renal failure. Serum creatinine: 3.2 mg/dl, proteinuria: 6g/day. Renal biopsy: Class IV lupus nephritis. Pulse cyclophosphamide therapy. Plasmapheresis for severe disease.'),
        (30, 5, '2024-06-20', 'Antiphospholipid Syndrome', 'Anticoagulation therapy', 'Warfarin 5mg OD (target INR 2-3), Aspirin 75mg OD', 'Recurrent thrombosis, pregnancy losses. Anticardiolipin antibodies positive, Lupus anticoagulant positive. Deep vein thrombosis. Long-term anticoagulation initiated.'),
        (30, 5, '2024-04-15', 'Sjögren Syndrome', 'Symptomatic treatment, immunosuppression', 'Artificial tears, Pilocarpine 5mg QID, Methotrexate 15mg weekly', 'Dry eyes, dry mouth for 18 months. Schirmer test: <5mm. Salivary gland biopsy: lymphocytic infiltration. Anti-Ro/SSA positive. Sicca symptoms management.'),
        (30, 5, '2024-01-10', 'Rheumatoid Arthritis (Seropositive)', 'DMARD therapy, biologic agent', 'Methotrexate 20mg weekly, Adalimumab 40mg SC fortnightly', 'Symmetrical polyarthritis for 8 months. RF positive, Anti-CCP positive. DAS28 score: 6.8 (high activity). Erosions on X-ray. DMARD therapy with biologic agent.')
    ]
    
    insert_records_query = """
    INSERT INTO medical_records (patient_id, doctor_id, visit_date, diagnosis, treatment, prescription, notes)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.executemany(insert_records_query, records_data)
    print(f"✅ {len(records_data)} sample medical records inserted")

def display_database_summary(cursor):
    """Display database summary"""
    print("\n📊 DATABASE SUMMARY:")
    print("=" * 50)
    
    # Count records in each table
    tables = ['patients', 'doctors', 'appointments', 'medical_records', 'rooms']
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"📋 {table.capitalize()}: {count} records")
    
    print("\n🏥 SAMPLE DATA PREVIEW:")
    print("-" * 30)
    
    # Show sample patients
    cursor.execute("SELECT patient_id, first_name, last_name, phone FROM patients LIMIT 5")
    patients = cursor.fetchall()
    print("\n👥 Sample Patients:")
    for patient in patients:
        print(f"  ID: {patient[0]} - {patient[1]} {patient[2]} ({patient[3]})")
    
    # Show sample doctors
    cursor.execute("SELECT doctor_id, first_name, last_name, specialization FROM doctors LIMIT 5")
    doctors = cursor.fetchall()
    print("\n👨‍⚕️ Sample Doctors:")
    for doctor in doctors:
        print(f"  ID: {doctor[0]} - Dr. {doctor[1]} {doctor[2]} ({doctor[3]})")
    
    # Show today's appointments
    cursor.execute("""
        SELECT a.appointment_time, p.first_name, p.last_name, d.first_name, d.last_name, a.status
        FROM appointments a
        JOIN patients p ON a.patient_id = p.patient_id
        JOIN doctors d ON a.doctor_id = d.doctor_id
        WHERE a.appointment_date = CURDATE()
        ORDER BY a.appointment_time
    """)
    appointments = cursor.fetchall()
    print(f"\n📅 Today's Appointments ({len(appointments)}):")
    for apt in appointments:
        print(f"  {apt[0]} - {apt[1]} {apt[2]} with Dr. {apt[3]} {apt[4]} ({apt[5]})")

if __name__ == "__main__":
    print("🏥 Creating Hospital Management Database...")
    print("=" * 50)
    create_complete_database()
`

---


## README.md

### Project README

`markdown
# Hospital Management System

A comprehensive hospital management system built with Python, Streamlit, and MySQL.

## Features

- 📊 Dashboard with key metrics
- 👥 Patient Management (registration, search, details)
- 👨‍⚕️ Doctor Management
- 📅 Appointment Scheduling
- 📋 Medical Records
- 🏨 Room & Admission Management
- 💰 Billing & Payments
- 📦 Inventory Management
- 📈 Reports & Analytics

## Setup Instructions

### Prerequisites
- Python 3.7+
- MySQL Server
- Git

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd hospital-management-system
```

2. Create virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Setup MySQL Database:
   - Create database named `hospital_management`
   - Update credentials in `config.py` and `app.py`

5. Test database connection:
```bash
python test_db_connection.py
```

6. Create database with sample data:
```bash
python create_hospital_database.py
```

7. Run the application (choose one):

### 🏆 **Recommended: Flask + Tkinter** (Best Performance)
```bash
# Terminal 1: Start Flask API server
python flask_app.py

# Terminal 2: Start Tkinter GUI  
python tkinter_flask_gui.py
```

### 🌐 **Web Interface: Streamlit**
```bash
streamlit run app.py
```

### 🖥️ **Simple Desktop: Direct Tkinter**
```bash
python working_gui.py
```

## Configuration

Update database credentials in:
- `config.py` - Main configuration
- `app.py` - Streamlit app configuration
- `test_db_connection.py` - Connection test

## Usage

### Flask + Tkinter (Recommended)
1. Start Flask server: `python flask_app.py`
2. Start GUI: `python tkinter_flask_gui.py`
3. Use sample Patient IDs (1-16) for testing appointments
4. See `USAGE_INSTRUCTIONS.md` for detailed guide

### Streamlit Web Interface
1. Start with: `streamlit run app.py`
2. Navigate to `http://localhost:8501`
3. Use the sidebar to access different modules

### Sample Data for Testing
- **Patient IDs**: 1-16 (e.g., Patient ID 1 = John Doe)
- **Doctor IDs**: 1-10 (e.g., Dr. John Smith - Cardiology)
- Use "✓ Validate" button in appointment booking to verify Patient IDs

## Database Schema

The system uses the following main tables:
- `patients` - Patient information
- `doctors` - Doctor details and specializations
- `appointments` - Appointment scheduling
- `medical_records` - Patient medical history
- `rooms` - Hospital room management
- `billing` - Payment and billing records

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## License

This project is for educational purposes.
`

---


## USAGE_INSTRUCTIONS.md

### Usage Instructions

`markdown
# Hospital Management System - Usage Instructions

## 🚀 How to Run the System

### Option 1: Flask + Tkinter (Recommended)
```bash
# Start Flask server first
python flask_app.py

# In another terminal, start the GUI
python tkinter_flask_gui.py
```

### Option 2: Use the automated starter
```bash
python run_hospital_system.py
```

### Option 3: Use batch file (Windows)
```bash
start_hospital_system.bat
```

## 📋 Sample Data Available

### Sample Patients (Use these IDs for testing):
- **Patient ID 1**: John Doe (555-0001) - 4 medical records
- **Patient ID 2**: Sarah Johnson (555-0003) - 3 medical records
- **Patient ID 3**: Michael Brown (555-0005) - 3 medical records
- **Patient ID 4**: Emily Davis (555-0007) - 3 medical records
- **Patient ID 5**: David Wilson (555-0009) - 2 medical records
- **All 19 patients** have comprehensive medical records (58 total records)

### Sample Doctors:
- **Dr. John Smith** - Cardiology (ID: 1)
- **Dr. Sarah Johnson** - Pediatrics (ID: 2)
- **Dr. Michael Brown** - Orthopedics (ID: 3)
- **Dr. Emily Davis** - Neurology (ID: 4)
- **Dr. David Wilson** - General Medicine (ID: 5)

## 🏥 How to Use Each Feature

### 📊 Dashboard
- View hospital statistics (patients, doctors, appointments, rooms)
- See today's appointments
- Click "🔄 Refresh Dashboard" to update data

### 👥 Patient Management

#### Add New Patient:
1. Go to "👥 Patients" tab
2. Click "➕ Add Patient" sub-tab
3. Fill in required fields (marked with *)
4. Click "🚀 Register Patient"

#### Search Patients:
1. Go to "🔍 Search Patients" sub-tab
2. Enter name, phone, or email in search box
3. Click "🔍 Search" or "📋 Load All"

### 📅 Appointment Booking

#### Book New Appointment:
1. Go to "📅 Appointments" tab
2. Enter a valid Patient ID (use sample IDs above)
3. Click "✓ Validate" to check if patient exists
4. Select a doctor from dropdown
5. Choose date and time
6. Add reason (optional)
7. Click "✅ Book Appointment"

**Important**: Use existing Patient IDs (1-16) for testing appointments!

### 📋 Medical Records
1. Go to "📋 Medical Records" tab
2. Enter any Patient ID (1-19 all have comprehensive medical records)
3. Click "📋 Load Records"
4. View detailed medical history including:
   - Visit dates and diagnoses
   - Doctor specializations
   - Treatments and prescriptions
   - Clinical notes

### 🔄 Quick Sort Data Analysis
1. Go to "🔄 Quick Sort" tab
2. Select data type (Medical Records, Patients, or Appointments)
3. Choose sort field (automatically updates based on data type)
4. Select sort order (Ascending or Descending)
5. Optional: Enter Filter ID for specific patient/doctor records
6. Click "🚀 Quick Sort Data" to execute
7. View sorted results with algorithm performance metrics

**Quick Sort Features:**
- **Medical Records**: Sort by visit date, diagnosis, specialization, etc.
- **Patients**: Sort by name, ID, birth date, gender, etc.
- **Appointments**: Sort by date, time, status, patient, doctor
- **Performance**: O(n log n) efficient Quick Sort algorithm
- **Real-time**: Instant results with sorting statistics

## ⚠️ Troubleshooting

### "Failed to book appointment" Error:
- **Cause**: Invalid Patient ID or Doctor ID
- **Solution**: Use the "✓ Validate" button to check Patient ID
- **Valid Patient IDs**: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16

### "Cannot connect to Flask API" Error:
- **Cause**: Flask server not running
- **Solution**: Start Flask server first: `python flask_app.py`

### Database Connection Error:
- **Cause**: MySQL not running or wrong credentials
- **Solution**: 
  1. Start MySQL server
  2. Run: `python create_hospital_database.py`
  3. Check credentials in `flask_app.py`

## 🔧 API Endpoints (for developers)

- `GET /api/test` - Test API connection
- `GET /api/dashboard` - Get dashboard data
- `GET /api/patients` - Get all patients
- `POST /api/patients/search` - Search patients
- `POST /api/patients` - Add new patient
- `GET /api/doctors` - Get all doctors
- `POST /api/appointments` - Book appointment
- `GET /api/validate/patient/{id}` - Validate patient ID
- `GET /api/validate/doctor/{id}` - Validate doctor ID

## 📞 Quick Test Scenario

1. **Start the system**: `python flask_app.py` then `python tkinter_flask_gui.py`
2. **View dashboard**: Check current statistics
3. **Add a patient**: Register a new patient and note the Patient ID
4. **Book appointment**: Use the new Patient ID to book an appointment
5. **View results**: Check dashboard to see the new appointment

## 💡 Tips

- Always validate Patient IDs before booking appointments
- Use the search feature to find existing patients
- The system shows real-time data from the MySQL database
- All times are in 24-hour format (08:00 - 17:45)
- Appointments can only be booked for future dates
`

---

