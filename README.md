#  AI Movie Recommendation Website

A Flask-based web application that allows users to receive intelligent movie recommendations through an AI-powered chatbox. The project includes an admin dashboard for managing movie data and integrates OpenAI's GPT API for natural, conversational responses.

---

##  Features

###  Public Pages
- **Homepage:**  
  Displays a dynamic grid of movies with title, genre, rating, year, and poster.
- **About Page:**  
  Brief description of the project or purpose.
- **Chatbox Page:**  
  Allows users to enter movie preferences (e.g., genre, year, rating) and receive AI-generated recommendations based on the stored database.

### AI Chat Integration
- Integrated **OpenAI ChatGPT API** (GPT-3.5) to generate responses from filtered movie results.
- Supports natural language queries such as:
  > "Show me romantic movies from 2023 with rating over 7"

### Admin Panel
- **Admin Login:**  
  Protected route (`/admin`) with session-based login (`/login`)
- **Movie Entry Form:**  
  Add new movies with the following fields:
  - Title  
  - Genre (e.g., Action, Comedy, Drama...)  
  - Year  
  - IMDb Rating  
  - Poster URL
- **Logout:**  
  Logs out and redirects back to the homepage.

---

##  Tech Stack

| Layer      | Tools / Technologies                      |
|------------|-------------------------------------------|
| Backend    | Python, Flask                             |
| Database   | SQLite                                    |
| AI API     | OpenAI GPT-3.5 (ChatCompletion API)       |
| Frontend   | HTML, CSS (custom velvet-styled theme)    |
| Editor     | VS Code on macOS                          |

---

##  Sample Features

-  Posters loaded dynamically using direct URLs
-  Real-time recommendations based on genre/year/rating
-  Simple admin panel to insert/update movie content
-  Session-based admin authentication

---

##  How to Run

1. Clone this repository  
2. Install Flask:##  Project Structure
3. Set your OpenAI key inside `app.py`:
```python
openai.api_key = "your-api-key"
python app.py
