from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import openai

openai.api_key = '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'

app = Flask(__name__)
cors = CORS(app)

@app.route('/GetRecipeCategories', methods = ['POST'])
def GetRecipeCategories():
    input_value = request.form['input']
    print(input_value)
    # prompt = 'Give me the categories for this recipe (such as ingredient, cuisine, ...): ' + request.values.get('input')
    prompt = 'Give me the categories for recipe (such as ingredient, cuisine, preparation time ...)：'+ input_value
    # client = OpenAI()
    client = OpenAI(api_key=openai.api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": prompt}
        ]
    )
    print(response.choices[0].message.content)
    result_json = response.choices[0].message.content
    return result_json

@app.route('/GetParticularRecipeCategories', methods = ['GET'])
def GetParticularRecipeCategories():
    #test_1
    return 0


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8088)
    # app.run(debug=True)