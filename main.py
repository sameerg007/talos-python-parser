import sys
import json
from src.intelligence import IntelEngine

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python3 main.py <path_to_log>"}, indent=2))
        sys.exit(1)

    log_path = sys.argv[1]
    kb_path = 'data/knowledge_base.json'

    try:
        # Instantiate the engine
        engine = IntelEngine(kb_path)
        
        # Run the analysis
        diagnostic_report = engine.analyze_log(log_path)

        # Print the exact JSON object you wanted
        print(json.dumps(diagnostic_report, indent=2))

    # Senior-level Exception Handling (Outputted as JSON to maintain data integrity)
    except FileNotFoundError as e:
        print(json.dumps({"error": f"Critical Error: File not found - {e.filename}"}, indent=2))
    except PermissionError as e:
        print(json.dumps({"error": f"Critical Error: Permission denied for - {e.filename}"}, indent=2))
    except Exception as e:
        print(json.dumps({"error": f"System Engine Failure: {str(e)}"}, indent=2))

if __name__ == "__main__":
    main()
