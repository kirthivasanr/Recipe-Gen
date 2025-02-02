# AI Recipe Generator

A web application that generates recipes based on available ingredients using AI.

## Features

- Input available ingredients
- Generate complete recipes with cooking instructions
- Get nutritional information
- Receive suggestions for optional ingredients
- Responsive design for mobile and desktop

## Setup Instructions

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Open your browser and navigate to `http://localhost:5000`

## Technologies Used

- Backend: Python Flask
- Frontend: HTML, JavaScript, Tailwind CSS
- AI: OpenAI GPT-3.5 Turbo
- Additional: Flask-CORS, python-decouple

## Note

Make sure to keep your OpenAI API key secure and never commit it to version control.
