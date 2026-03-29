import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

# Import Custom Modules
from models import db, User, ResumeHistory
from resume_parser import ResumeParser
from ai_suggestions import get_ai_analysis, get_career_roadmap, get_linkedin_audit
from skill_extractor import extract_skills
from ats_scoring import calculate_ats_score
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'zenith_ultimate_industrial_secret_99'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = 'uploads'

# Initialize Database and Login Management
db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- PAGE NAVIGATION ROUTES ---

@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/about')
def about(): 
    return render_template('about.html')

@app.route('/services')
def services(): 
    return render_template('services.html')

@app.route('/resources')
def resources(): 
    return render_template('resources.html')

@app.route('/roadmap')
def roadmap_page(): 
    return render_template('roadmap.html')

@app.route('/linkedin')
def linkedin_page(): 
    return render_template('linkedin.html')

@app.route('/build_resume')
def build_resume_page(): 
    return render_template('build_resume.html')

# --- AUTHENTICATION SYSTEM ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            return redirect(url_for('index'))
        flash('ACCESS DENIED: INVALID CREDENTIALS')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(email=email).first():
            flash('IDENTITY ALREADY ARCHIVED')
            return redirect(url_for('signup'))
            
        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(email=email, password=hashed_pw)
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        except Exception as e:
            flash('REGISTRATION ERROR')
    return render_template('signup.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        seed = request.form.get('avatar_seed', 'Felix')
        current_user.avatar_url = f'https://api.dicebear.com/7.x/avataaars/svg?seed={seed}'
        db.session.commit()
        return redirect(url_for('profile'))
    return render_template('profile.html')

# --- CORE AI INTELLIGENCE ENDPOINTS ---

# 1. Main ATS & Resume Analysis Engine
@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files.get('resume')
    if not file: return jsonify({"error": "No file uploaded"}), 400
    
    jd_text = request.form.get('jd', '').strip()
    user_role = request.form.get('role', 'jobseeker')
    
    filename = secure_filename(file.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(path)

    try:
        # Step 1: Text Extraction
        p = ResumeParser()
        text = p.extract_text(path)
        if not text: raise ValueError("Could not extract readable text from PDF/DOCX")
        
        # Step 2: Data Component Analysis
        profile_data = p.extract_profile(text)
        skills_found = extract_skills(text)
        sections_found = p.check_sections(text)
        
        # Step 3: Scoring & AI Synthesis
        score, rating = calculate_ats_score(text, jd_text, sections_found, skills_found)
        ai_data = get_ai_analysis(text, jd_text, user_role)

        # Step 4: Save History for Logged-in Users
        if current_user.is_authenticated:
            history_entry = ResumeHistory(
                candidate_name=profile_data['name'], 
                score=int(score), 
                user_id=current_user.id
            )
            db.session.add(history_entry)
            db.session.commit()

        os.remove(path) # Cleanup
        return jsonify({
            "score": int(score),
            "rating": rating,
            "profile": profile_data,
            "ai": ai_data
        })
    except Exception as e:
        if os.path.exists(path): os.remove(path)
        return jsonify({"error": str(e)}), 500

# 2. Dedicated Career Roadmap Engine
@app.route('/analyze_roadmap', methods=['POST'])
def analyze_roadmap():
    file = request.files.get('resume')
    if not file: return jsonify({"error": "Resume required for roadmap"}), 400
    
    filename = secure_filename(file.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(path)
    
    try:
        p = ResumeParser()
        text = p.extract_text(path)
        # Call specialized Roadmap AI logic
        ai_data = get_career_roadmap(text)
        
        os.remove(path)
        return jsonify({"ai": ai_data})
    except Exception as e:
        if os.path.exists(path): os.remove(path)
        return jsonify({"error": str(e)}), 500

# 3. Dedicated LinkedIn Audit Engine
@app.route('/analyze_linkedin', methods=['POST'])
def analyze_linkedin():
    link = request.form.get('link', '').strip()
    if not link: return jsonify({"error": "LinkedIn URL required"}), 400
    
    try:
        # Call specialized LinkedIn AI logic (URL only)
        ai_data = get_linkedin_audit(link)
        return jsonify({"ai": ai_data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 4. Interactive AI Chatbot Endpoint
@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_msg = request.json.get('message')
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant", 
            messages=[{"role": "user", "content": f"Answer as a pro career coach: {user_msg}"}]
        )
        return jsonify({"reply": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"reply": "System busy. Please try later."})

# --- APPLICATION INITIALIZATION ---

if __name__ == '__main__':
    with app.app_context():
        # Auto-create the database file and tables
        db.create_all()
    
    # Ensure the uploads folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
        
    app.run(debug=True)