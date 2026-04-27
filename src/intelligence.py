# # import json
# # import os
# # import re

# # class IntelEngine:
# #     def __init__(self, kb_path):
# #         with open(kb_path, 'r') as f:
# #             self.kb = json.load(f)

# #     def analyze_log(self, log_path):
# #         if not os.path.exists(log_path):
# #             return {"error": "Target log file not found."}

# #         report = []
# #         with open(log_path, 'r') as f:
# #             for line in f:
# #                 # 1. Standard Knowledge Base Check (SOPs)
# #                 line_upper = line.upper()
# #                 for marker, intel in self.kb.items():
# #                     if marker in line_upper:
# #                         report.append({"issue": marker, "diagnostic": intel})
                
# #                 # 2. Timing Path Anomaly Detection (The "Architect" Logic)
# #                 if "INST" in line:
# #                     # Extracts content inside each {}
# #                     fields = re.findall(r'\{(.*?)\}', line)
                    
# #                     if len(fields) >= 8:
# #                         try:
# #                             cell_name = fields[0]
# #                             cell_type = fields[6]
# #                             delay = float(fields[7])
                            
# #                             # Flag any cell with delay > 0.150ns as a bottleneck
# #                             if delay > 0.150:
# #                                 report.append({
# #                                     "issue": f"HIGH DELAY: {cell_type}",
# #                                     "diagnostic": {
# #                                         "severity": "CRITICAL",
# #                                         "impact": f"Cell {cell_name} is causing a {delay}ns stall.",
# #                                         "resolution": "Check fanout or replace with higher drive strength cell.",
# #                                         "sop": "PD-OPT-AUTO"
# #                                     }
# #                                 })
# #                         except (ValueError, IndexError):
# #                             continue
# #         return report
# # import json
# # import os

# # class IntelEngine:
# #     def __init__(self, kb_path):
# #         self.kb_path = kb_path
# #         # The Intelligence Layer: Expanded keywords for NXP
# #         self.keywords = ["ERROR", "FATAL", "VIOLATION", "FAIL"]

# #     def analyze_log(self, log_path):
# #         diagnostic_report = []
        
# #         # Guard clause: If file doesn't exist, return empty to prevent crash
# #         if not os.path.exists(log_path):
# #             return diagnostic_report

# #         try:
# #             with open(log_path, 'r') as file:
# #                 for line_num, line in enumerate(file, 1):
# #                     # Standardize to uppercase for robust matching
# #                     upper_line = line.upper()
                    
# #                     for key in self.keywords:
# #                         if key in upper_line:
# #                             # Construct the JSON-type object
# #                             entry = {
# #                                 "line": line_num,
# #                                 "type": key,
# #                                 "content": line.strip()
# #                             }
# #                             diagnostic_report.append(entry)
# #                             break # Move to next line after finding one match
                            
# #         except Exception:
# #             # If an error occurs during reading, return whatever we found
# #             pass
            
# #         return diagnostic_report


# import json
# import os
# import re

# class IntelEngine:
#     def __init__(self, kb_path):
#         # Added a try-except here to prevent the demo from crashing if the path is wrong
#         try:
#             with open(kb_path, 'r') as f:
#                 self.kb = json.load(f)
#         except:
#             self.kb = {}

#     def analyze_log(self, log_path):
#         if not os.path.exists(log_path):
#             return [{"issue": "SYSTEM", "diagnostic": "Target log file not found."}]

#         report = []
#         # Define high-priority keywords that must ALWAYS be caught
#         critical_keywords = ["ERROR", "FATAL", "VIOLATION", "FAIL"]

#         with open(log_path, 'r') as f:
#             for line_num, line in enumerate(f, 1):
#                 line_upper = line.upper()
#                 line_flagged = False
                
#                 # 1. Standard Knowledge Base Check (SOPs)
#                 for marker, intel in self.kb.items():
#                     if marker in line_upper:
#                         report.append({
#                             "line": line_num,
#                             "issue": marker, 
#                             "diagnostic": intel
#                         })
#                         line_flagged = True
                
#                 # 2. Universal Keyword Catch-all (The "Safety Net")
#                 # If Logic 1 missed it, Logic 2 checks for general critical words
#                 if not line_flagged:
#                     for key in critical_keywords:
#                         if key in line_upper:
#                             report.append({
#                                 "line": line_num,
#                                 "issue": key,
#                                 "diagnostic": {
#                                     "severity": "HIGH",
#                                     "content": line.strip(),
#                                     "resolution": "Unmapped issue. Manual inspection required."
#                                 }
#                             })
#                             line_flagged = True
#                             break

#                 # 3. Timing Path Anomaly Detection (The "Architect" Logic)
#                 # We keep this strictly for "INST" lines as per your original design
#                 if "INST" in line:
#                     fields = re.findall(r'\{(.*?)\}', line)
#                     if len(fields) >= 8:
#                         try:
#                             cell_name = fields[0]
#                             cell_type = fields[6]
#                             delay = float(fields[7])
#                             if delay > 0.150:
#                                 report.append({
#                                     "line": line_num,
#                                     "issue": f"HIGH DELAY: {cell_type}",
#                                     "diagnostic": {
#                                         "severity": "CRITICAL",
#                                         "impact": f"Cell {cell_name} is causing a {delay}ns stall.",
#                                         "resolution": "Check fanout or replace with higher drive strength cell.",
#                                         "sop": "PD-OPT-AUTO"
#                                     }
#                                 })
#                         except (ValueError, IndexError):
#                             continue
#         return report


import json
import os
import re

class IntelEngine:
    def __init__(self, kb_path):
        try:
            with open(kb_path, 'r') as f:
                self.kb = json.load(f)
        except:
            self.kb = {}

    def analyze_log(self, log_path):
        if not os.path.exists(log_path):
            return [{"issue": "SYSTEM", "diagnostic": "Target log file not found."}]

        report = []
        # Added 'SPACING' to catch Image 1 even without the Regex match
        critical_keywords = ["ERROR", "FATAL", "VIOLATION", "FAIL", "SPACING"]
        
        # Regex to detect Cadence Innovus DRC patterns like "SPACING: ("
        drc_pattern = re.compile(r"^([A-Z_]+):\s*\(")

        with open(log_path, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line_upper = line.upper()
                clean_line = line.strip()
                line_flagged = False
                
                # 1. Standard Knowledge Base Check (SOPs)
                for marker, intel in self.kb.items():
                    if marker in line_upper:
                        report.append({
                            "line": line_num,
                            "issue": marker, 
                            "diagnostic": intel
                        })
                        line_flagged = True
                        break # Optimization: One match is enough
                
                # 2. Physical Design DRC Detection (The Image 1 Fix)
                if not line_flagged:
                    drc_match = drc_pattern.search(clean_line)
                    if drc_match:
                        violation_type = drc_match.group(1)
                        report.append({
                            "line": line_num,
                            "issue": violation_type,
                            "diagnostic": {
                                "severity": "CRITICAL",
                                "content": clean_line,
                                "resolution": self.kb.get(violation_type, "DRC breach detected. Check layout coordinates.")
                            }
                        })
                        line_flagged = True

                # 3. Universal Keyword Catch-all (The "Safety Net")
                if not line_flagged:
                    for key in critical_keywords:
                        if key in line_upper:
                            report.append({
                                "line": line_num,
                                "issue": key,
                                "diagnostic": {
                                    "severity": "HIGH",
                                    "content": clean_line,
                                    "resolution": "Unmapped issue. Manual inspection required."
                                }
                            })
                            line_flagged = True
                            break

                # 4. Timing Path Anomaly Detection (The "Architect" Logic)
                if "INST" in line:
                    fields = re.findall(r'\{(.*?)\}', line)
                    if len(fields) >= 8:
                        try:
                            cell_name = fields[0]
                            cell_type = fields[6]
                            delay = float(fields[7])
                            if delay > 0.150:
                                report.append({
                                    "line": line_num,
                                    "issue": f"HIGH DELAY: {cell_type}",
                                    "diagnostic": {
                                        "severity": "CRITICAL",
                                        "impact": f"Cell {cell_name} is causing a {delay}ns stall.",
                                        "resolution": "Check fanout or replace with higher drive strength cell.",
                                        "sop": "PD-OPT-AUTO"
                                    }
                                })
                        except (ValueError, IndexError):
                            continue
                            
        return report