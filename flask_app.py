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