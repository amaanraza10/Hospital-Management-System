import mysql.connector
from datetime import date, timedelta
import random

def add_more_indian_patients():
    """Add 50 more Indian patients with comprehensive data"""
    
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="amaanraza",
            password="Amaan123!",
            database="hospital_management"
        )
        
        cursor = connection.cursor()
        
        # Additional 50 Indian patients with authentic names
        new_patients = [
            # 31-40
            ('Lakshmi', 'Krishnan', '1986-03-22', 'Female', '+91-9876543270', 'lakshmi.krishnan@email.com', 'EE-429, Coimbatore RS Puram, TN', 'Ravi Krishnan', '+91-9876543271', 'A+'),
            ('Aditya', 'Deshmukh', '1990-11-15', 'Male', '+91-9876543272', 'aditya.deshmukh@email.com', 'FF-530, Nagpur Dharampeth, MH', 'Priya Deshmukh', '+91-9876543273', 'B+'),
            ('Meera', 'Kulkarni', '1983-07-08', 'Female', '+91-9876543274', 'meera.kulkarni@email.com', 'GG-631, Pune Shivaji Nagar, MH', 'Suresh Kulkarni', '+91-9876543275', 'O+'),
            ('Varun', 'Bose', '1995-02-19', 'Male', '+91-9876543276', 'varun.bose@email.com', 'HH-732, Kolkata Park Street, WB', 'Anita Bose', '+91-9876543277', 'AB+'),
            ('Tanvi', 'Rao', '1988-09-12', 'Female', '+91-9876543278', 'tanvi.rao@email.com', 'II-833, Bangalore Indiranagar, KA', 'Mohan Rao', '+91-9876543279', 'A-'),
            ('Kunal', 'Mehta', '1979-05-25', 'Male', '+91-9876543280', 'kunal.mehta@email.com', 'JJ-934, Ahmedabad Navrangpura, GJ', 'Sneha Mehta', '+91-9876543281', 'B-'),
            ('Divya', 'Pillai', '1992-12-03', 'Female', '+91-9876543282', 'divya.pillai@email.com', 'KK-135, Trivandrum Pattom, KL', 'Arun Pillai', '+91-9876543283', 'O-'),
            ('Rohan', 'Chatterjee', '1985-08-17', 'Male', '+91-9876543284', 'rohan.chatterjee@email.com', 'LL-236, Kolkata Salt Lake, WB', 'Ritu Chatterjee', '+91-9876543285', 'AB-'),
            ('Shruti', 'Ghosh', '1991-04-29', 'Female', '+91-9876543286', 'shruti.ghosh@email.com', 'MM-337, Kolkata Ballygunge, WB', 'Amit Ghosh', '+91-9876543287', 'A+'),
            ('Yash', 'Thakur', '1987-10-14', 'Male', '+91-9876543288', 'yash.thakur@email.com', 'NN-438, Shimla Mall Road, HP', 'Pooja Thakur', '+91-9876543289', 'B+'),
            
            # 41-50
            ('Priyanka', 'Shetty', '1993-06-07', 'Female', '+91-9876543290', 'priyanka.shetty@email.com', 'OO-539, Mangalore Kadri, KA', 'Rajesh Shetty', '+91-9876543291', 'O+'),
            ('Aryan', 'Khanna', '1982-01-20', 'Male', '+91-9876543292', 'aryan.khanna@email.com', 'PP-640, Delhi Connaught Place, DL', 'Neha Khanna', '+91-9876543293', 'AB+'),
            ('Sakshi', 'Dubey', '1989-07-13', 'Female', '+91-9876543294', 'sakshi.dubey@email.com', 'QQ-741, Lucknow Hazratganj, UP', 'Vivek Dubey', '+91-9876543295', 'A-'),
            ('Kartik', 'Nambiar', '1994-03-26', 'Male', '+91-9876543296', 'kartik.nambiar@email.com', 'RR-842, Kochi Ernakulam, KL', 'Divya Nambiar', '+91-9876543297', 'B-'),
            ('Anushka', 'Bajaj', '1986-11-09', 'Female', '+91-9876543298', 'anushka.bajaj@email.com', 'SS-943, Chandigarh Sector 35, CH', 'Rohit Bajaj', '+91-9876543299', 'O-'),
            ('Siddharth', 'Rane', '1990-05-22', 'Male', '+91-9876543300', 'siddharth.rane@email.com', 'TT-144, Mumbai Dadar, MH', 'Priya Rane', '+91-9876543301', 'AB-'),
            ('Tanya', 'Kaul', '1984-12-15', 'Female', '+91-9876543302', 'tanya.kaul@email.com', 'UU-245, Srinagar Dal Lake, JK', 'Anil Kaul', '+91-9876543303', 'A+'),
            ('Dhruv', 'Sethi', '1992-08-28', 'Male', '+91-9876543304', 'dhruv.sethi@email.com', 'VV-346, Delhi Rohini, DL', 'Kavita Sethi', '+91-9876543305', 'B+'),
            ('Isha', 'Bhatia', '1988-02-11', 'Female', '+91-9876543306', 'isha.bhatia@email.com', 'WW-447, Amritsar Golden Temple, PB', 'Manish Bhatia', '+91-9876543307', 'O+'),
            ('Arnav', 'Dutta', '1981-09-04', 'Male', '+91-9876543308', 'arnav.dutta@email.com', 'XX-548, Guwahati Fancy Bazaar, AS', 'Ritu Dutta', '+91-9876543309', 'AB+'),
            
            # 51-60
            ('Naina', 'Kohli', '1995-04-17', 'Female', '+91-9876543310', 'naina.kohli@email.com', 'YY-649, Ludhiana Model Town, PB', 'Rajiv Kohli', '+91-9876543311', 'A-'),
            ('Vihaan', 'Tripathi', '1987-10-30', 'Male', '+91-9876543312', 'vihaan.tripathi@email.com', 'ZZ-750, Varanasi Assi Ghat, UP', 'Anjali Tripathi', '+91-9876543313', 'B-'),
            ('Kiara', 'Hegde', '1991-06-23', 'Female', '+91-9876543314', 'kiara.hegde@email.com', 'AAA-851, Udupi Car Street, KA', 'Suresh Hegde', '+91-9876543315', 'O-'),
            ('Reyansh', 'Pandya', '1983-01-06', 'Male', '+91-9876543316', 'reyansh.pandya@email.com', 'BBB-952, Rajkot Kalawad Road, GJ', 'Priya Pandya', '+91-9876543317', 'AB-'),
            ('Myra', 'Saxena', '1989-07-19', 'Female', '+91-9876543318', 'myra.saxena@email.com', 'CCC-153, Indore Vijay Nagar, MP', 'Amit Saxena', '+91-9876543319', 'A+'),
            ('Aarav', 'Menon', '1994-03-02', 'Male', '+91-9876543320', 'aarav.menon@email.com', 'DDD-254, Chennai Anna Nagar, TN', 'Divya Menon', '+91-9876543321', 'B+'),
            ('Saanvi', 'Joshi', '1986-11-25', 'Female', '+91-9876543322', 'saanvi.joshi@email.com', 'EEE-355, Pune Kothrud, MH', 'Rohit Joshi', '+91-9876543323', 'O+'),
            ('Vivaan', 'Bhardwaj', '1992-05-08', 'Male', '+91-9876543324', 'vivaan.bhardwaj@email.com', 'FFF-456', 'Neha Bhardwaj', '+91-9876543325', 'AB+'),
            ('Aanya', 'Malhotra', '1988-12-21', 'Female', '+91-9876543326', 'aanya.malhotra@email.com', 'GGG-557, Delhi Vasant Kunj, DL', 'Karan Malhotra', '+91-9876543327', 'A-'),
            ('Ayaan', 'Kapoor', '1980-08-14', 'Male', '+91-9876543328', 'ayaan.kapoor@email.com', 'HHH-658, Mumbai Bandra, MH', 'Priya Kapoor', '+91-9876543329', 'B-'),
            
            # 61-70
            ('Diya', 'Sharma', '1993-02-27', 'Female', '+91-9876543330', 'diya.sharma@email.com', 'III-759, Jaipur C-Scheme, RJ', 'Rajesh Sharma', '+91-9876543331', 'O-'),
            ('Arjun', 'Reddy', '1985-09-10', 'Male', '+91-9876543332', 'arjun.reddy@email.com', 'JJJ-860, Hyderabad Jubilee Hills, TS', 'Sneha Reddy', '+91-9876543333', 'AB-'),
            ('Pari', 'Gupta', '1991-05-23', 'Female', '+91-9876543334', 'pari.gupta@email.com', 'KKK-961, Noida Sector 62, UP', 'Amit Gupta', '+91-9876543335', 'A+'),
            ('Shaurya', 'Singh', '1987-01-16', 'Male', '+91-9876543336', 'shaurya.singh@email.com', 'LLL-162, Lucknow Gomti Nagar, UP', 'Kavita Singh', '+91-9876543337', 'B+'),
            ('Anaya', 'Patel', '1994-07-29', 'Female', '+91-9876543338', 'anaya.patel@email.com', 'MMM-263, Surat Adajan, GJ', 'Manish Patel', '+91-9876543339', 'O+'),
            ('Kabir', 'Verma', '1982-03-12', 'Male', '+91-9876543340', 'kabir.verma@email.com', 'NNN-364, Bhopal Arera Colony, MP', 'Ritu Verma', '+91-9876543341', 'AB+'),
            ('Aadhya', 'Iyer', '1989-10-05', 'Female', '+91-9876543342', 'aadhya.iyer@email.com', 'OOO-465, Bangalore Whitefield, KA', 'Suresh Iyer', '+91-9876543343', 'A-'),
            ('Advait', 'Nair', '1995-06-18', 'Male', '+91-9876543344', 'advait.nair@email.com', 'PPP-566, Kochi Fort Kochi, KL', 'Priya Nair', '+91-9876543345', 'B-'),
            ('Navya', 'Agarwal', '1986-12-01', 'Female', '+91-9876543346', 'navya.agarwal@email.com', 'QQQ-667, Jaipur Vaishali Nagar, RJ', 'Rohit Agarwal', '+91-9876543347', 'O-'),
            ('Atharv', 'Chopra', '1992-08-24', 'Male', '+91-9876543348', 'atharv.chopra@email.com', 'RRR-768, Chandigarh Sector 17, CH', 'Anjali Chopra', '+91-9876543349', 'AB-'),
            
            # 71-80
            ('Ira', 'Bansal', '1988-04-07', 'Female', '+91-9876543350', 'ira.bansal@email.com', 'SSS-869, Gurgaon DLF Phase 3, HR', 'Karan Bansal', '+91-9876543351', 'A+'),
            ('Rudra', 'Mishra', '1984-11-20', 'Male', '+91-9876543352', 'rudra.mishra@email.com', 'TTT-970, Varanasi Cantonment, UP', 'Priya Mishra', '+91-9876543353', 'B+'),
            ('Zara', 'Pandey', '1990-05-13', 'Female', '+91-9876543354', 'zara.pandey@email.com', 'UUU-171, Allahabad Civil Lines, UP', 'Vivek Pandey', '+91-9876543355', 'O+'),
            ('Shivansh', 'Tiwari', '1993-01-26', 'Male', '+91-9876543356', 'shivansh.tiwari@email.com', 'VVV-272, Kanpur Swaroop Nagar, UP', 'Neha Tiwari', '+91-9876543357', 'AB+'),
            ('Anika', 'Bhatt', '1987-07-09', 'Female', '+91-9876543358', 'anika.bhatt@email.com', 'WWW-373, Surat Vesu, GJ', 'Rajesh Bhatt', '+91-9876543359', 'A-'),
            ('Veer', 'Kumar', '1991-03-22', 'Male', '+91-9876543360', 'veer.kumar@email.com', 'XXX-474, Patna Boring Road, BR', 'Anjali Kumar', '+91-9876543361', 'B-'),
            ('Riya', 'Sinha', '1985-10-15', 'Female', '+91-9876543362', 'riya.sinha@email.com', 'YYY-575, Ranchi Main Road, JH', 'Amit Sinha', '+91-9876543363', 'O-'),
            ('Aadi', 'Yadav', '1994-06-28', 'Male', '+91-9876543364', 'aadi.yadav@email.com', 'ZZZ-676, Agra Taj Ganj, UP', 'Priya Yadav', '+91-9876543365', 'AB-'),
            ('Sara', 'Jain', '1989-02-11', 'Female', '+91-9876543366', 'sara.jain@email.com', 'AAAA-777, Indore Palasia, MP', 'Manish Jain', '+91-9876543367', 'A+'),
            ('Ishaan', 'Desai', '1982-09-04', 'Male', '+91-9876543368', 'ishaan.desai@email.com', 'BBBB-878, Mumbai Andheri, MH', 'Kavita Desai', '+91-9876543369', 'B+'),
        ]
        
        # Insert new patients
        insert_query = """
        INSERT INTO patients (first_name, last_name, date_of_birth, gender, phone, email, address, emergency_contact_name, emergency_contact_phone, blood_type)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.executemany(insert_query, new_patients)
        connection.commit()
        
        print(f"✅ Successfully added {len(new_patients)} new Indian patients!")
        
        # Get patient IDs for medical records
        cursor.execute("SELECT patient_id FROM patients WHERE patient_id > 30 ORDER BY patient_id")
        new_patient_ids = [row[0] for row in cursor.fetchall()]
        
        # Add comprehensive medical records for new patients
        print("📋 Adding medical records for new patients...")
        
        medical_records = []
        doctors = list(range(1, 13))  # 12 doctors
        
        # Common Indian medical conditions
        conditions = [
            ('Type 2 Diabetes Mellitus', 'Metformin 500mg BD, Glimepiride 2mg OD', 'Lifestyle modification, regular monitoring'),
            ('Hypertension (Essential)', 'Amlodipine 5mg OD, Telmisartan 40mg OD', 'Salt restriction, regular BP monitoring'),
            ('Acute Gastroenteritis', 'ORS, Zinc supplements, Probiotics', 'Oral rehydration therapy'),
            ('Dengue Fever', 'Paracetamol, IV fluids, Platelet monitoring', 'Supportive care, rest'),
            ('Bronchial Asthma', 'Salbutamol inhaler, Budesonide inhaler', 'Avoid triggers, regular follow-up'),
            ('Thyroid Disorder', 'Levothyroxine 50mcg OD', 'Regular thyroid function tests'),
            ('Vitamin D Deficiency', 'Vitamin D3 60,000 IU weekly', 'Sun exposure, dietary supplements'),
            ('Iron Deficiency Anemia', 'Ferrous sulfate 200mg OD', 'Iron-rich diet, follow-up CBC'),
            ('Acute Upper Respiratory Infection', 'Paracetamol, Antihistamines', 'Rest, fluids, steam inhalation'),
            ('Osteoarthritis', 'Glucosamine, Chondroitin, Physiotherapy', 'Weight management, exercise'),
            ('Migraine', 'Propranolol 40mg BD, Sumatriptan SOS', 'Trigger avoidance, stress management'),
            ('Peptic Ulcer Disease', 'Pantoprazole 40mg BD, H.pylori therapy', 'Avoid NSAIDs, dietary modification'),
            ('Allergic Rhinitis', 'Cetirizine 10mg OD, Nasal spray', 'Avoid allergens'),
            ('Urinary Tract Infection', 'Nitrofurantoin 100mg BD for 5 days', 'Increased fluid intake'),
            ('Acute Bronchitis', 'Azithromycin 500mg OD, Cough syrup', 'Rest, steam inhalation'),
        ]
        
        # Add 3-5 medical records per new patient
        for patient_id in new_patient_ids:
            num_records = random.randint(3, 5)
            for i in range(num_records):
                doctor_id = random.choice(doctors)
                condition = random.choice(conditions)
                days_ago = random.randint(30, 365)
                visit_date = date.today() - timedelta(days=days_ago)
                
                diagnosis, prescription, treatment = condition
                notes = f"Patient presented with symptoms. Examination conducted. {treatment}. Follow-up advised."
                
                medical_records.append((
                    patient_id, doctor_id, visit_date,
                    diagnosis, treatment, prescription, notes
                ))
        
        # Insert medical records
        records_query = """
        INSERT INTO medical_records (patient_id, doctor_id, visit_date, diagnosis, treatment, prescription, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.executemany(records_query, medical_records)
        connection.commit()
        
        print(f"✅ Successfully added {len(medical_records)} medical records!")
        
        # Add some appointments for new patients
        print("📅 Adding appointments for new patients...")
        
        appointments = []
        today = date.today()
        
        # Add 20 random appointments
        for _ in range(20):
            patient_id = random.choice(new_patient_ids)
            doctor_id = random.choice(doctors)
            days_offset = random.randint(-7, 30)  # Past week to next month
            apt_date = today + timedelta(days=days_offset)
            apt_time = f"{random.randint(9, 17):02d}:{random.choice(['00', '15', '30', '45'])}:00"
            
            if days_offset < 0:
                status = 'Completed'
            elif days_offset == 0:
                status = random.choice(['Scheduled', 'In Progress'])
            else:
                status = 'Scheduled'
            
            reasons = [
                'Regular checkup', 'Follow-up visit', 'Consultation',
                'Health screening', 'Medication review', 'Symptom evaluation'
            ]
            reason = random.choice(reasons)
            
            appointments.append((
                patient_id, doctor_id, apt_date, apt_time, status, reason
            ))
        
        apt_query = """
        INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, status, reason)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        cursor.executemany(apt_query, appointments)
        connection.commit()
        
        print(f"✅ Successfully added {len(appointments)} appointments!")
        
        # Display summary
        cursor.execute("SELECT COUNT(*) FROM patients")
        total_patients = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM medical_records")
        total_records = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM appointments")
        total_appointments = cursor.fetchone()[0]
        
        print("\n" + "="*50)
        print("📊 DATABASE SUMMARY")
        print("="*50)
        print(f"👥 Total Patients: {total_patients}")
        print(f"📋 Total Medical Records: {total_records}")
        print(f"📅 Total Appointments: {total_appointments}")
        print(f"👨‍⚕️ Total Doctors: 12")
        print("="*50)
        print("\n🎉 Database updated successfully with more Indian patient data!")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🏥 Adding More Indian Patients to Hospital Database")
    print("="*50)
    add_more_indian_patients()
