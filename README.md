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