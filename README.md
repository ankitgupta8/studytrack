# Lecture Progress Tracker

A Streamlit-based lecture progress tracking application with advanced user authentication, personalized progress management, and secure individual user data storage.

## Deployment to Streamlit.io

### Prerequisites
1. Create a Streamlit account at https://streamlit.io
2. Install Git (if not already installed)

### Required Dependencies
- streamlit
- flask
- flask-sqlalchemy
- flask-login
- werkzeug
- pandas
- plotly

### Deployment Steps

1. Create a GitHub repository and push your code:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo-url>
git push -u origin main
```

2. Log in to Streamlit.io and create a new app:
   - Click "New app"
   - Select your GitHub repository
   - Select the main branch
   - Click "Deploy"

3. Configure Secrets:
   - In the Streamlit Cloud dashboard, go to your app settings
   - Find the "Secrets" section
   - Add the following configuration (adjust values as needed):
```toml
[database]
url = "sqlite:///lecture_tracker.db"

[flask]
secret_key = "your-production-secret-key"
```

### Important Notes
- The app uses SQLite by default. For production, consider using a more robust database like PostgreSQL
- Make sure to set a strong secret key in production
- Keep your .streamlit/secrets.toml file in .gitignore to prevent sensitive data exposure

### Local Development
To run the app locally:
```bash
streamlit run main.py
```

### Features
- User authentication and registration
- Subject and chapter management
- Progress tracking with visual analytics
- Interactive dashboard
- Secure data storage
