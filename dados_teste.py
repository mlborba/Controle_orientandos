from app import app, db, Orientando, Marco, Orientacao, DiarioOrientacao
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

with app.app_context():
    # Limpar dados existentes (exceto usuário admin)
    DiarioOrientacao.query.delete()
    Orientacao.query.delete()
    Marco.query.delete()
    Orientando.query.delete()
    db.session.commit()
    
    # Criar orientandos
    orientandos = [
        Orientando(
            nome="Maria Silva",
            email="maria.silva@email.com",
            telefone="(11) 98765-4321",
            data_ingresso=datetime(2023, 3, 1).date(),
            titulo_projeto="Análise de algoritmos de aprendizado de máquina para detecção de fraudes",
            area_pesquisa="Inteligência Artificial",
            tipo="orientando"
        ),
        Orientando(
            nome="João Santos",
            email="joao.santos@email.com",
            telefone="(11) 91234-5678",
            data_ingresso=datetime(2023, 3, 15).date(),
            titulo_projeto="Desenvolvimento de frameworks para aplicações web escaláveis",
            area_pesquisa="Engenharia de Software",
            tipo="orientando"
        ),
        Orientando(
            nome="Ana Oliveira",
            email="ana.oliveira@email.com",
            telefone="(11) 99876-5432",
            data_ingresso=datetime(2023, 2, 1).date(),
            titulo_projeto="Segurança em sistemas distribuídos baseados em blockchain",
            area_pesquisa="Segurança da Informação",
            tipo="orientando"
        ),
        Orientando(
            nome="Pedro Souza",
            email="pedro.souza@email.com",
            telefone="(11) 98765-1234",
            data_ingresso=datetime(2023, 4, 1).date(),
            titulo_projeto="Otimização de consultas em bancos de dados NoSQL",
            area_pesquisa="Banco de Dados",
            tipo="orientando"
        ),
        Orientando(
            nome="Carla Ferreira",
            email="carla.ferreira@email.com",
            telefone="(11) 97654-3210",
            data_ingresso=datetime(2023, 5, 1).date(),
            titulo_projeto="Aplicação de processamento de linguagem natural em análise de sentimentos",
            area_pesquisa="Processamento de Linguagem Natural",
            tipo="orientando"
        ),
        Orientando(
            nome="Lucas Martins",
            email="lucas.martins@email.com",
            telefone="(11) 96543-2109",
            data_ingresso=datetime(2023, 6, 1).date(),
            titulo_projeto="Desenvolvimento de interfaces adaptativas para aplicações móveis",
            area_pesquisa="Interação Humano-Computador",
            tipo="orientando"
        )
    ]
    
    # Adicionar orientandos ao banco de dados
    for orientando in orientandos:
        db.session.add(orientando)
    
    db.session.commit()
    
    # Criar coorientandos
    coorientandos = [
        Orientando(
            nome="Fernanda Lima",
            email="fernanda.lima@email.com",
            telefone="(11) 95432-1098",
            data_ingresso=datetime(2023, 3, 10).date(),
            titulo_projeto="Aplicação de redes neurais em reconhecimento de imagens médicas",
            area_pesquisa="Inteligência Artificial",
            tipo="coorientando",
            orientador_principal_id=1  # Maria Silva
        ),
        Orientando(
            nome="Roberto Alves",
            email="roberto.alves@email.com",
            telefone="(11) 94321-0987",
            data_ingresso=datetime(2023, 4, 15).date(),
            titulo_projeto="Desenvolvimento de microserviços para sistemas distribuídos",
            area_pesquisa="Engenharia de Software",
            tipo="coorientando",
            orientador_principal_id=2  # João Santos
        ),
        Orientando(
            nome="Juliana Costa",
            email="juliana.costa@email.com",
            telefone="(11) 93210-9876",
            data_ingresso=datetime(2023, 5, 20).date(),
            titulo_projeto="Análise de vulnerabilidades em sistemas IoT",
            area_pesquisa="Segurança da Informação",
            tipo="coorientando",
            orientador_principal_id=3  # Ana Oliveira
        ),
        Orientando(
            nome="Marcelo Vieira",
            email="marcelo.vieira@email.com",
            telefone="(11) 92109-8765",
            data_ingresso=datetime(2023, 6, 25).date(),
            titulo_projeto="Otimização de consultas em bancos de dados distribuídos",
            area_pesquisa="Banco de Dados",
            tipo="coorientando",
            orientador_principal_id=4  # Pedro Souza
        )
    ]
    
    # Adicionar coorientandos ao banco de dados
    for coorientando in coorientandos:
        db.session.add(coorientando)
    
    db.session.commit()
    
    # Criar marcos para cada orientando
    hoje = datetime.now().date()
    
    for orientando in orientandos:
        # Seminário do primeiro semestre (6 meses após ingresso)
        data_seminario1 = orientando.data_ingresso + relativedelta(months=6)
        status_seminario1 = "concluído" if data_seminario1 < hoje else "pendente"
        data_realizada_seminario1 = data_seminario1 if status_seminario1 == "concluído" else None
        
        marco_seminario1 = Marco(
            orientando_id=orientando.id,
            tipo="Seminário do 1º Semestre",
            data_prevista=data_seminario1,
            data_realizada=data_realizada_seminario1,
            status=status_seminario1,
            observacoes="Apresentação dos resultados preliminares"
        )
        db.session.add(marco_seminario1)
        
        # Seminário do segundo semestre (12 meses após ingresso)
        data_seminario2 = orientando.data_ingresso + relativedelta(months=12)
        status_seminario2 = "concluído" if data_seminario2 < hoje else "pendente"
        data_realizada_seminario2 = data_seminario2 if status_seminario2 == "concluído" else None
        
        marco_seminario2 = Marco(
            orientando_id=orientando.id,
            tipo="Seminário do 2º Semestre",
            data_prevista=data_seminario2,
            data_realizada=data_realizada_seminario2,
            status=status_seminario2,
            observacoes="Apresentação dos resultados parciais"
        )
        db.session.add(marco_seminario2)
        
        # Qualificação (18 meses após ingresso)
        data_qualificacao = orientando.data_ingresso + relativedelta(months=18)
        status_qualificacao = "concluído" if data_qualificacao < hoje else "pendente"
        data_realizada_qualificacao = data_qualificacao if status_qualificacao == "concluído" else None
        
        marco_qualificacao = Marco(
            orientando_id=orientando.id,
            tipo="Qualificação",
            data_prevista=data_qualificacao,
            data_realizada=data_realizada_qualificacao,
            status=status_qualificacao,
            observacoes="Banca de qualificação"
        )
        db.session.add(marco_qualificacao)
        
        # Defesa (24 meses após ingresso)
        data_defesa = orientando.data_ingresso + relativedelta(months=24)
        status_defesa = "concluído" if data_defesa < hoje else "pendente"
        data_realizada_defesa = data_defesa if status_defesa == "concluído" else None
        
        marco_defesa = Marco(
            orientando_id=orientando.id,
            tipo="Defesa",
            data_prevista=data_defesa,
            data_realizada=data_realizada_defesa,
            status=status_defesa,
            observacoes="Defesa final da dissertação"
        )
        db.session.add(marco_defesa)
    
    db.session.commit()
    
    # Criar algumas orientações
    for i, orientando in enumerate(orientandos + coorientandos):
        # Orientação passada (realizada)
        data_passada = datetime.now() - timedelta(days=15 + i)
        orientacao_passada = Orientacao(
            orientando_id=orientando.id,
            data_hora=data_passada,
            duracao_prevista=60,
            status="realizada",
            modalidade="presencial" if i % 2 == 0 else "online",
            local="Sala 101" if i % 2 == 0 else "https://meet.google.com/abc-defg-hij"
        )
        db.session.add(orientacao_passada)
        db.session.commit()  # Commit para garantir que o ID da orientação seja gerado
        
        # Diário para orientação passada
        diario = DiarioOrientacao(
            orientacao_id=orientacao_passada.id,
            topicos_discutidos="Discussão sobre o andamento do projeto e revisão bibliográfica.",
            progresso_observado="O orientando está avançando conforme o cronograma estabelecido.",
            pendencias="Finalizar a revisão bibliográfica e iniciar a coleta de dados.",
            tarefas_atribuidas="1. Concluir a revisão bibliográfica\n2. Preparar o protocolo de coleta de dados\n3. Iniciar a implementação do método proposto",
            prazo_proximas_entregas=(data_passada + timedelta(days=30)).date(),
            avaliacao_progresso="bom"
        )
        db.session.add(diario)
        db.session.commit()  # Commit após cada diário
        
        # Orientação futura (agendada)
        data_futura = datetime.now() + timedelta(days=15 + i)
        orientacao_futura = Orientacao(
            orientando_id=orientando.id,
            data_hora=data_futura,
            duracao_prevista=60,
            status="agendada",
            modalidade="online" if i % 2 == 0 else "presencial",
            local="https://meet.google.com/abc-defg-hij" if i % 2 == 0 else "Sala 102"
        )
        db.session.add(orientacao_futura)
        db.session.commit()  # Commit após cada orientação futura
    
    print("Dados de teste criados com sucesso!")
