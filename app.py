from flask import Flask, render_template, request, redirect, url_for, session
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
    # Carrega as perguntas de um arquivo ou banco de dados
    try:
        with open(QUESTIONS_FILE, 'r') as f:
            questions = json.load(f)
    except FileNotFoundError:
        questions = []
    
    # Garantir que a chave 'answers' exista para cada pergunta
    for question in questions:
        if 'answers' not in question:
            question['answers'] = []
    
    return questions

# Função para salvar perguntas
def save_questions(questions):
    with open(QUESTIONS_FILE, 'w') as f:
        json.dump(questions, f)

# Página de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()

        # Verifica se o usuário já existe
        if username in users:
            return "Usuário já existe!"

        # Adiciona novo usuário
        users[username] = {'password': password}
        save_users(users)

        return redirect(url_for('login'))
    return render_template('register.html')

# Página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()

        # Verifica se o usuário existe e se a senha está correta
        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('home'))

        return "Usuário ou senha incorretos!"
    return render_template('login.html')

# Página inicial (primeira tela carregada)
@app.route('/')
def home():
    # Se o usuário estiver logado, mostra o conteúdo da home
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    
    # Se não estiver logado, mostra a home sem exigir login
    return render_template('home.html', username="Visitante")

@app.route('/create_question', methods=['GET', 'POST'])
def create_question():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        question_text = request.form['question']
        answers = [
            request.form['answer1'],
            request.form['answer2'],
            request.form['answer3'],
            request.form['answer4']  # A resposta correta
        ]


        # Descobrir o novo índice da resposta correta após o embaralhamento
        correct_answer_index = answers.index(request.form['answer4'])  # Resposta correta original

        question_data = {
            'question': question_text,
            'answers': answers,
            'correct_answer': request.form['answer4'],  # Agora salva a resposta correta
            'correct_answer_index': correct_answer_index,
            'user_responses': []  # Lista para armazenar respostas dos usuários
        }

        questions = load_questions()
        questions.append(question_data)
        save_questions(questions)

        return redirect(url_for('home'))

    return render_template('create_question.html')

# Página para responder perguntas
@app.route('/answer_question', methods=['GET', 'POST'])
def answer_question():
    if 'username' not in session:
        return redirect(url_for('login'))

    questions = load_questions()

    if request.method == 'POST':
        question_id = int(request.form['question_id'])
        user_answer = request.form['answer']

        # Obtém a resposta correta da pergunta
        correct_answer = questions[question_id]['correct_answer']

        # Normaliza as respostas para evitar erros de comparação
        is_correct = user_answer.strip().lower() == correct_answer.strip().lower()

        # Certificar que a chave 'answers' existe antes de adicionar uma resposta
        if 'answers' not in questions[question_id]:
            questions[question_id]['answers'] = []

        questions[question_id]['answers'].append({
            'user': session['username'],
            'answer': user_answer,
            'is_correct': is_correct  # Armazena se a resposta foi correta
        })

        save_questions(questions)

        return redirect(url_for('responses'))  # Redireciona para ver as respostas

    return render_template('answer_question.html', questions=questions)

# Página de respostas
@app.route('/responses')
def responses():
    # Carrega as perguntas e suas respectivas respostas
    questions = load_questions()  
    return render_template('responses.html', questions=questions)

# Página de logout
@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove o usuário da sessão
    return redirect(url_for('home'))  # Redireciona de volta para a página inicial

@app.route('/flutter')
def flutter():
    return render_template('flutter.html')

if __name__ == "__main__":
    app.run(debug=True)
