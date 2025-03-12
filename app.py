from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
import json

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Chave secreta para a sessão

# Arquivos de dados
USERS_FILE = 'users.json'
QUESTIONS_FILE = 'questions.json'

# Função para carregar dados de usuários
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

# Função para salvar dados de usuários
def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

# Função para carregar perguntas
def load_questions():
    try:
        with open(QUESTIONS_FILE, 'r') as f:
            questions = json.load(f)
    except FileNotFoundError:
        questions = []
    
    for question in questions:
        if 'answers' not in question:
            question['answers'] = []
    
    return questions

# Função para salvar perguntas
def save_questions(questions):
    with open(QUESTIONS_FILE, 'w') as f:
        json.dump(questions, f)

# Página de registro (aceita JSON e formulário)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form
        
        username = data.get('username')
        password = data.get('password')
        users = load_users()

        if not username or not password:
            return jsonify({"error": "Usuário e senha são obrigatórios!"}), 400

        if username in users:
            return jsonify({"error": "Usuário já existe!"}), 400

        users[username] = {'password': password}
        save_users(users)

        return jsonify({"message": "Usuário cadastrado com sucesso!"}), 201

    return render_template('register.html')

# Página de login (aceita JSON e formulário)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form
        
        username = data.get('username')
        password = data.get('password')
        users = load_users()

        if not username or not password:
            return jsonify({"error": "Usuário e senha são obrigatórios!"}), 400

        if username in users and users[username]['password'] == password:
            session['username'] = username
            return jsonify({"message": "Login bem-sucedido!"}), 200

        return jsonify({"error": "Usuário ou senha incorretos!"}), 401

    return render_template('login.html')

# Página inicial
@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return render_template('home.html', username="Visitante")

# Página para criar perguntas (Aceita JSON e formulário HTML)
@app.route('/create_question', methods=['GET', 'POST'])
def create_question():
    if 'username' not in session:
        return jsonify({"error": "Não autorizado"}), 403

    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            question_text = data.get('question')
            answers = data.get('answers')
            correct_answer = data.get('correct_answer')
        else:
            question_text = request.form['question']
            answers = [
                request.form['answer1'],
                request.form['answer2'],
                request.form['answer3'],
                request.form['answer4']
            ]
            correct_answer = request.form['answer4']
        
        question_data = {
            'question': question_text,
            'answers': answers,
            'correct_answer': correct_answer,
            'user_responses': []
        }

        questions = load_questions()
        questions.append(question_data)
        save_questions(questions)

        return jsonify({"message": "Pergunta cadastrada com sucesso!"}), 201

    return render_template('create_question.html')

# Página para responder perguntas
@app.route('/answer_question', methods=['GET', 'POST'])
def answer_question():
    if 'username' not in session:
        return redirect(url_for('login'))

    questions = load_questions()

    if request.method == 'POST':
        # Usar request.get_json() para pegar os dados em JSON no corpo da requisição
        data = request.get_json()
        
        question_id = int(data['question_id'])
        user_answer = data['answer']
        correct_answer = questions[question_id]['correct_answer']
        is_correct = user_answer.strip().lower() == correct_answer.strip().lower()

        if 'answers' not in questions[question_id]:
            questions[question_id]['answers'] = []

        questions[question_id]['answers'].append({
            'user': session['username'],
            'answer': user_answer,
            'is_correct': is_correct
        })

        save_questions(questions)
        return redirect(url_for('responses'))

    return render_template('answer_question.html', questions=questions)


# Página de respostas
@app.route('/responses')
def responses():
    questions = load_questions()  
    return render_template('responses.html', questions=questions)

# Página de logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/flutter')
def flutter():
    return render_template('flutter.html')

if __name__ == "__main__":
    app.run(debug=True)