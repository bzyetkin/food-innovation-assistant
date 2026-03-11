import json

def load_data():
    try:
        with open('data.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

def assistant():
    data = load_data()
    print("--- Welcome to Food Innovation Assistant v2.0 ---")
    print("(I can now learn new pairings!)")
    
    while True:
        ingredient = input("\nEnter an ingredient (or 'q' to quit): ").capitalize()
        
        if ingredient.lower() == 'q':
            print("Goodbye!")
            break
            
        if ingredient in data:
            pairings = ", ".join(data[ingredient])
            print(f"> {ingredient} pairs well with: {pairings}")
        else:
            print(f"> I don't know '{ingredient}' yet.")
            answer = input(f"What goes well with {ingredient}? (Separate with commas or press Enter to skip): ")
            
            if answer:
                # Yeni malzemeyi listeye ekliyoruz
                new_pairings = [item.strip().capitalize() for item in answer.split(",")]
                data[ingredient] = new_pairings
                save_data(data) # Dosyaya kaydediyoruz
                print(f"> Thanks! I've learned that {ingredient} pairs with {', '.join(new_pairings)}.")

if __name__ == "__main__":
    assistant()
    