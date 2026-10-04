# CareNavigator Architecture Documentation

This document describes the architectural design, component division, data flow, and key integration patterns of the CareNavigator application.

## High-Level Architecture

CareNavigator follows the classic Model-View-Template (MVT) architecture pattern provided by the Django framework. The backend manages data persistence, processes API request handlers, handles translations, and orchestrates calls to external AI services (Google Gemini API). The frontend is built using Vanilla CSS and JavaScript, structured around dynamically updated DOM components that consume the backend JSON APIs.

```
+-------------------------------------------------------------+
|                        Client Browser                       |
|  +--------------------+ +-------------------+               |
|  | Web UI (HTML/CSS)  | | Vanilla JS Client |               |
|  +---------+----------+ +---------+---------+               |
+------------|----------------------|-------------------------+
             | HTML Pages           | JSON API (Fetch)
             v                      v
+------------|----------------------|-------------------------+
|            |                      |                         |
|  +---------v----------+ +---------v---------+  Django Web    |
|  | Template Engine    | | JSON View APIs    |  Application  |
|  +---------+----------+ +---------+---------+  Server       |
|            |                      |                         |
|            |                      +--------+                |
|            |                               |                |
|            +---------------+               |                |
|                            |               |                |
|                      +-----v---------------v-----+          |
|                      |  Business Logic (Views)   |          |
|                      +-----+---------------+-----+          |
|                            |               |                |
+----------------------------|---------------|----------------+
                             | ORM Queries   | API Calls
                             v               v
                     +-------v------+ +------v-------+
                     | SQLite DB    | | Gemini AI   |
                     +--------------+ +--------------+
```

---

## 1. Data Layer (Models)

The database schema is defined in `core/models.py` and maps to a SQLite database. There are three main models:

### Hospital
Stores comprehensive records for each medical facility, containing metadata and capacity details.
- **Attributes**: Name, address, city, pincode, lat/lng coordinates, contact information.
- **Specialities**: Stored as a list of strings within a Django `JSONField` (e.g., Cardiologist, Pediatrician).
- **Accepted Schemes**: List of objects containing accepted health schemes (`JSONField`).
- **Capacity**: Total beds, ICU beds, and emergency beds (`IntegerField`).
- **Facilities**: A JSON object mapping equipment availability (`xray`, `mri`, `ct_scan`, etc.).
- **Base Cost Factor**: A multiplier used by the Cost Estimator to scale treatment costs relative to hospital tiers.

### Doctor
Represents specialist consultants linked to specific hospitals.
- **Attributes**: Name, qualification, specialization, experience in years, and consultation days.
- **Relationship**: Many-to-One relationship to `Hospital` (`ForeignKey`).

### LabReportHistory
Saves previous lab report uploads and their corresponding AI analysis results.
- **Attributes**: Filename, analysis (full Gemini JSON response stored in `JSONField`), and creation timestamp.

---

## 2. Business Logic and View Layers

View endpoints in `core/views.py` handle both template rendering and API routes:

- **Template Views**:
  - `index`: Renders the main dashboard template (`core/index.html`).
  - `lab_report`: Renders the file upload page for lab reports.
  - `hospital_detail`: Dynamically fetches and displays complete details of a specific hospital, including listed specialist doctors and available beds.

- **API Views**:
  - `analyze_symptoms`: Accepts a POST request with symptoms text and location. Detects the active session locale and passes the query to the Gemini AI client. Returns JSON containing structured diagnosis and recommended specialities.
  - `search_hospitals`: Accepts GET query parameters (`speciality`, `city`, `disease`, `budget`). Queries hospitals filtering by city, validates specialities lists programmatically, computes treatment costs, and filters results based on budget constraints.

---

## 3. Cost Range Estimator

The logic in `core/utils/cost.py` estimates the pricing for medical treatments:
- **Base Costs**: Configured in a local database mapping disease tags to base treatment costs.
- **City Multipliers**: Multiplies cost based on geographic regions (e.g., Tier-1 vs Tier-2 cities).
- **Hospital Scaling**: Applies the `base_cost_factor` from the target `Hospital` model.
- **Formula**:
  $$\text{Estimated Cost} = \text{Disease Base Cost} \times \text{City Multiplier} \times \text{Hospital Base Cost Factor}$$

---

## 4. Gemini AI Integration

The system accesses Gemini AI via `core/utils/gemini.py` using structured system prompts to control output formatting:
- **Symptom Analyzer**: Guides Gemini to return JSON containing possible causes, severity, and the recommended clinical speciality, while adhering to the request language.
- **Lab Analyzer**: Prompts the AI model to parse uploaded images/PDF data, identify abnormal values, list reference ranges, and output a simplified explanation.
- **Translation Wrapper**: Automates direct text translations for cross-lingual support.

---

## 5. Multilingual and Localization (i18n)

CareNavigator uses Django's built-in translation system (`django.middleware.locale.LocaleMiddleware`):
- **Translation Catalogs**: Stored in `locale/<lang_code>/LC_MESSAGES/django.po`.
- **Supported Languages**: English (`en`), Hindi (`hi`), Marathi (`mr`), Gujarati (`gu`), Punjabi (`pa`), Bengali (`bn`), Tamil (`ta`), and Telugu (`te`).
- **Compilation**: Translates human-readable `.po` files to machine-readable `.mo` binaries used by the Django translation engine during runtime.

---

## 6. Frontend Architecture

The client-side architecture is implemented in `static/js/app.js` using vanilla JavaScript:
- **State Management**: Local state object handles the active symptoms text, analyzed specialities, location coordinates, and results lists.
- **Caching**: Leverages browser LocalStorage to cache analysis results, minimizing redundant API requests.
- **Voice API**: Interacts with the browser's native Web Speech API to provide speech-to-text input capability.
- **User Interactions**: Triggers asynchronous network requests using the `fetch` API, updating components dynamically without requiring page refreshes.
