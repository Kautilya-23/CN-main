from django.core.management.base import BaseCommand
from core.models import Hospital
import uuid

class Command(BaseCommand):
    help = 'Seeds the database with initial hospital data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')
        
        # Clear existing data
        Hospital.objects.all().delete()

        hospitals = [
          # ===== GOVERNMENT / TRUST (LOW COST, ALL-ROUND) =====
          {
            "name": 'Civil Hospital Ahmedabad',
            "address": 'Asarwa',
            "city": 'Ahmedabad',
            "pincode": '380016',
            "lat": 23.0525,
            "lng": 72.6028,
            "contact": '079-22683721',
            "specialities": [
              'General Medicine',
              'Emergency',
              'Trauma',
              'Cardiology',
              'Neurology',
              'Orthopedics',
              'Pediatrics',
              'Gynecology',
              'Psychiatry'
            ],
            "hospital_type": 'government',
            "rating": 4.0,
            "acceptedSchemes": [
              { "schemeName": 'Ayushman Bharat PM-JAY', "schemeId": str(uuid.uuid4()) },
              { "schemeName": 'Mukhyamantri Amrutum Yojana', "schemeId": str(uuid.uuid4()) },
              { "schemeName": 'CGHS', "schemeId": str(uuid.uuid4()) }
            ],
            "base_cost_factor": 0.85
          },
          {
            "name": 'V.S. General Hospital',
            "address": 'Ellisbridge',
            "city": 'Ahmedabad',
            "pincode": '380006',
            "lat": 23.0225,
            "lng": 72.5714,
            "contact": '079-26577621',
            "specialities": [
              'General Medicine',
              'Dermatology',
              'Pediatrics',
              'ENT',
              'Ophthalmology'
            ],
            "hospital_type": 'trust',
            "rating": 3.8,
            "acceptedSchemes": [
              { "schemeName": 'Ayushman Bharat PM-JAY', "schemeId": str(uuid.uuid4()) },
              { "schemeName": 'Mukhyamantri Amrutum Yojana', "schemeId": str(uuid.uuid4()) }
            ],
            "base_cost_factor": 0.95
          },
          {
            "name": 'IKDRC – Institute of Kidney Diseases',
            "address": 'Civil Hospital Campus, Asarwa',
            "city": 'Ahmedabad',
            "pincode": '380016',
            "lat": 23.0539,
            "lng": 72.6031,
            "contact": '079-22687101',
            "specialities": [
              'Nephrology',
              'Dialysis',
              'Transplant',
              'Urology'
            ],
            "hospital_type": 'government',
            "rating": 4.1,
            "acceptedSchemes": [
              { "schemeName": 'Ayushman Bharat PM-JAY', "schemeId": str(uuid.uuid4()) },
              { "schemeName": 'Mukhyamantri Amrutum Yojana', "schemeId": str(uuid.uuid4()) },
              { "schemeName": 'ESIC', "schemeId": str(uuid.uuid4()) }
            ],
            "base_cost_factor": 0.8
          },

          # ===== PREMIUM MULTISPECIALITY (ALL SYMPTOMS) =====
          {
            "name": 'Apollo Hospitals',
            "address": 'Plot No. 1A, Bhat GIDC Estate',
            "city": 'Ahmedabad',
            "pincode": '382428',
            "lat": 23.1096,
            "lng": 72.5937,
            "contact": '079-66701800',
            "specialities": [
              'Cardiology',
              'Cardiac Surgery',
              'Neurology',
              'Neurosurgery',
              'Oncology',
              'Gastroenterology',
              'Pulmonology',
              'Orthopedics',
              'Emergency',
              'ICU'
            ],
            "hospital_type": 'premium',
            "rating": 4.8,
            "acceptedSchemes": [
              { "schemeName": 'Private Insurance', "schemeId": str(uuid.uuid4()) },
              { "schemeName": 'Corporate Tie-ups', "schemeId": str(uuid.uuid4()) }
            ],
            "base_cost_factor": 1.4
          },
          {
            "name": 'CIMS Hospital',
            "address": 'Science City Road, Sola',
            "city": 'Ahmedabad',
            "pincode": '380060',
            "lat": 23.0815,
            "lng": 72.5112,
            "contact": '079-66505555',
            "specialities": [
              'Cardiology',
              'Neurology',
              'Transplants',
              'Emergency',
              'ICU',
              'General Surgery'
            ],
            "hospital_type": 'premium',
            "rating": 4.7,
            "acceptedSchemes": [
              { "schemeName": 'Private Insurance', "schemeId": str(uuid.uuid4()) },
              { "schemeName": 'Corporate Tie-ups', "schemeId": str(uuid.uuid4()) }
            ],
            "base_cost_factor": 1.35
          },

          # ===== PRIVATE MULTISPECIALITY (MID RANGE) =====
          {
            "name": 'Zydus Hospital',
            "address": 'Zydus Hospitals Road, Thaltej',
            "city": 'Ahmedabad',
            "pincode": '380054',
            "lat": 23.0642,
            "lng": 72.5156,
            "contact": '079-66190201',
            "specialities": [
              'Neurology',
              'Nephrology',
              'Gastroenterology',
              'Cardiology',
              'Endocrinology'
            ],
            "hospital_type": 'private',
            "rating": 4.7,
            "acceptedSchemes": [
              { "schemeName": 'Private Insurance', "schemeId": str(uuid.uuid4()) },
              { "schemeName": 'Ayushman Bharat PM-JAY', "schemeId": str(uuid.uuid4()) }
            ],
            "base_cost_factor": 1.2
          },
          {
            "name": 'Sterling Hospital',
            "address": 'Memnagar',
            "city": 'Ahmedabad',
            "pincode": '380052',
            "lat": 23.0497,
            "lng": 72.5317,
            "contact": '079-40011111',
            "specialities": [
              'General Surgery',
              'Urology',
              'Pulmonology',
              'General Medicine'
            ],
            "hospital_type": 'private',
            "rating": 4.5,
            "acceptedSchemes": [
              { "schemeName": 'Private Insurance', "schemeId": str(uuid.uuid4()) }
            ],
            "base_cost_factor": 1.1
          },
          {
            "name": 'SAL Hospital',
            "address": 'Drive In Road, Thaltej',
            "city": 'Ahmedabad',
            "pincode": '380054',
            "lat": 23.0536,
            "lng": 72.5179,
            "contact": '079-66121000',
            "specialities": [
              'Orthopedics',
              'Cardiology',
              'General Surgery',
              'Physiotherapy'
            ],
            "hospital_type": 'private',
            "rating": 4.2,
            "acceptedSchemes": [
              { "schemeName": 'Private Insurance', "schemeId": str(uuid.uuid4()) },
              { "schemeName": 'Mukhyamantri Amrutum Yojana', "schemeId": str(uuid.uuid4()) }
            ],
            "base_cost_factor": 1.1
          },
          {
            "name": 'Shalby Multispeciality Hospital',
            "address": 'SG Highway',
            "city": 'Ahmedabad',
            "pincode": '380015',
            "lat": 23.0358,
            "lng": 72.5025,
            "contact": '079-40203030',
            "specialities": [
              'Orthopedics',
              'Joint Replacement',
              'Spine Care',
              'Physiotherapy'
            ],
            "hospital_type": 'private',
            "rating": 4.4,
            "acceptedSchemes": [
              { "schemeName": 'Private Insurance', "schemeId": str(uuid.uuid4()) },
              { "schemeName": 'Corporate Tie-ups', "schemeId": str(uuid.uuid4()) }
            ],
            "base_cost_factor": 1.15
          },

          # ===== CANCER / SPECIAL CASES =====
          {
            "name": 'HCG Cancer Centre',
            "address": 'Sola-Science City Road',
            "city": 'Ahmedabad',
            "pincode": '380060',
            "lat": 23.0785,
            "lng": 72.5089,
            "contact": '079-40410101',
            "specialities": [
              'Oncology',
              'Radiotherapy',
              'Chemotherapy',
              'Hematology'
            ],
            "hospital_type": 'private',
            "rating": 4.6,
            "acceptedSchemes": [
              { "schemeName": 'Mukhyamantri Amrutum Yojana', "schemeId": str(uuid.uuid4()) },
              { "schemeName": 'Private Insurance', "schemeId": str(uuid.uuid4()) }
            ],
            "base_cost_factor": 1.3
          },
          {
            "name": 'Narayana Multispeciality Hospital',
            "address": 'Rakhial',
            "city": 'Ahmedabad',
            "pincode": '380023',
            "lat": 23.0218,
            "lng": 72.6229,
            "contact": '079-71238888',
            "specialities": [
              'Cardiac Surgery',
              'Emergency',
              'ICU',
              'Trauma'
            ],
            "hospital_type": 'private',
            "rating": 4.3,
            "acceptedSchemes": [
              { "schemeName": 'Ayushman Bharat PM-JAY', "schemeId": str(uuid.uuid4()) },
              { "schemeName": 'Mukhyamantri Amrutum Yojana', "schemeId": str(uuid.uuid4()) }
            ],
            "base_cost_factor": 1.2
          }
        ]

        # ===== NON-HOSPITAL FACILITY CENTERS =====
        facilities = [
          # X-Ray Centers
          {
            "name": "Ahmedabad Diagnostic X-Ray Center",
            "address": "CG Road, Navrangpura",
            "city": "Ahmedabad",
            "pincode": "380009",
            "lat": 23.0362,
            "lng": 72.5603,
            "contact": "079-26444555",
            "specialities": ["Digital X-Ray", "Dental X-Ray", "Chest X-Ray"],
            "hospital_type": "private",
            "rating": 4.2,
            "acceptedSchemes": [],
            "base_cost_factor": 0.7,
            "facility_category": "xray",
          },
          {
            "name": "Sanjivani X-Ray & Imaging",
            "address": "Maninagar",
            "city": "Ahmedabad",
            "pincode": "380008",
            "lat": 23.0031,
            "lng": 72.6021,
            "contact": "079-25431122",
            "specialities": ["X-Ray", "Fluoroscopy", "Bone Density Scan"],
            "hospital_type": "private",
            "rating": 3.9,
            "acceptedSchemes": [],
            "base_cost_factor": 0.65,
            "facility_category": "xray",
          },
          # MRI Centers
          {
            "name": "NeuroScan MRI Centre",
            "address": "Vastrapur",
            "city": "Ahmedabad",
            "pincode": "380015",
            "lat": 23.0375,
            "lng": 72.5270,
            "contact": "079-40021234",
            "specialities": ["Brain MRI", "Spine MRI", "Joint MRI", "Full Body MRI"],
            "hospital_type": "private",
            "rating": 4.5,
            "acceptedSchemes": [
              { "schemeName": "Private Insurance", "schemeId": str(uuid.uuid4()) }
            ],
            "base_cost_factor": 1.0,
            "facility_category": "mri",
          },
          {
            "name": "Prime MRI & Diagnostics",
            "address": "Satellite Road",
            "city": "Ahmedabad",
            "pincode": "380015",
            "lat": 23.0258,
            "lng": 72.5127,
            "contact": "079-26920088",
            "specialities": ["3T MRI", "Cardiac MRI", "Abdominal MRI"],
            "hospital_type": "private",
            "rating": 4.3,
            "acceptedSchemes": [],
            "base_cost_factor": 1.1,
            "facility_category": "mri",
          },
          # CT Scan Centers
          {
            "name": "City CT Scan & Diagnostic Center",
            "address": "Paldi",
            "city": "Ahmedabad",
            "pincode": "380007",
            "lat": 23.0156,
            "lng": 72.5618,
            "contact": "079-26583344",
            "specialities": ["CT Scan", "HRCT Chest", "CT Angiography", "PET-CT"],
            "hospital_type": "private",
            "rating": 4.4,
            "acceptedSchemes": [],
            "base_cost_factor": 0.9,
            "facility_category": "ct_scan",
          },
          {
            "name": "Advanced CT Imaging Hub",
            "address": "SG Highway, Bodakdev",
            "city": "Ahmedabad",
            "pincode": "380054",
            "lat": 23.0510,
            "lng": 72.5010,
            "contact": "079-40058877",
            "specialities": ["128-Slice CT", "CT Brain", "CT Abdomen"],
            "hospital_type": "private",
            "rating": 4.1,
            "acceptedSchemes": [
              { "schemeName": "Private Insurance", "schemeId": str(uuid.uuid4()) }
            ],
            "base_cost_factor": 1.05,
            "facility_category": "ct_scan",
          },
          # Physiotherapy Centers
          {
            "name": "PhysioFirst Rehabilitation Center",
            "address": "Gurukul Road",
            "city": "Ahmedabad",
            "pincode": "380052",
            "lat": 23.0422,
            "lng": 72.5345,
            "contact": "079-27442200",
            "specialities": ["Sports Rehab", "Post-Surgery Rehab", "Spine Therapy", "Neuro Rehab"],
            "hospital_type": "private",
            "rating": 4.6,
            "acceptedSchemes": [],
            "base_cost_factor": 0.8,
            "facility_category": "physiotherapy",
          },
          {
            "name": "ActiveLife Physiotherapy Clinic",
            "address": "Thaltej Cross Roads",
            "city": "Ahmedabad",
            "pincode": "380054",
            "lat": 23.0553,
            "lng": 72.5134,
            "contact": "079-48001234",
            "specialities": ["Ortho Physiotherapy", "Geriatric Care", "Pain Management"],
            "hospital_type": "private",
            "rating": 4.0,
            "acceptedSchemes": [],
            "base_cost_factor": 0.75,
            "facility_category": "physiotherapy",
          },
          # Pathology Labs
          {
            "name": "MedPath Diagnostics & Pathology Lab",
            "address": "Ashram Road, Navrangpura",
            "city": "Ahmedabad",
            "pincode": "380009",
            "lat": 23.0345,
            "lng": 72.5610,
            "contact": "079-26565000",
            "specialities": ["Blood Tests", "Urine Analysis", "Hormonal Assays", "Allergy Testing"],
            "hospital_type": "private",
            "rating": 4.4,
            "acceptedSchemes": [],
            "base_cost_factor": 0.6,
            "facility_category": "pathology",
          },
          {
            "name": "CityLab Pathology & Diagnostics",
            "address": "Satellite Road, Jodhpur Cross Roads",
            "city": "Ahmedabad",
            "pincode": "380015",
            "lat": 23.0285,
            "lng": 72.5098,
            "contact": "079-26920088",
            "specialities": ["Complete Blood Count", "Liver Function", "Kidney Function", "Thyroid Panel"],
            "hospital_type": "private",
            "rating": 4.1,
            "acceptedSchemes": [],
            "base_cost_factor": 0.55,
            "facility_category": "pathology",
          },
        ]

        for h_data in hospitals:
            Hospital.objects.create(**h_data)

        for f_data in facilities:
            Hospital.objects.create(**f_data)
        
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(hospitals)} hospitals and {len(facilities)} facility centers'))
