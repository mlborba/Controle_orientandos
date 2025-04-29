from app import app, db, Usuario

with app.app_context():
    # Verificar se o usuário admin já existe
    admin = Usuario.query.filter_by(username='admin').first()
    
    # Se não existir, criar o usuário admin
    if not admin:
        admin = Usuario(
            username='admin',
            nome='Administrador',
            email='admin@example.com'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print('Usuário administrador criado com sucesso')
    else:
        print('Usuário administrador já existe')
