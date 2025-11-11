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