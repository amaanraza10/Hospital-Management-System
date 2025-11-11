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