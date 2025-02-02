from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from decouple import config
import requests
import json
import urllib.parse

app = Flask(__name__, static_folder='static')
CORS(app)

API_KEY = config('OPENAI_API_KEY')
API_URL = "https://api.groq.com/openai/v1/chat/completions"
YOUTUBE_API_KEY = config('YOUTUBE_API_KEY', default='')  # You'll need to add this to your .env file

def generate_recipe(ingredients):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""Create a recipe using these ingredients: {ingredients}
    Respond ONLY with a JSON object in this exact format:
    {{
        "name": "Recipe Name",
        "cookingTime": "XX minutes",
        "instructions": ["step 1", "step 2", "step 3"],
        "ingredients": ["ingredient 1", "ingredient 2"],
        "nutritionalInfo": "Basic nutritional information"
    }}"""
    
    payload = {
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 800,
        "model": "mixtral-8x7b-32768"
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        recipe_text = result['choices'][0]['message']['content'].strip()
        
        # Ensure we got valid JSON
        recipe_json = json.loads(recipe_text)
        return recipe_json
        
    except requests.exceptions.RequestException as e:
        print(f"API Error: {str(e)}")
        if hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        raise Exception("Failed to generate recipe")
    except json.JSONDecodeError as e:
        print(f"JSON Parse Error: {str(e)}")
        raise Exception("Invalid recipe format received")
    except Exception as e:
        print(f"Unexpected Error: {str(e)}")
        raise

def search_youtube_videos(recipe_name):
    if not YOUTUBE_API_KEY:
        # Return mock data if no API key is provided
        return [
            {
                "videoId": "dQw4w9WgXcQ",
                "title": f"How to Make {recipe_name}",
                "channelTitle": "Cooking Channel"
            },
            {
                "videoId": "dQw4w9WgXcQ",
                "title": f"Easy {recipe_name} Recipe",
                "channelTitle": "Chef's Kitchen"
            }
        ]
    
    try:
        query = urllib.parse.quote(f"{recipe_name} recipe")
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&maxResults=4&key={YOUTUBE_API_KEY}"
        
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        videos = []
        
        for item in data.get('items', []):
            videos.append({
                "videoId": item['id']['videoId'],
                "title": item['snippet']['title'],
                "channelTitle": item['snippet']['channelTitle']
            })
        
        return videos
        
    except Exception as e:
        print(f"Error fetching videos: {str(e)}")
        return []

@app.route('/api/generate', methods=['POST'])
def create_recipe():
    try:
        data = request.get_json()
        ingredients = data.get('ingredients', '')
        
        if not ingredients:
            return jsonify({'error': 'No ingredients provided'}), 400
            
        recipe = generate_recipe(ingredients)
        return jsonify(recipe)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/videos')
def get_videos():
    recipe = request.args.get('recipe', '')
    if not recipe:
        return jsonify({'error': 'No recipe name provided'}), 400
    
    videos = search_youtube_videos(recipe)
    return jsonify(videos)

@app.route('/')
def serve_app():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    app.run(debug=True)
