import os
import json
import base64
import hashlib
import google.generativeai as genai
from functools import lru_cache
from dotenv import load_dotenv
from core.utils.gemini_keys import key_manager

load_dotenv()

@lru_cache(maxsize=512)
def _cached_api_call(func_name, input_hash):
    """
    LRU cache wrapper to store results by key mapping to avoid repeating identical prompt calls.
    Since we need serialization/deserialization for dict responses, we store as JSON string.
    """
    pass

# We implement a helper function to call Gemini with specific configuration
def _call_gemini_model(api_key, prompt, image_part=None):
    if not api_key:
        raise ValueError("API key is empty")
    
    genai.configure(api_key=api_key)
    
    # temperature=0 ensures fully deterministic responses
    generation_config = genai.types.GenerationConfig(
        temperature=0.0,
        top_p=1.0,
        top_k=1,
    )
    
    model = genai.GenerativeModel(
        'gemini-2.5-flash',
        generation_config=generation_config
    )
    
    if image_part:
        response = model.generate_content([prompt, image_part])
    else:
        response = model.generate_content(prompt)
        
    return response.text

# We will cache symptom analysis results as it takes plain text query
# To bypass dict mutation issues with lru_cache, we store as serialized JSON
_symptom_cache = {}

def get_cached_symptoms(symptoms_text, city, response_language):
    cache_key = hashlib.md5(f"{symptoms_text}||{city}||{response_language}".encode('utf-8')).hexdigest()
    if cache_key in _symptom_cache:
        return _symptom_cache[cache_key]
    return None

def set_cached_symptoms(symptoms_text, city, response_language, result):
    cache_key = hashlib.md5(f"{symptoms_text}||{city}||{response_language}".encode('utf-8')).hexdigest()
    _symptom_cache[cache_key] = result

def analyze_symptoms(symptoms_text, city, response_language='English'):
    # Check cache first
    cached = get_cached_symptoms(symptoms_text, city, response_language)
    if cached:
        return cached

    input_json = json.dumps({
        "symptoms_text": symptoms_text,
        "location": city or ""
    })

    # Language instruction
    lang_instruction = (
        f"IMPORTANT: Respond in {response_language}. All string values in the JSON must be written in {response_language}."
        if response_language != 'English' else ''
    )
    
    prompt = f"""You are a concise, safety-first medical triage assistant. Output JSON only.
You are trained in Indian medical standards and common diseases in India.
{lang_instruction}

Task: Carefully analyze the given symptoms_text. Consider:
1. The combination and severity of all symptoms together (not individually).
2. Common diseases in India matching this symptom profile.
3. The patient's location for region-specific diseases (e.g., dengue/malaria in monsoon areas, specific infections).
4. Return up to 3 possible diseases ranked by probability, a single medical speciality, urgency (low|medium|high), and confidence.

Input:
{input_json}

Return EXACT JSON:
{{
  "possible_diseases":[
    {{"name":"<string>","probability":<0.0-1.0>,"notes":"<<= 12 words justification>"}}
  ],
  "speciality":"<single string>",
  "urgency":"low|medium|high",
  "confidence":<0.0-1.0>
}}

Rules:
- Use cautious phrasing; this is not a diagnosis.
- Consider symptom combinations holistically, not each symptom in isolation.
- Prioritize the most clinically likely diagnosis based on Indian epidemiology.
- For ambiguous symptoms, recommend General Medicine and set confidence lower.
- If emergency signs (severe chest pain + sweating + fainting / severe breathlessness / heavy bleeding) then urgency="high".
- Output valid JSON only."""

    def _execute(api_key):
        return _call_gemini_model(api_key, prompt)

    try:
        text_content = key_manager.call_with_failover(_execute)
        
        # Clean markdown code blocks if present
        if "```json" in text_content:
            text_content = text_content.replace("```json", "").replace("```", "")
        elif "```" in text_content:
            text_content = text_content.replace("```", "")
            
        parsed_result = json.loads(text_content.strip())
        set_cached_symptoms(symptoms_text, city, response_language, parsed_result)
        return parsed_result
        
    except Exception as e:
        print(f"Gemini analysis error: {e}")
        return get_default_response(symptoms_text)

def get_default_response(symptoms_text=''):
    symptoms = symptoms_text.lower()
    
    diseases = []
    speciality = "General Medicine"
    urgency = "low"
    
    # Fever-related
    if 'fever' in symptoms:
        if any(x in symptoms for x in ['joint', 'muscle', 'pain']):
            diseases.append({"name": "Dengue Fever", "probability": 0.6, "notes": "Fever with joint/muscle pain"})
            diseases.append({"name": "Viral Infection", "probability": 0.3, "notes": "Common viral symptoms"})
            urgency = "medium"
        else:
            diseases.append({"name": "Viral Fever", "probability": 0.7, "notes": "Common fever symptoms"})
            diseases.append({"name": "Flu", "probability": 0.2, "notes": "Influenza-like illness"})
        speciality = "General Medicine"
        
    # Chest pain
    elif 'chest' in symptoms and 'pain' in symptoms:
        diseases.append({"name": "Angina", "probability": 0.5, "notes": "Chest pain, needs evaluation"})
        diseases.append({"name": "Gastritis", "probability": 0.3, "notes": "Acid reflux related"})
        speciality = "Cardiology"
        urgency = "high"
        
    # Headache
    elif 'headache' in symptoms or 'head' in symptoms:
        diseases.append({"name": "Tension Headache", "probability": 0.6, "notes": "Common headache"})
        diseases.append({"name": "Migraine", "probability": 0.3, "notes": "Severe headache"})
        speciality = "Neurology"
        
    # Stomach
    elif any(x in symptoms for x in ['stomach', 'abdominal', 'vomit']):
        diseases.append({"name": "Gastroenteritis", "probability": 0.6, "notes": "Stomach infection"})
        diseases.append({"name": "Food Poisoning", "probability": 0.3, "notes": "Food-related illness"})
        speciality = "Gastroenterology"
        
    # Cough/cold
    elif 'cough' in symptoms or 'cold' in symptoms:
        diseases.append({"name": "Upper Respiratory Infection", "probability": 0.7, "notes": "Common cold"})
        diseases.append({"name": "Bronchitis", "probability": 0.2, "notes": "Chest infection"})
        speciality = "General Medicine"
        
    else:
        diseases.append({"name": "General Checkup Recommended", "probability": 0.5, "notes": "Consult a doctor"})
        
    return {
        "possible_diseases": diseases,
        "speciality": speciality,
        "urgency": urgency,
        "confidence": 0.5
    }


# ─── Lab Report Analyser ──────────────────────────────────────────────────────

def analyze_lab_report(file_bytes: bytes, mime_type: str, filename: str = "", response_language: str = 'English'):
    """Send a lab report image/PDF to Gemini Vision and get a structured analysis."""
    
    # Language instruction
    lang_instruction = (
        f"IMPORTANT: Respond in {response_language}. All explanatory text fields (simple_explanation, overall_summary, explanation, cause, recommendation, disclaimer) must be written in {response_language}."
        if response_language != 'English' else ''
    )

    prompt = f"""
You are a medical lab report interpreter helping a patient understand their report.
You must be precise with numerical comparisons - carefully check each value against the normal range.
Mark a parameter as "high" ONLY if the patient's value exceeds the upper bound of the normal range.
Mark as "low" ONLY if it is below the lower bound.
If the value is within the normal range, mark it as "normal" - even if it is near the boundary.

{lang_instruction}
Analyze the uploaded lab report image/document and return ONLY valid JSON in this exact format:

{{
  "report_type": "<e.g. Complete Blood Count, Lipid Profile, Thyroid Panel>",
  "parameters": [
    {{
      "name": "<test name>",
      "value": "<patient's value with unit>",
      "normal_range": "<normal range with unit>",
      "status": "normal|high|low",
      "simple_explanation": "<1-2 sentences in simple language>"
    }}
  ],
  "overall_summary": "<2-3 sentence plain-language summary of the overall report>",
  "possible_conditions": [
    {{
      "name": "<condition name>",
      "likelihood": "possible|likely|unlikely",
      "explanation": "<plain language explanation in 1-2 sentences>",
      "cause": "<what typically causes this condition>"
    }}
  ],
  "recommendation": "<brief advice on next steps>",
  "disclaimer": "This analysis is AI-generated for informational purposes only and is not a medical diagnosis. Please consult a qualified doctor."
}}

Rules:
- Use simple, non-technical language a patient can understand.
- status must be exactly: normal, high, or low.
- If the image is not a lab report or is unreadable, return {{"error": "Could not read a valid lab report from this file."}}.
- Output valid JSON only, no markdown fences.
"""

    b64 = base64.b64encode(file_bytes).decode('utf-8')
    image_part = {"inline_data": {"mime_type": mime_type, "data": b64}}

    def _execute(api_key):
        return _call_gemini_model(api_key, prompt, image_part=image_part)

    try:
        text = key_manager.call_with_failover(_execute).strip()

        # Strip accidental markdown fences
        if text.startswith("```"):
            text = text.split("\n", 1)[-1]
            text = text.rsplit("```", 1)[0]

        return json.loads(text)

    except Exception as e:
        print(f"Lab report analysis error: {e}")
        return get_default_lab_response()


def get_default_lab_response():
    return {
        "error": "Analysis temporarily unavailable. Please try again or check your API key."
    }


def translate_lab_result(result: dict, target_language: str) -> dict:
    """
    Translate the human-readable text fields in a lab report result dict
    into `target_language` using a focused Gemini call.
    Medical values, normal_range, status, and likelihood are kept as-is.
    Returns the original result on any failure (graceful degradation).
    """
    if not result or 'error' in result or target_language == 'English':
        return result

    # Build a flat dict of translatable texts keyed by a unique identifier
    to_translate = {}
    to_translate['report_type'] = result.get('report_type', '')
    to_translate['overall_summary'] = result.get('overall_summary', '')
    to_translate['recommendation'] = result.get('recommendation', '')
    to_translate['disclaimer'] = result.get('disclaimer', '')

    for i, p in enumerate(result.get('parameters', [])):
        to_translate[f'param_{i}_explanation'] = p.get('simple_explanation', '')

    for i, c in enumerate(result.get('possible_conditions', [])):
        to_translate[f'condition_{i}_name'] = c.get('name', '')
        to_translate[f'condition_{i}_explanation'] = c.get('explanation', '')
        to_translate[f'condition_{i}_cause'] = c.get('cause', '')

    source_json = json.dumps(to_translate, ensure_ascii=False)

    prompt = f"""You are a medical translator. Translate the following JSON values from English to {target_language}.
Return ONLY a JSON object with the EXACT same keys, with the values translated to {target_language}.
Do NOT translate the keys. Do NOT add or remove any keys. Do NOT include markdown fences.

Source JSON:
{source_json}"""

    def _execute(api_key):
        return _call_gemini_model(api_key, prompt)

    try:
        text = key_manager.call_with_failover(_execute).strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[-1]
            text = text.rsplit("```", 1)[0]
        translated = json.loads(text)
    except Exception as e:
        print(f"Translation error: {e}")
        return result  # graceful fallback - return English result

    # Merge translated values back into the result
    out = dict(result)
    out['report_type']     = translated.get('report_type', result.get('report_type', ''))
    out['overall_summary'] = translated.get('overall_summary', result.get('overall_summary', ''))
    out['recommendation']  = translated.get('recommendation', result.get('recommendation', ''))
    out['disclaimer']      = translated.get('disclaimer', result.get('disclaimer', ''))

    new_params = []
    for i, p in enumerate(result.get('parameters', [])):
        new_p = dict(p)
        key = f'param_{i}_explanation'
        if key in translated:
            new_p['simple_explanation'] = translated[key]
        new_params.append(new_p)
    out['parameters'] = new_params

    new_conditions = []
    for i, c in enumerate(result.get('possible_conditions', [])):
        new_c = dict(c)
        if f'condition_{i}_name' in translated:
            new_c['name'] = translated[f'condition_{i}_name']
        if f'condition_{i}_explanation' in translated:
            new_c['explanation'] = translated[f'condition_{i}_explanation']
        if f'condition_{i}_cause' in translated:
            new_c['cause'] = translated[f'condition_{i}_cause']
        new_conditions.append(new_c)
    out['possible_conditions'] = new_conditions

    return out
