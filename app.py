from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
from dateutil.relativedelta import relativedelta

# Configuração do aplicativo
app = Flask(__name__)
app.instance_path = '/tmp/instance_orientacao'  # Corrige o erro de sistema de arquivos somente leitura no Vercel

# Usar uma SECRET_KEY fixa para manter as sessões entre reinicializações
app.config['SECRET_KEY'] = 'chave_secreta_fixa_para_sistema_orientacao_2025'  # IMPORTANTE: Usar uma chave fixa
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)  # Sessão dura 1 dia

# Configuração do banco de dados
# Verificar se existe variável de ambiente DATABASE_URL (para o Vercel)
if os.environ.get('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    print("Usando banco de dados configurado via DATABASE_URL")
    print(f"URL do banco de dados configurada: {os.environ.get('DATABASE_URL')}")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orientacao.db'
    print("Usando banco de dados SQLite local")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialização do banco de dados
db = SQLAlchemy(app)

# Configuração do login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Modelos de dados
class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Orientando(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telefone = db.Column(db.String(20))
    data_ingresso = db.Column(db.Date, nullable=False)
    titulo_projeto = db.Column(db.String(200), nullable=False)
    area_pesquisa = db.Column(db.String(100))
    status = db.Column(db.String(20), default='ativo')  # ativo/inativo
    tipo = db.Column(db.String(20), nullable=False)  # orientando/coorientando
    orientador_principal_id = db.Column(db.Integer, db.ForeignKey('orientando.id'), nullable=True)
    
    # Relacionamentos
    marcos = db.relationship('Marco', backref='orientando', lazy=True)
    orientacoes = db.relationship('Orientacao', backref='orientando', lazy=True)
    
    def __repr__(self):
        return f'<Orientando {self.nome}>'

class Marco(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    orientando_id = db.Column(db.Integer, db.ForeignKey('orientando.id'), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # seminário semestral, qualificação, defesa
    data_prevista = db.Column(db.Date, nullable=False)
    data_realizada = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(20), default='pendente')  # pendente, concluído, atrasado
    observacoes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Marco {self.tipo} - {self.orientando_id}>'

class Orientacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    orientando_id = db.Column(db.Integer, db.ForeignKey('orientando.id'), nullable=False)
    data_hora = db.Column(db.DateTime, nullable=False)
    duracao_prevista = db.Column(db.Integer, default=60)  # em minutos
    status = db.Column(db.String(20), default='agendada')  # agendada, realizada, cancelada
    modalidade = db.Column(db.String(20), default='presencial')  # presencial, online
    local = db.Column(db.String(100))
    
    # Relacionamento com o diário
    diario = db.relationship('DiarioOrientacao', backref='orientacao', lazy=True, uselist=False)
    
    def __repr__(self):
        return f'<Orientacao {self.orientando_id} - {self.data_hora}>'

class DiarioOrientacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    orientacao_id = db.Column(db.Integer, db.ForeignKey('orientacao.id'), nullable=False, unique=True)
    topicos_discutidos = db.Column(db.Text)
    progresso_observado = db.Column(db.Text)
    pendencias = db.Column(db.Text)
    tarefas_atribuidas = db.Column(db.Text)
    prazo_proximas_entregas = db.Column(db.Date)
    avaliacao_progresso = db.Column(db.String(20))  # excelente, bom, regular, insuficiente
    
    def __repr__(self):
        return f'<DiarioOrientacao {self.orientacao_id}>'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Rotas
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = Usuario.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=True)  # Usar remember=True para manter a sessão
            session.permanent = True  # Tornar a sessão permanente
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        
        flash('Usuário ou senha inválidos')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Contagem de orientandos por tipo
    orientandos = Orientando.query.filter_by(tipo='orientando', status='ativo').count()
    coorientandos = Orientando.query.filter_by(tipo='coorientando', status='ativo').count()
    
    # Próximas orientações
    hoje = datetime.now()
    proximas_orientacoes = Orientacao.query.filter(
        Orientacao.data_hora >= hoje,
        Orientacao.status == 'agendada'
    ).order_by(Orientacao.data_hora).limit(5).all()
    
    # Próximos marcos
    proximos_marcos = Marco.query.filter(
        Marco.data_prevista >= hoje.date(),
        Marco.status == 'pendente'
    ).order_by(Marco.data_prevista).limit(5).all()
    
    # Marcos atrasados
    marcos_atrasados = Marco.query.filter(
        Marco.data_prevista < hoje.date(),
        Marco.status == 'pendente'
    ).order_by(Marco.data_prevista).all()
    
    return render_template(
        'dashboard.html',
        orientandos=orientandos,
        coorientandos=coorientandos,
        proximas_orientacoes=proximas_orientacoes,
        proximos_marcos=proximos_marcos,
        marcos_atrasados=marcos_atrasados,
        now=datetime.now()
    )

# Rotas para Orientandos
@app.route('/orientandos')
@login_required
def listar_orientandos():
    orientandos = Orientando.query.all()
    return render_template('orientandos/listar.html', orientandos=orientandos)

@app.route('/orientandos/novo', methods=['GET', 'POST'])
@login_required
def novo_orientando():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        data_ingresso = datetime.strptime(request.form.get('data_ingresso'), '%Y-%m-%d').date()
        titulo_projeto = request.form.get('titulo_projeto')
        area_pesquisa = request.form.get('area_pesquisa')
        tipo = request.form.get('tipo')
        orientador_principal_id = request.form.get('orientador_principal_id')
        
        if orientador_principal_id == '':
            orientador_principal_id = None
        
        orientando = Orientando(
            nome=nome,
            email=email,
            telefone=telefone,
            data_ingresso=data_ingresso,
            titulo_projeto=titulo_projeto,
            area_pesquisa=area_pesquisa,
            tipo=tipo,
            orientador_principal_id=orientador_principal_id
        )
        
        db.session.add(orientando)
        db.session.commit()
        
        # Criar marcos automáticos baseados na data de ingresso
        if tipo == 'orientando':
            # Seminário do primeiro semestre (6 meses após ingresso)
            data_seminario1 = data_ingresso + relativedelta(months=6)
            marco_seminario1 = Marco(
                orientando_id=orientando.id,
                tipo='Seminário do 1º Semestre',
                data_prevista=data_seminario1,
                observacoes='Gerado automaticamente'
            )
            db.session.add(marco_seminario1)
            
            # Seminário do segundo semestre (12 meses após ingresso)
            data_seminario2 = data_ingresso + relativedelta(months=12)
            marco_seminario2 = Marco(
                orientando_id=orientando.id,
                tipo='Seminário do 2º Semestre',
                data_prevista=data_seminario2,
                observacoes='Gerado automaticamente'
            )
            db.session.add(marco_seminario2)
            
            # Qualificação (18 meses após ingresso)
            data_qualificacao = data_ingresso + relativedelta(months=18)
            marco_qualificacao = Marco(
                orientando_id=orientando.id,
                tipo='Qualificação',
                data_prevista=data_qualificacao,
                observacoes='Gerado automaticamente'
            )
            db.session.add(marco_qualificacao)
            
            # Defesa (24 meses após ingresso)
            data_defesa = data_ingresso + relativedelta(months=24)
            marco_defesa = Marco(
                orientando_id=orientando.id,
                tipo='Defesa',
                data_prevista=data_defesa,
                observacoes='Gerado automaticamente'
            )
            db.session.add(marco_defesa)
            
            db.session.commit()
        
        flash('Orientando cadastrado com sucesso!')
        return redirect(url_for('listar_orientandos'))
    
    # Para o formulário de coorientandos, precisamos listar os orientandos disponíveis
    orientandos_disponiveis = Orientando.query.filter_by(tipo='orientando').all()
    return render_template('orientandos/novo.html', orientandos_disponiveis=orientandos_disponiveis)

@app.route('/orientandos/<int:id>')
@login_required
def visualizar_orientando(id):
    orientando = Orientando.query.get_or_404(id)
    marcos = Marco.query.filter_by(orientando_id=id).order_by(Marco.data_prevista).all()
    orientacoes = Orientacao.query.filter_by(orientando_id=id).order_by(Orientacao.data_hora.desc()).all()
    
    return render_template(
        'orientandos/visualizar.html',
        orientando=orientando,
        marcos=marcos,
        orientacoes=orientacoes
    )

@app.route('/orientandos/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_orientando(id):
    orientando = Orientando.query.get_or_404(id)
    
    if request.method == 'POST':
        orientando.nome = request.form.get('nome')
        orientando.email = request.form.get('email')
        orientando.telefone = request.form.get('telefone')
        orientando.data_ingresso = datetime.strptime(request.form.get('data_ingresso'), '%Y-%m-%d').date()
        orientando.titulo_projeto = request.form.get('titulo_projeto')
        orientando.area_pesquisa = request.form.get('area_pesquisa')
        orientando.status = request.form.get('status')
        orientando.tipo = request.form.get('tipo')
        
        orientador_principal_id = request.form.get('orientador_principal_id')
        if orientador_principal_id == '':
            orientando.orientador_principal_id = None
        else:
            orientando.orientador_principal_id = orientador_principal_id
        
        db.session.commit()
        flash('Orientando atualizado com sucesso!')
        return redirect(url_for('visualizar_orientando', id=id))
    
    orientandos_disponiveis = Orientando.query.filter_by(tipo='orientando').all()
    return render_template('orientandos/editar.html', orientando=orientando, orientandos_disponiveis=orientandos_disponiveis)

# Rota para excluir orientando
@app.route('/orientandos/<int:id>/excluir', methods=['POST'])
@login_required
def excluir_orientando(id):
    orientando = Orientando.query.get_or_404(id)
    
    # Verificar se o orientando é orientador principal de algum coorientando
    coorientandos_associados = Orientando.query.filter_by(orientador_principal_id=id).count()
    if coorientandos_associados > 0:
        flash('Não é possível excluir este orientando, pois ele é orientador principal de um ou mais coorientandos. Remova a associação primeiro.', 'danger')
        return redirect(url_for('listar_orientandos'))
        
    try:
        # Excluir marcos associados
        Marco.query.filter_by(orientando_id=id).delete()
        # Excluir diários de orientação associados (indireto, via orientação)
        orientacoes = Orientacao.query.filter_by(orientando_id=id).all()
        for orientacao in orientacoes:
            DiarioOrientacao.query.filter_by(orientacao_id=orientacao.id).delete()
        # Excluir orientações associadas
        Orientacao.query.filter_by(orientando_id=id).delete()
        
        db.session.delete(orientando)
        db.session.commit()
        flash('Orientando e todos os seus dados relacionados foram excluídos com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir o orientando: {str(e)}', 'danger')
    return redirect(url_for('listar_orientandos'))

# Rotas para Marcos
@app.route('/marcos')
@login_required
def listar_marcos():
    marcos = Marco.query.order_by(Marco.data_prevista).all()
    return render_template('marcos/listar.html', marcos=marcos)

@app.route('/marcos/novo', methods=['GET', 'POST'])
@login_required
def novo_marco():
    if request.method == 'POST':
        orientando_id = request.form.get('orientando_id')
        tipo = request.form.get('tipo')
        data_prevista = datetime.strptime(request.form.get('data_prevista'), '%Y-%m-%d').date()
        observacoes = request.form.get('observacoes')
        
        marco = Marco(
            orientando_id=orientando_id,
            tipo=tipo,
            data_prevista=data_prevista,
            observacoes=observacoes
        )
        
        db.session.add(marco)
        db.session.commit()
        
        flash('Marco cadastrado com sucesso!')
        return redirect(url_for('listar_marcos'))
    
    orientandos = Orientando.query.all()
    return render_template('marcos/novo.html', orientandos=orientandos)

@app.route('/marcos/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_marco(id):
    marco = Marco.query.get_or_404(id)
    
    if request.method == 'POST':
        marco.orientando_id = request.form.get('orientando_id')
        marco.tipo = request.form.get('tipo')
        marco.data_prevista = datetime.strptime(request.form.get('data_prevista'), '%Y-%m-%d').date()
        
        data_realizada = request.form.get('data_realizada')
        if data_realizada:
            marco.data_realizada = datetime.strptime(data_realizada, '%Y-%m-%d').date()
            marco.status = 'concluído'
        else:
            marco.data_realizada = None
            # Atualizar status baseado na data prevista
            if marco.data_prevista < datetime.now().date() and marco.status == 'pendente':
                marco.status = 'atrasado'
            else:
                marco.status = request.form.get('status')
        
        marco.observacoes = request.form.get('observacoes')
        
        db.session.commit()
        flash('Marco atualizado com sucesso!')
        return redirect(url_for('listar_marcos'))
    
    orientandos = Orientando.query.all()
    return render_template('marcos/editar.html', marco=marco, orientandos=orientandos)

# Rota para excluir marco
@app.route('/marcos/<int:id>/excluir', methods=['POST'])
@login_required
def excluir_marco(id):
    marco = Marco.query.get_or_404(id)
    try:
        db.session.delete(marco)
        db.session.commit()
        flash('Marco excluído com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir o marco: {str(e)}', 'danger')
    return redirect(url_for('listar_marcos'))

# Rotas para Orientações
@app.route('/orientacoes')
@login_required
def listar_orientacoes():
    orientacoes = Orientacao.query.order_by(Orientacao.data_hora.desc()).all()
    return render_template('orientacoes/listar.html', orientacoes=orientacoes)

@app.route('/orientacoes/nova', methods=['GET', 'POST'])
@login_required
def nova_orientacao():
    if request.method == 'POST':
        orientando_id = request.form.get('orientando_id')
        data = request.form.get('data')
        hora = request.form.get('hora')
        data_hora = datetime.strptime(f'{data} {hora}', '%Y-%m-%d %H:%M')
        duracao_prevista = request.form.get('duracao_prevista')
        modalidade = request.form.get('modalidade')
        local = request.form.get('local')
        
        orientacao = Orientacao(
            orientando_id=orientando_id,
            data_hora=data_hora,
            duracao_prevista=duracao_prevista,
            modalidade=modalidade,
            local=local
        )
        
        db.session.add(orientacao)
        db.session.commit()
        
        flash('Orientação agendada com sucesso!')
        return redirect(url_for('listar_orientacoes'))
    
    orientandos = Orientando.query.filter_by(status='ativo').all()
    return render_template('orientacoes/nova.html', orientandos=orientandos)

# VERSÃO CORRIGIDA - Visualizar orientação com tratamento de erro
@app.route('/orientacoes/<int:id>')
@login_required
def visualizar_orientacao(id):
    try:
        orientacao = Orientacao.query.get_or_404(id)
        return render_template('orientacoes/visualizar.html', orientacao=orientacao)
    except Exception as e:
        import traceback
        app.logger.error(f"Erro ao visualizar orientação {id}: {str(e)}")
        app.logger.error(traceback.format_exc())
        flash(f"Erro ao visualizar orientação: {str(e)}", "danger")
        return redirect(url_for('listar_orientacoes'))

@app.route('/orientacoes/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_orientacao(id):
    orientacao = Orientacao.query.get_or_404(id)
    
    if request.method == 'POST':
        orientacao.orientando_id = request.form.get('orientando_id')
        data = request.form.get('data')
        hora = request.form.get('hora')
        orientacao.data_hora = datetime.strptime(f'{data} {hora}', '%Y-%m-%d %H:%M')
        orientacao.duracao_prevista = request.form.get('duracao_prevista')
        orientacao.status = request.form.get('status')
        orientacao.modalidade = request.form.get('modalidade')
        orientacao.local = request.form.get('local')
        
        db.session.commit()
        flash('Orientação atualizada com sucesso!')
        return redirect(url_for('visualizar_orientacao', id=id))
    
    orientandos = Orientando.query.filter_by(status='ativo').all()
    return render_template('orientacoes/editar.html', orientacao=orientacao, orientandos=orientandos)

# VERSÃO CORRIGIDA - Registrar diário com tratamento de erro
@app.route('/orientacoes/<int:id>/registrar', methods=['GET', 'POST'])
@login_required
def registrar_diario(id):
    orientacao = Orientacao.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            # Verificar se já existe um diário para esta orientação
            diario_existente = DiarioOrientacao.query.filter_by(orientacao_id=id).first()
            
            if diario_existente:
                # Atualizar diário existente
                diario_existente.topicos_discutidos = request.form.get('topicos_discutidos', '')
                diario_existente.progresso_observado = request.form.get('progresso_observado', '')
                diario_existente.pendencias = request.form.get('pendencias', '')
                diario_existente.tarefas_atribuidas = request.form.get('tarefas_atribuidas', '')
                
                # Tratar o campo de data corretamente
                prazo_str = request.form.get('prazo_proximas_entregas')
                if prazo_str and prazo_str.strip():
                    diario_existente.prazo_proximas_entregas = datetime.strptime(prazo_str, '%Y-%m-%d').date()
                else:
                    diario_existente.prazo_proximas_entregas = None
                    
                diario_existente.avaliacao_progresso = request.form.get('avaliacao_progresso', '')
            else:
                # Criar novo diário
                prazo_str = request.form.get('prazo_proximas_entregas')
                prazo_date = None
                if prazo_str and prazo_str.strip():
                    prazo_date = datetime.strptime(prazo_str, '%Y-%m-%d').date()
                
                diario = DiarioOrientacao(
                    orientacao_id=id,
                    topicos_discutidos=request.form.get('topicos_discutidos', ''),
                    progresso_observado=request.form.get('progresso_observado', ''),
                    pendencias=request.form.get('pendencias', ''),
                    tarefas_atribuidas=request.form.get('tarefas_atribuidas', ''),
                    prazo_proximas_entregas=prazo_date,
                    avaliacao_progresso=request.form.get('avaliacao_progresso', '')
                )
                db.session.add(diario)
            
            # Atualizar status da orientação
            orientacao.status = 'realizada'
            
            db.session.commit()
            flash('Diário registrado com sucesso!', 'success')
            return redirect(url_for('visualizar_orientacao', id=id))
            
        except Exception as e:
            db.session.rollback()
            import traceback
            app.logger.error(f"Erro ao registrar diário: {str(e)}")
            app.logger.error(traceback.format_exc())
            flash(f"Erro ao registrar diário: {str(e)}", "danger")
            return render_template('orientacoes/registrar_diario.html', orientacao=orientacao)
    
    # GET: exibir formulário
    diario = DiarioOrientacao.query.filter_by(orientacao_id=id).first()
    return render_template('orientacoes/registrar_diario.html', orientacao=orientacao, diario=diario)

# Rota para verificar status da sessão
@app.route('/check-session')
@login_required
def check_session():
    return f"Usuário autenticado: {current_user.username}, ID: {current_user.id}"

# Inicialização do banco de dados
@app.cli.command('init-db')
def init_db_command():
    """Inicializa o banco de dados."""
    db.create_all()
    
    # Criar usuário administrador se não existir
    admin = Usuario.query.filter_by(username='admin').first()
    if not admin:
        admin = Usuario(
            username='admin',
            nome='Administrador',
            email='admin@example.com'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
    
    print('Banco de dados inicializado.')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Criar usuário administrador se não existir
        admin = Usuario.query.filter_by(username='admin').first()
        if not admin:
            admin = Usuario(
                username='admin',
                nome='Administrador',
                email='admin@example.com'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print('Usuário administrador criado.')
    
    app.run(host='0.0.0.0', port=5000, debug=True)
