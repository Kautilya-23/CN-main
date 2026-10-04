import os
import threading
from pathlib import Path
from dotenv import load_dotenv
import google.api_core.exceptions

# Always load .env before reading keys — this file is imported as a singleton
# before gemini.py's load_dotenv() has a chance to run
load_dotenv(Path(__file__).resolve().parents[2] / '.env')

class GeminiKeyManager:
    def __init__(self):
        # Read the keys from environment
        keys_env = [
            os.getenv("GEMINI_API_KEY_1"),
            os.getenv("GEMINI_API_KEY_2"),
            os.getenv("GEMINI_API_KEY_3"),
            os.getenv("GEMINI_API_KEY") # fallback to single key if exists
        ]
        # Filter out empty or None values
        self.keys = [k for k in keys_env if k]
        self._index = 0
        self._lock = threading.Lock()

    def get_next_key(self) -> str:
        if not self.keys:
            return ""
        with self._lock:
            key = self.keys[self._index % len(self.keys)]
            self._index += 1
            return key

    def call_with_failover(self, func, *args, **kwargs):
        """
        Executes func(api_key, *args, **kwargs) by cycling through available keys
        if a google.api_core.exceptions.ResourceExhausted or similar API error is encountered.
        """
        if not self.keys:
            # Fallback behavior if no keys configured
            return func("", *args, **kwargs)

        last_error = None
        # Try at most as many times as the number of keys we have
        attempts = len(self.keys)
        for _ in range(attempts):
            key = self.get_next_key()
            try:
                return func(key, *args, **kwargs)
            except google.api_core.exceptions.ResourceExhausted as e:
                print(f"Gemini API key exhausted. Retrying with next key. Error: {e}")
                last_error = e
                continue
            except Exception as e:
                # If it's a general exception that might not be resource exhaust, we check if it looks like a quota limit
                err_str = str(e).lower()
                if "quota" in err_str or "exhausted" in err_str or "429" in err_str:
                    print(f"Detected potential quota exhaustion. Retrying with next key. Error: {e}")
                    last_error = e
                    continue
                # For other errors, raise immediately
                raise e

        # If all keys failed, raise the last error
        if last_error:
            raise last_error
        raise Exception("No active Gemini API keys available.")

key_manager = GeminiKeyManager()
