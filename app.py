import json

def load_data():
    try:
        # We are still using the filename 'veriler.json' for now
        with open('data.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: data.json file not found!")
        return {}

def assistant():
    data = load_data()
    print("--- Welcome to Food Innovation Assistant ---")
    
    while True:
        ingredient = input("\nEnter an ingredient (or 'q' to quit): ").capitalize()
        
        if ingredient.lower() == 'q':
            print("Goodbye!")
            break
            
        if ingredient in data:
            pairings = ", ".join(data[ingredient])
            print(f"> {ingredient} pairs well with: {pairings}")
        else:
            print(f"> Sorry, no pairing info for '{ingredient}' yet.")

if __name__ == "__main__":
    assistant()