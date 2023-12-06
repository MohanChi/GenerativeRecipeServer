from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import openai
import json

# openai.api_key = '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'
openai.api_key = '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'

app = Flask(__name__)
cors = CORS(app)

EXAMPLE_RESULT_CATEGORY = {
  "categories": [
    {
      "Ingredient": ["Ground Beef", "Italian Sausage", "Chicken", "Shrimp", "Salmon", "Pancetta", "Tomatoes",
                     "Garlic", "Onion", "Bell Peppers", "Mushrooms", "Spinach", "Zucchini", "Cherry Tomatoes",
                     "Parmesan", "Mozzarella", "Ricotta", "Pecorino", "Gorgonzola"],
      "Cuisine": ["Italian", "American", "Asian", "Mediterranean", "Latin American"],
      "PreparationTime": ["10mins", "20mins"],
      "CookingMethod": ["Frying", "Stewing", "Boiling", "Baking"],
      "AllergenInformation": ["Wheat", "Gluten", "Eggs", "Milk", "Soy", "Tree Nuts", "Peanuts", "Shellfish", "Fish"],
      "DietaryConsideration": ["Whole Grain", "Vegetarian", "High-Protein", "Vegan", "Gluten-Free"],
      "Varieties": ["Spaghetti", "Penne", "Fusilli", "Farfalle", "Rigatoni", "Fettuccine", "Linguine", "Orzo",
                    "Ravioli", "Tortellini"]
    }
  ]
}

client = OpenAI(api_key=openai.api_key)

@app.route('/GetRecipeCategories', methods = ['POST'])
def GetRecipeCategories():
    input_value = request.form['input']
    print(input_value)
    # prompt = 'Give me the categories for this recipe (such as ingredient, cuisine, ...): ' + request.values.get('input')
    prompt = 'Give me the categories for this dish：'+ input_value
    # client = OpenAI()
    example_string= json.dumps(EXAMPLE_RESULT_CATEGORY, indent=2)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content":
                "You are a helpful assistant designed to output JSON. The JSON should be 3 layers."
                "Provide me with the categories for recipe generation of pasta"
                "including aspects such as ingredients, cuisine, preparation time, and more. "
                "Specifically, within the category, list the relevant subcategories for recipe generation."
             },
            {"role": "user", "content": "Give me the categories for this dish：pasta"},
            {"role": "assistant", "content": example_string},
            {"role": "user", "content": prompt}
        ]
    )
    print(response.choices[0].message.content)
    result_json = response.choices[0].message.content
    return result_json

@app.route('/GetParticularRecipeCategories', methods = ['POST'])
def GetParticularRecipeCategories():
    user_json_data = request.get_json()
    categories = user_json_data.get("categories", [])
    userInput = user_json_data.get("userInput")
    prompt = f"Give me a Recipe of {userInput}\n"
    for category in categories:
        for key, values in category.items():
            prompt += f"{key} is {', '.join(values)}\n"
    print("prompt: " + prompt)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={"type": "text"},
        messages=[
            {"role": "system", "content":
                "You are a helpful assistant designed to output a customized recipe text."
             },
            {"role": "user", "content": prompt}
        ]
    )
    customized_recipe = response.choices[0].message.content
    print("customized recipe: " + customized_recipe)
    return customized_recipe


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8088)
    # app.run(debug=True)