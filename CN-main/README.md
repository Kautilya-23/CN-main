# CareNavigator

CareNavigator is a Django-based healthcare assistant application designed to guide patients by analyzing symptoms, explaining lab reports in plain language, and matching them with relevant local hospitals, specialist doctors, and estimated treatment costs. The application uses Google Gemini AI to provide personalized health guidance in multiple languages.

## Key Features

- **Symptom Analysis**: Users describe their symptoms in plain language to receive an AI-powered assessment of potential conditions, recommended medical specialities, and level of urgency (e.g., routine, urgent, emergency).
- **Lab Report Explanation**: Users upload lab report documents or images to receive a clear translation of complex medical jargon into easy-to-understand explanations.
- **Multilingual Support**: Supports English, Hindi, Marathi, Gujarati, Punjabi, Bengali, Tamil, and Telugu. The AI agent adapts its response language to match the user's active session locale.
- **Hospital Directory**: Locates hospitals by city and speciality, providing contact info, coordinates, rating, bed availability (total, ICU, emergency), facilities (MRI, CT Scan, Blood Bank, etc.), and accepted health schemes.
- **Treatment Cost Estimator**: Computes cost ranges for specific conditions based on disease definitions, regional multipliers, and hospital pricing structures.
- **Speech Recognition**: Voice-input option on the web UI to dictate symptoms or search queries.

## Tech Stack

- **Backend**: Django 4.2+ (Python)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript (integrated with Django Templates and Django's i18n system)
- **Database**: SQLite (default database configuration)
- **AI Integration**: Google Gemini API via the `google-generativeai` SDK
- **Styling**: Vanilla CSS with modern responsive design principles

## Project Structure

```
CareNavigator/
├── CareNavigator_Django/     # Settings, URL routing, and WSGI/ASGI configurations
├── core/                     # Application logic
│   ├── templates/            # HTML templates and UI partials
│   ├── utils/                # Utility modules (Gemini API wrappers, cost estimators, etc.)
│   ├── models.py             # Database schemas (Hospital, Doctor, LabReportHistory)
│   └── views.py              # Request handlers
├── locale/                   # Multilingual translation binaries (.mo) and source catalogs (.po)
├── static/                   # Static resources (CSS, JS, images)
├── manage.py                 # Django command-line execution entry point
├── package.json              # Frontend package configuration (TailwindCSS/PostCSS compilation)
└── tailwind.config.js        # Styling configuration
```

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- Node.js (for compiled frontend assets, if necessary)
- Pip (Python Package Installer)

### Installation Steps

1. **Clone the repository and navigate into the project directory**:
   ```bash
   cd CareNavigator
   ```

2. **Set up a Python Virtual Environment**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   # If a requirements.txt is not yet defined, install key dependencies:
   # pip install django google-generativeai python-dotenv
   ```

4. **Environment Variables**:
   Create a `.env` file in the root directory and configure the Gemini API key and other secrets:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   SECRET_KEY=your_django_secret_key
   DEBUG=True
   ```

5. **Database Migrations**:
   Run the migrations to create the database schemas:
   ```bash
   python manage.py migrate
   ```

6. **Seed Sample Data (Optional)**:
   If there is a data migration or seeding script, run it to populate hospitals and doctors:
   ```bash
   python manage.py loaddata initial_data.json
   ```

7. **Compile Translation Messages**:
   Make sure all translations are compiled before running the server:
   ```bash
   python manage.py compilemessages
   ```

8. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```
   Open `http://127.0.0.1:8000/` in your browser.
