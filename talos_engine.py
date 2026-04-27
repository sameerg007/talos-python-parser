import sys
import json
import os

def load_kb(path):
    """Graceful loading of the Intelligence Layer."""
    if not os.path.exists(path):
        # Create a default if missing to ensure the demo NEVER crashes
        default = {"ERROR": "Critical Signal Failure.", "VIOLATION": "Timing Slack Violation."}
        with open(path, 'w') as f:
            json.dump(default, f, indent=4)
        return default
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except:
        return {}

def main():
    # Maintain your existing terminal path functionality
    if len(sys.argv) < 2:
        print("Usage: python3 talos_engine.py <log_file_path>")
        sys.exit(1)

    log_path = sys.argv[1]
    kb_path = "knowledge_base.json"
    kb = load_kb(kb_path)
    
    # Expanded Keyword Intelligence
    keywords = ["ERROR", "FATAL", "VIOLATION", "FAIL"]
    
    print(f"--- TALOS Engine v2.0: Analyzing {log_path} ---")

    # Robust Exception Handling for File Access
    try:
        with open(log_path, 'r') as file:
            for line_num, line in enumerate(file, 1):
                clean_line = line.upper()
                
                # Intelligent Multi-Keyword Matching
                for key in keywords:
                    if key in clean_line:
                        resolution = kb.get(key, "SOP: Escalate to Senior Architect.")
                        print(f"\n[!] {key} Detected (Line {line_num})")
                        print(f"    LOG: {line.strip()}")
                        print(f"    RES: {resolution}")
                        break
        
        print("\n--- Analysis Complete ---")

    except FileNotFoundError:
        print(f"CRITICAL ERROR: The path '{log_path}' is invalid.")
    except Exception as e:
        print(f"SYSTEM ERROR: {e}")

if __name__ == "__main__":
    main()
