import re
import json

def extract_functions_key_values(file_path):

    try:
        with open(file_path, 'r') as file:
            content = file.read()
        
        pattern = r'<function>(.*?)</function>'
        matches = re.findall(pattern, content, re.DOTALL)
        results = []

        
        for i, match in enumerate(matches, 1):
            try:
                json_obj = json.loads(match.strip())
                
                def flatten_json(obj, prefix=""):
                    flattened = {}

                    
                    if isinstance(obj, dict):
                        for key, value in obj.items():
                            current_key = f"{prefix}.{key}" if prefix else key
                            
                            if isinstance(value, (dict, list)):
                                nested = flatten_json(value, current_key)
                                flattened.update(nested)
                            else:
                                flattened[current_key] = value
                    
                    elif isinstance(obj, list):
                        for i, item in enumerate(obj):
                            current_key = f"{prefix}[{i}]"
                            
                            if isinstance(item, (dict, list)):
                                nested = flatten_json(item, current_key)
                                flattened.update(nested)
                            else:
                                flattened[current_key] = item
                    
                    return flattened
                
                function_data = {
                    "function_index": i,
                    "key_values": flatten_json(json_obj)
                }
                
                results.append(function_data)
                
            except json.JSONDecodeError as e:
                print(f"Warning: Invalid JSON in function {i}: {e}")
                continue
        
        return results
        
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")

if __name__ == "__main__":
    key_value_pairs = extract_functions_key_values("cursor agent.txt")
    for func in key_value_pairs:
        print(f"Number of headers here:  {func['function_index']}")
        print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        for key, value in func['key_values'].items():
            print(f"  {key}: {value}")
            print()
                