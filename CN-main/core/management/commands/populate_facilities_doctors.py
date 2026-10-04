from django.core.management.base import BaseCommand
from core.models import Hospital, Doctor
import random


class Command(BaseCommand):
    help = 'Populate hospitals with facility data and doctors'

    def handle(self, *args, **kwargs):
        hospitals = Hospital.objects.all()
        
        if not hospitals.exists():
            self.stdout.write(self.style.WARNING('No hospitals found. Please add hospitals first.'))
            return
        
        # Facility templates based on hospital type
        facility_templates = {
            'government': {
                'total_beds': (200, 500),
                'icu_beds': (20, 50),
                'emergency_beds': (30, 80),
                'facilities': {
                    'xray': True,
                    'mri': True,
                    'ct_scan': True,
                    'ultrasound': True,
                    'blood_bank': True,
                    'laboratory': True,
                    'pharmacy': True,
                    'ambulance': True,
                    'operation_theaters': random.randint(5, 12)
                }
            },
            'premium': {
                'total_beds': (100, 300),
                'icu_beds': (15, 40),
                'emergency_beds': (20, 50),
                'facilities': {
                    'xray': True,
                    'mri': True,
                    'ct_scan': True,
                    'ultrasound': True,
                    'blood_bank': True,
                    'laboratory': True,
                    'pharmacy': True,
                    'ambulance': True,
                    'operation_theaters': random.randint(8, 15)
                }
            },
            'private': {
                'total_beds': (50, 200),
                'icu_beds': (10, 30),
                'emergency_beds': (10, 40),
                'facilities': {
                    'xray': True,
                    'mri': random.choice([True, False]),
                    'ct_scan': random.choice([True, False]),
                    'ultrasound': True,
                    'blood_bank': True,
                    'laboratory': True,
                    'pharmacy': True,
                    'ambulance': True,
                    'operation_theaters': random.randint(3, 8)
                }
            },
            'trust': {
                'total_beds': (80, 250),
                'icu_beds': (12, 35),
                'emergency_beds': (15, 50),
                'facilities': {
                    'xray': True,
                    'mri': True,
                    'ct_scan': random.choice([True, False]),
                    'ultrasound': True,
                    'blood_bank': True,
                    'laboratory': True,
                    'pharmacy': True,
                    'ambulance': True,
                    'operation_theaters': random.randint(4, 10)
                }
            },
        }
        
        # ===== CATEGORY-SPECIFIC FACILITY TEMPLATES =====
        category_facility_templates = {
            'xray': {
                'total_beds': 0,
                'icu_beds': 0,
                'emergency_beds': 0,
                'facilities': {
                    'xray': True,
                    'digital_xray': True,
                    'dental_xray': True,
                    'fluoroscopy': True,
                    'ultrasound': random.choice([True, False]),
                    'laboratory': False,
                    'pharmacy': False,
                    'ambulance': False,
                    'waiting_lounge': True,
                    'report_delivery': True,
                    'online_reports': True,
                }
            },
            'mri': {
                'total_beds': 0,
                'icu_beds': 0,
                'emergency_beds': 0,
                'facilities': {
                    'mri': True,
                    'mri_3t': random.choice([True, False]),
                    'mri_1_5t': True,
                    'open_mri': random.choice([True, False]),
                    'contrast_mri': True,
                    'xray': random.choice([True, False]),
                    'ultrasound': random.choice([True, False]),
                    'laboratory': False,
                    'pharmacy': False,
                    'ambulance': False,
                    'waiting_lounge': True,
                    'report_delivery': True,
                    'online_reports': True,
                }
            },
            'ct_scan': {
                'total_beds': 0,
                'icu_beds': 0,
                'emergency_beds': 0,
                'facilities': {
                    'ct_scan': True,
                    'ct_128_slice': random.choice([True, False]),
                    'ct_64_slice': True,
                    'ct_angiography': True,
                    'ct_contrast': True,
                    'xray': random.choice([True, False]),
                    'ultrasound': random.choice([True, False]),
                    'laboratory': False,
                    'pharmacy': False,
                    'ambulance': False,
                    'waiting_lounge': True,
                    'report_delivery': True,
                    'online_reports': True,
                }
            },
            'physiotherapy': {
                'total_beds': (5, 15),
                'icu_beds': 0,
                'emergency_beds': 0,
                'facilities': {
                    'electrotherapy': True,
                    'ultrasound_therapy': True,
                    'hydrotherapy': random.choice([True, False]),
                    'traction_unit': True,
                    'exercise_gym': True,
                    'parallel_bars': True,
                    'tens_machine': True,
                    'laser_therapy': random.choice([True, False]),
                    'cryotherapy': True,
                    'wax_therapy': True,
                    'waiting_lounge': True,
                    'ambulance': False,
                    'pharmacy': False,
                    'laboratory': False,
                }
            },
            'pathology': {
                'total_beds': 0,
                'icu_beds': 0,
                'emergency_beds': 0,
                'facilities': {
                    'laboratory': True,
                    'blood_collection': True,
                    'urine_analysis': True,
                    'hematology': True,
                    'biochemistry': True,
                    'microbiology': True,
                    'histopathology': random.choice([True, False]),
                    'serology': True,
                    'immunology': random.choice([True, False]),
                    'home_collection': True,
                    'online_reports': True,
                    'report_delivery': True,
                    'waiting_lounge': True,
                    'ambulance': False,
                    'pharmacy': False,
                }
            },
        }

        # ===== CATEGORY-SPECIFIC DOCTOR TEMPLATES =====
        category_doctor_templates = {
            'xray': [
                {'name': 'Dr. Rahul Verma', 'qualification': 'MBBS, MD (Radiology)', 'specialization': 'Radiologist', 'experience': (8, 20)},
                {'name': 'Dr. Neha Saxena', 'qualification': 'MBBS, DMRD', 'specialization': 'Diagnostic Radiologist', 'experience': (5, 15)},
                {'name': 'Dr. Kiran Bhatt', 'qualification': 'MBBS, DNB (Radiology)', 'specialization': 'X-Ray Specialist', 'experience': (6, 18)},
            ],
            'mri': [
                {'name': 'Dr. Sanjay Kulkarni', 'qualification': 'MBBS, MD (Radiology), Fellowship MRI', 'specialization': 'MRI Specialist', 'experience': (10, 25)},
                {'name': 'Dr. Pooja Rawal', 'qualification': 'MBBS, DM (Neuroradiology)', 'specialization': 'Neuro-Radiologist', 'experience': (12, 22)},
                {'name': 'Dr. Aditya Parikh', 'qualification': 'MBBS, MD (Radiology)', 'specialization': 'Musculoskeletal Radiologist', 'experience': (8, 18)},
            ],
            'ct_scan': [
                {'name': 'Dr. Manoj Tiwari', 'qualification': 'MBBS, MD (Radiology), Fellowship CT', 'specialization': 'CT Imaging Specialist', 'experience': (10, 22)},
                {'name': 'Dr. Ritu Agarwal', 'qualification': 'MBBS, DMRD, DNB', 'specialization': 'Diagnostic Imaging Specialist', 'experience': (8, 20)},
                {'name': 'Dr. Vikash Jain', 'qualification': 'MBBS, MD (Radiology)', 'specialization': 'Interventional Radiologist', 'experience': (10, 25)},
            ],
            'physiotherapy': [
                {'name': 'Dr. Ananya Iyer', 'qualification': 'BPT, MPT (Orthopedics)', 'specialization': 'Orthopedic Physiotherapist', 'experience': (6, 15)},
                {'name': 'Dr. Deepak Chauhan', 'qualification': 'BPT, MPT (Neuro)', 'specialization': 'Neuro Physiotherapist', 'experience': (8, 18)},
                {'name': 'Dr. Swati Pandey', 'qualification': 'BPT, MPT (Sports Medicine)', 'specialization': 'Sports Physiotherapist', 'experience': (5, 14)},
                {'name': 'Dr. Rakesh Yadav', 'qualification': 'BPT, MPT (Cardiopulmonary)', 'specialization': 'Cardiopulmonary Physiotherapist', 'experience': (7, 16)},
            ],
            'pathology': [
                {'name': 'Dr. Meera Chatterjee', 'qualification': 'MBBS, MD (Pathology)', 'specialization': 'Clinical Pathologist', 'experience': (10, 25)},
                {'name': 'Dr. Arun Kapoor', 'qualification': 'MBBS, MD (Microbiology)', 'specialization': 'Microbiologist', 'experience': (8, 20)},
                {'name': 'Dr. Sunita Rao', 'qualification': 'MBBS, MD (Biochemistry)', 'specialization': 'Biochemist', 'experience': (7, 18)},
                {'name': 'Dr. Nitin Shah', 'qualification': 'MBBS, MD (Hematology)', 'specialization': 'Hematologist', 'experience': (10, 22)},
            ],
        }

        # Doctor templates for hospitals
        doctor_templates = [
            {'name': 'Rajesh Kumar', 'qualification': 'MBBS, MD (General Medicine)', 'specialization': 'General Physician', 'experience': (5, 15)},
            {'name': 'Priya Sharma', 'qualification': 'MBBS, MS (General Surgery)', 'specialization': 'General Surgeon', 'experience': (8, 20)},
            {'name': 'Amit Patel', 'qualification': 'MBBS, MD (Cardiology)', 'specialization': 'Cardiologist', 'experience': (10, 25)},
            {'name': 'Sneha Desai', 'qualification': 'MBBS, MD (Pediatrics)', 'specialization': 'Pediatrician', 'experience': (6, 18)},
            {'name': 'Vikram Singh', 'qualification': 'MBBS, MS (Orthopedics)', 'specialization': 'Orthopedic Surgeon', 'experience': (12, 28)},
            {'name': 'Anjali Mehta', 'qualification': 'MBBS, MD (Dermatology)', 'specialization': 'Dermatologist', 'experience': (7, 16)},
            {'name': 'Suresh Reddy', 'qualification': 'MBBS, DM (Neurology)', 'specialization': 'Neurologist', 'experience': (15, 30)},
            {'name': 'Kavita Joshi', 'qualification': 'MBBS, MD (Gynecology)', 'specialization': 'Gynecologist', 'experience': (9, 22)},
            {'name': 'Rahul Verma', 'qualification': 'MBBS, MD (Radiology)', 'specialization': 'Radiologist', 'experience': (8, 19)},
            {'name': 'Meera Nair', 'qualification': 'MBBS, MD (Anesthesiology)', 'specialization': 'Anesthesiologist', 'experience': (10, 24)},
        ]
        
        consultation_days_options = [
            'Mon-Sat',
            'Mon, Wed, Fri',
            'Tue, Thu, Sat',
            'Mon-Fri',
            'Daily',
            'Mon, Tue, Thu, Fri'
        ]
        
        updated_count = 0
        doctors_created = 0
        
        for hospital in hospitals:
            category = hospital.facility_category

            if category != 'hospital' and category in category_facility_templates:
                # ===== NON-HOSPITAL FACILITY CENTER =====
                cat_template = category_facility_templates[category]

                # Set beds (0 for imaging/pathology, small range for physiotherapy)
                beds = cat_template['total_beds']
                hospital.total_beds = random.randint(*beds) if isinstance(beds, tuple) else beds
                hospital.icu_beds = cat_template['icu_beds']
                hospital.emergency_beds = cat_template['emergency_beds']

                # Set category-specific facilities
                hospital.facilities = cat_template['facilities'].copy()
                hospital.save()
                updated_count += 1

                # Delete existing doctors for this center
                hospital.doctors.all().delete()

                # Create category-specific doctors (2-3 per center)
                cat_doctors = category_doctor_templates.get(category, [])
                num_doctors = min(random.randint(2, 3), len(cat_doctors))
                selected_doctors = random.sample(cat_doctors, num_doctors)

                for idx, doc_template in enumerate(selected_doctors):
                    experience = random.randint(*doc_template['experience'])
                    Doctor.objects.create(
                        hospital=hospital,
                        name=doc_template['name'],
                        qualification=doc_template['qualification'],
                        specialization=doc_template['specialization'],
                        experience_years=experience,
                        is_head_doctor=(idx == 0),
                        consultation_days=random.choice(consultation_days_options)
                    )
                    doctors_created += 1
            else:
                # ===== HOSPITAL =====
                template = facility_templates.get(hospital.hospital_type, facility_templates['private'])
                
                total_beds_range = template['total_beds']
                icu_beds_range = template['icu_beds']
                emergency_beds_range = template['emergency_beds']
                
                hospital.total_beds = random.randint(*total_beds_range)
                hospital.icu_beds = random.randint(*icu_beds_range)
                hospital.emergency_beds = random.randint(*emergency_beds_range)
                
                facilities = template['facilities'].copy()
                facilities['operation_theaters'] = random.randint(3, 15)
                hospital.facilities = facilities
                
                hospital.save()
                updated_count += 1
                
                # Delete existing doctors for this hospital
                hospital.doctors.all().delete()

                # Create 3-5 doctors per hospital
                num_doctors = random.randint(3, 5)
                selected_doctors = random.sample(doctor_templates, min(num_doctors, len(doctor_templates)))
                
                for idx, doc_template in enumerate(selected_doctors):
                    experience = random.randint(*doc_template['experience'])
                    
                    Doctor.objects.create(
                        hospital=hospital,
                        name=doc_template['name'],
                        qualification=doc_template['qualification'],
                        specialization=doc_template['specialization'],
                        experience_years=experience,
                        is_head_doctor=(idx == 0),
                        consultation_days=random.choice(consultation_days_options)
                    )
                    doctors_created += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully updated {updated_count} facilities with data and created {doctors_created} doctors'
            )
        )
