import bcrypt
import pyodbc
from datetime import datetime
import pytz
import random
import messagebox as msg
import string
import numpy as np
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from private import APP_KEY, MAIL


# Todos as funções dos CRUDs necessários para o sistema


# Cria um usuário
def create_user(nome, data_nascimento, genero, email, area, cargo, salario, data_admissao):
    """Cadastra um funcionário no banco de dados

    Args:
        nome (str): Nome do funcionário
        data_nascimento (str): Data de nascimento do funcionario no formato DD/MM/AAAA
        genero (str): Gênero do funcionário, podendo ser (Masculino/Feminino/Outros)
        email (str): Email do funcionário
        area (str): Área de atuação do funcionário
        cargo (str): Cargo do funcionário
        salario (int/float): Salário do funcionário
        data_admissao (str): Data de admissão do funcionário no formato DD/MM/AAAA H:M:S
    """
    # Cria a conexão
    dados_conexao = ("Driver={SQLite3 ODBC Driver};"
                "Server=localhost;"
                r"Database=DB\gerenciador.db")
    conexao = pyodbc.connect(dados_conexao)

    cursor = conexao.cursor()

    cursor.execute(f"SELECT COUNT(*) FROM Funcionarios WHERE email = ?", (email))
    if cursor.fetchone()[0] > 0:
        msg.showerror("Erro", "O e-mail inserido já está cadastrado")
        return False
    else:
        
        cursor.execute(f"""
    INSERT INTO Funcionarios ('nome', 'dataNascimento', 'genero', 'email', 'area', 'cargo', 'salario', 'dataAdmissao')
    VALUES
    (?, ?, ?, ?, ?, ?, ?, ?)
    """, (str(nome), str(data_nascimento), str(genero), str(email), str(area), str(cargo), salario, str(data_admissao)))
        

        cursor.commit()

        cursor.close()
        conexao.close
        return True

# Lê o banco de dados
def read_user(nome=None):
    # Define o tipo da busca
    if nome is None:
        busca = f"SELECT * FROM Funcionarios"
    elif nome is not None:
        busca = f"SELECT * FROM Funcionarios Where [nome] = ?"

    # Cria a conexão
    dados_conexao = ("Driver={SQLite3 ODBC Driver};"
                "Server=localhost;"
                r"Database=DB\gerenciador.db")
    conexao = pyodbc.connect(dados_conexao)

    cursor = conexao.cursor()

    cursor.execute(busca, str(nome))

    dados = cursor.fetchall()
    cursor.close()
    return dados

# Cria um admin
def create_admin(nome, user, senha, email, ultimo_acesso):
    """Cadastra um administrador no banco de dados

    Args:
        nome (str): Nome do administrador
        user (str): Nome de usuário do administrador (Usado para fazer login)
        senha (str): Senha do administrador
        email (str): E-mail do administrador
        ultimo_acesso (str): último acesso do administrador no formato DD/MM/AAAA H:M:S
    """
    # Cria a conexão
    dados_conexao = ("Driver={SQLite3 ODBC Driver};"
                "Server=localhost;"
                r"Database=DB\gerenciador.db")
    conexao = pyodbc.connect(dados_conexao)

    cursor = conexao.cursor()

    cursor.execute("""
    INSERT INTO Admins (nome, usuario, senha, email, ultimoAcesso)
    VALUES (?, ?, ?, ?, ?)""",
    (nome, user, hash_password(senha), email, ultimo_acesso))

    cursor.commit()

    cursor.close()

# Deleta um admin
def delete_admin(user, email):

    # Cria a conexão
    dados_conexao = ("Driver={SQLite3 ODBC Driver};"
                "Server=localhost;"
                r"Database=DB\gerenciador.db")
    conexao = pyodbc.connect(dados_conexao)
    cursor = conexao.cursor()

    cursor.execute("DELETE FROM Admins WHERE usuario = ? AND email = ?", (user, email))

    cursor.commit()
    cursor.close()
    conexao.close()

# Autentica um admin
def auth_admin(login, password):
    # Conexão com o banco de dados
    dados_conexao = ("Driver={SQLite3 ODBC Driver};"
                     "Server=localhost;"
                     r"Database=DB\gerenciador.db")
    try:
        conexao = pyodbc.connect(dados_conexao)
        cursor = conexao.cursor()

        cursor.execute("SELECT senha FROM Admins WHERE usuario = ? OR email = ?", (login, login))
        resultado = cursor.fetchone()  # Resultado da busca
        cursor.close()
        conexao.close()

        if resultado:
            senha_hash = resultado[0].strip()  # Obter senha e remover espaços extras
            if bcrypt.checkpw(password.encode("utf-8"), senha_hash.encode("utf-8")):
                return True
        return False

    except pyodbc.Error as e:
        print(f"Erro ao autenticar o administrador: {e}")
        return False

# Criptografa uma determinada senha
def hash_password(password):
    """Criptografa a senha determinada

    Args:
        password (str): Senha que será criptografada
    
    Returns:
        Senha criptografada
    
    """
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')

# Pega data e hora atuais
def timenow():
    """Pega a data e hora atuais

    Returns:
        data e hora formatados
    """
    fuso_br = pytz.timezone("America/Sao_Paulo")
    return datetime.now(fuso_br).strftime("%d/%m/%Y %H:%M:%S")

# Cria um código de recuperação, atribui ao BD e envia por e-mail
def recover_pass(email, user):
    code = "".join(random.choices(string.ascii_letters.upper() + string.digits, k=5))  #  Cria o código de recuperação
    def send_mail():
        # Configurações do servidor SMTP do Gmail
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587  # Porta para conexão TLS
        sender_email = MAIL  # Seu e-mail do Gmail
        sender_password = APP_KEY   # senha do Gmail

        # Destinatário e corpo do e-mail
        recipient_email = email
        subject = 'Redefinição de senha'
        body = f'<p>Seu código de redefinição de senha é: <b>{code}</b></p>'

        # Criar mensagem
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'html'))

        # Conectar ao servidor SMTP do Gmail e enviar e-mail
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()  # Habilitar TLS
            server.login(sender_email, sender_password)
            text = message.as_string()
            server.sendmail(sender_email, recipient_email, text)
            print('E-mail enviado com sucesso!')
        except Exception as e:
            print(f'Erro ao enviar e-mail: {str(e)}')
        finally:
            server.quit()  # Encerrar conexão com o servidor SMTP

    def create_code():
        try:
            dados_conexao = ("Driver={SQLite3 ODBC Driver};"
                    "Server=localhost;"
                    r"Database=DB\gerenciador.db")
            conexao = pyodbc.connect(dados_conexao)

            cursor = conexao.cursor()
            cursor.execute("UPDATE Admins SET [codigoTemporario] = ? WHERE email = ? AND usuario = ?", (code, email, user))
            cursor.commit()
            cursor.close()
            conexao.close()
            return True
        except Exception as e:
            print(e)
            return False

    if create_code():
        send_mail()

# Verifica se um email está no BD
def verify_email(email):
    # Conexão com o banco de dados
    dados_conexao = ("Driver={SQLite3 ODBC Driver};"
                "Server=localhost;"
                r"Database=DB\gerenciador.db")
    conexao = pyodbc.connect(dados_conexao)

    cursor = conexao.cursor()

    cursor.execute(f"SELECT email FROM Admins WHERE email = ?", (email))
    resultado = cursor.fetchone()  # Resultado da busca
    cursor.close()
    conexao.close()

    if resultado is not None:
        return True
    else:
        return False

# Verifica se o usuário corresponde ao email inserido
def verify_user(email, user):
    # Conexão com o banco de dados
    dados_conexao = ("Driver={SQLite3 ODBC Driver};"
                "Server=localhost;"
                r"Database=DB\gerenciador.db")
    conexao = pyodbc.connect(dados_conexao)

    cursor = conexao.cursor()

    cursor.execute(f"SELECT usuario FROM Admins WHERE email = ? AND usuario = ?", (email, user))
    resultado = cursor.fetchval()  # Resultado da busca
    cursor.close()
    conexao.close()

    if resultado is not None:
        return True
    else:
        return False

# Verifica se o código inserido corresponde ao recebido por email
def verify_code(email, user, entry_code):
    # Conexão com o banco de dados
    dados_conexao = ("Driver={SQLite3 ODBC Driver};"
                "Server=localhost;"
                r"Database=DB\gerenciador.db")
    conexao = pyodbc.connect(dados_conexao)

    cursor = conexao.cursor()

    cursor.execute(f"SELECT [codigoTemporario] FROM Admins WHERE email = ? AND usuario = ?", (email, user))
    resultado = cursor.fetchval()  # Resultado da busca
    cursor.close()
    conexao.close()

    if entry_code == resultado:
        return True
    else:
        return False

# Redefine a senha de admin
def update_pass(email, user, nova_senha):
    try:
        # Conexão com o banco de dados
        dados_conexao = ("Driver={SQLite3 ODBC Driver};"
                    "Server=localhost;"
                    r"Database=DB\gerenciador.db")
        conexao = pyodbc.connect(dados_conexao)

        cursor = conexao.cursor()

        cursor.execute("UPDATE Admins SET senha = ? WHERE email = ? AND usuario = ?", (hash_password(nova_senha), email, user))

        cursor.commit()

        cursor.close()
        conexao.close()
        return True
    except Exception as e:
        print(e)
        return False

# Atualiza a data e hora do ultimo acesso do administrador
def update_last_access(login, senha):
    dados_conexao = ("Driver={SQLite3 ODBC Driver};"
                    "Server=localhost;"
                    r"Database=DB\gerenciador.db")
    conexao = pyodbc.connect(dados_conexao)

    cursor = conexao.cursor()
    cursor.execute("UPDATE Admins SET [ultimoAcesso] = ? WHERE usuario = ? or email = ? AND senha = ?", (timenow(), login, login, hash_password(senha)))
    cursor.commit()
    cursor.close()
    conexao.close()

#  Pega as informações de um administrador
def get_admin_info(user, email):
     # Conexão com o banco de dados
    dados_conexao = ("Driver={SQLite3 ODBC Driver};"
                "Server=localhost;"
                r"Database=DB\gerenciador.db")
    conexao = pyodbc.connect(dados_conexao)

    cursor = conexao.cursor()

    cursor.execute(f"SELECT nome, email, [ultimoAcesso] FROM Admins WHERE usuario = ? AND email = ?", (user, email))
    resultado = cursor.fetchall()  # Resultado da busca
    cursor.close()
    conexao.close()
    texto = f"""Nome: {resultado[0][0]}

E-mail: {resultado[0][1]}

Último acesso: {resultado[0][2]}"""
    return texto

#  Exclui um administrador
def delete_admin(user, email):
    dados_conexao = ("Driver={SQLite3 ODBC Driver};"
                "Server=localhost;"
                r"Database=DB\gerenciador.db")
    conexao = pyodbc.connect(dados_conexao)

    cursor = conexao.cursor()
    cursor.execute("DELETE FROM Admins WHERE usuario = ? AND email = ?", (user, email))

    cursor.commit()

    if cursor.rowcount > 0:
        cursor.close() 
        conexao.close()
        return True
    else:
        cursor.close() 
        conexao.close()
        return False

#  Exclui o código temporário do BD
def del_code(email, user):
    dados_conexao = ("Driver={SQLite3 ODBC Driver};"
                "Server=localhost;"
                r"Database=DB\gerenciador.db")
    conexao = pyodbc.connect(dados_conexao)

    cursor = conexao.cursor()
    cursor.execute("UPDATE Admins SET [codigoTemporario] = NULL WHERE email = ? AND usuario = ?", (email, user))

    cursor.commit()
    cursor.close()
    conexao.close()

#  Pega os nomes de todos os funcionários
def get_funcionarios():
    # Conexão com o banco de dados
    dados_conexao = ("Driver={SQLite3 ODBC Driver};"
                "Server=localhost;"
                r"Database=DB\gerenciador.db")
    conexao = pyodbc.connect(dados_conexao)

    cursor = conexao.cursor()

    cursor.execute(f"SELECT nome FROM Funcionarios")
    resultado = cursor.fetchall()  # Resultado da busca
    cursor.close()
    conexao.close()
    return [resultado[i][0] for i, row in enumerate(resultado)]

#  Pega os números de funcionários por gênero
def get_gender_stats():
    # Conexão com o banco de dados
    dados_conexao = ("Driver={SQLite3 ODBC Driver};"
                "Server=localhost;"
                r"Database=DB\gerenciador.db")
    conexao = pyodbc.connect(dados_conexao)

    cursor = conexao.cursor()

    cursor.execute(f"SELECT genero FROM Funcionarios WHERE [statusEmprego] != 'Demitido'")
    resultado = cursor.fetchall()  #Resultado da busca
    resultado_tratado = [resultado[i][0] for i, row in enumerate(resultado)]
    cursor.close()
    conexao.close()
    return [resultado_tratado.count("Masculino"), resultado_tratado.count("Feminino"), resultado_tratado.count("Outros")]

# Pega os números de funcionários por área
def get_area_stats():
    # Conexão com o banco de dados
    dados_conexao = ("Driver={SQLite3 ODBC Driver};"
                "Server=localhost;"
                r"Database=DB\gerenciador.db")
    conexao = pyodbc.connect(dados_conexao)

    cursor = conexao.cursor()

    cursor.execute(f"SELECT area FROM Funcionarios WHERE [statusEmprego] != 'Demitido'")
    resultado = cursor.fetchall()  # Resultado da busca
    resultado_tratado = [resultado[i][0] for i, row in enumerate(resultado)]
    cursor.close()
    conexao.close()
    return (list(set(resultado_tratado)), [resultado_tratado.count(i) for i in list(set(resultado_tratado))])

# Converte a data de nascimento em idade
def get_age(born_date):
    """Converte uma data de nascimento em idade

    Args:
        born_date (str): Data de nascimento no formato de string
    
    Returns:
        age (int): Idade no formato inteiro
    
    """
    y = datetime.strptime(born_date, "%d/%m/%Y").date()
    today = datetime.now(pytz.timezone("America/Sao_Paulo")).date()
    return int(str((today - y).days / 365)[:2])

# Pega todas idades com base na data de nascimento de cada funcionário, e conta as ocorrências de cada idade
def get_all_ages():
    """Pega as idades de todos os funcionários do banco de dados e retorna uma tupla com:

        - Lista de idades únicas (sem repetições)
        - Lista de contagens de ocorrências para cada idade

    Returns:
        (list, list): Tupla contendo a lista de idades únicas e a lista de contagens de ocorrências.
    """
    # Conexão com o banco de dados
    dados_conexao = ("Driver={SQLite3 ODBC Driver};"
                "Server=localhost;"
                r"Database=DB\gerenciador.db")
    conexao = pyodbc.connect(dados_conexao)

    cursor = conexao.cursor()

    cursor.execute(f"SELECT [dataNascimento] FROM Funcionarios WHERE [statusEmprego] != 'Demitido'")
    resultado = cursor.fetchall()  # Resultado da busca
    ages_list = [get_age(resultado[i][0]) for i, row in enumerate(resultado)]
    unique_ages = list(set(ages_list))
    cursor.close()
    conexao.close()
    return (unique_ages, [ages_list.count(i) for i in unique_ages])

# Pega o valor de todos os salários dos funcionários
def get_salaries():
    # Conexão com o banco de dados
    dados_conexao = ("Driver={SQLite3 ODBC Driver};"
                "Server=localhost;"
                r"Database=DB\gerenciador.db")
    conexao = pyodbc.connect(dados_conexao)

    cursor = conexao.cursor()

    cursor.execute(f"SELECT salario FROM Funcionarios")
    resultado = cursor.fetchall()  #Resultado da busca
    resultado_tratado = [resultado[i][0] for i, row in enumerate(resultado)]
    cursor.close()
    conexao.close()
    return resultado_tratado

# Pega as informações de um funcionário com base no ID ou Email
def get_employee_info(key):
    # Conexão com o banco de dados
    dados_conexao = ("Driver={SQLite3 ODBC Driver};"
                "Server=localhost;"
                r"Database=DB\gerenciador.db")
    conexao = pyodbc.connect(dados_conexao)

    cursor = conexao.cursor()

    cursor.execute(f"SELECT * FROM Funcionarios WHERE id = ?", (key))
    resultado = cursor.fetchall()  #Resultado da busca
    cursor.close()
    conexao.close()
    if len(resultado) == 1:
        return resultado[0]
    else:
        raise IndexError  # Uso um Except para gerar uma mensagem personalizada com base nesse erro (Promote.widgets linha 36)

# Demite um funcionário (Muda o estado de emprego para "Demitido" e adiciona o ID à tabela de demissões)
def fire_employee(key, motivo, obs):
    dados_conexao = ("Driver={SQLite3 ODBC Driver};"
                "Server=localhost;"
                r"Database=DB\gerenciador.db")
    conexao = pyodbc.connect(dados_conexao)

    cursor = conexao.cursor()
    cursor.execute(f"SELECT nome, email FROM Funcionarios WHERE id = ?", (key))
    resultado = cursor.fetchall()

    nome = resultado[0][0]
    email = resultado[0][1]

    try:

        # Atualiza o status do funcionário
        cursor.execute(f"""
    DELETE FROM Funcionarios 
    WHERE id = ?
    """, (key))
        
        # Atualiza a tabela de férias
        cursor.execute("""
    DELETE FROM Ferias
    WHERE Id_funcionario = ?
    """, (key))
        
        # Atualiza a tabela de horas extras
        cursor.execute("""
    DELETE FROM HorasExtras
    WHERE Id_funcionario = ?
    """, (key))
        
        # Atualiza a tabela de demissões
        cursor.execute("""
    INSERT INTO DemissoesFuncionarios (nome, email, [dataDemissao], motivo, obs)
    VALUES (?, ?, ?, ?, ?)
    """, (str(nome), str(email), timenow()[:10], str(motivo), obs))
        cursor.commit()
        cursor.close()
        conexao.close()
        return True
    except:
        cursor.close()
        conexao.close()
        return False

# Promove um funcionário, alterando seu cargo e salário, e adicionado o resgistro à tabela de promoções
def promote_employee(key, cargo_atual, novo_cargo, motivo, salario_atual, novo_salario):
    dados_conexao = ("Driver={SQLite3 ODBC Driver};"
                "Server=localhost;"
                r"Database=DB\gerenciador.db")
    conexao = pyodbc.connect(dados_conexao)
    cursor = conexao.cursor()

    try:
        # Alterar o cargo e o salario na tabela de funcionários
        cursor.execute("""
    UPDATE funcionarios
    SET cargo = ?, salario = ?
    WHERE id = ?
    """, (novo_cargo, novo_salario, key))
        
        # Adicionar a promoção à tabela de promoções
        cursor.execute(f"""
    INSERT INTO PromocoesFuncionarios ([Id_funcionario], [dataPromocao], [cargoAnterior], [novoCargo], [motivoPromocao], [salarioAnterior], [novoSalario])
    VALUES ('{key}', '{timenow()[:10]}', '{cargo_atual}', '{novo_cargo}', '{motivo}', {float(salario_atual)}, {float(novo_salario)})
    """)

        # Commitar as alterações
        cursor.commit()
        cursor.close()
        conexao.close()
        return True
    
    except Exception as e:
        cursor.close()
        conexao.close()
        print(e)
        return False

# Pega o nome de um funcionário através do ID
def get_employee_name(id):
    # Conexão com o banco de dados
    dados_conexao = ("Driver={SQLite3 ODBC Driver};"
                "Server=localhost;"
                r"Database=DB\gerenciador.db")
    conexao = pyodbc.connect(dados_conexao)

    cursor = conexao.cursor()

    cursor.execute(f"SELECT nome FROM funcionarios WHERE id = ?", (id))
    resultado = cursor.fetchval()  #Resultado da busca
    cursor.close()
    conexao.close()
    if resultado is not None:
        return resultado
    else:
        return ""

# Adiciona um registro de hora extra no banco de dados
def register_overtime(id, data_registro, horas, motivo):
    # Conexão com o banco de dados
    dados_conexao = ("Driver={SQLite3 ODBC Driver};"
                "Server=localhost;"
                r"Database=DB\gerenciador.db")
    conexao = pyodbc.connect(dados_conexao)

    cursor = conexao.cursor()

    cursor.execute(f"""
INSERT INTO HorasExtras ([Id_funcionario], [dataRegistro], horas, motivo)
VALUES ({id}, '{data_registro}', {horas}, '{motivo}')
                   """)
    cursor.commit()

    cursor.close()
    conexao.close()

# Pega a soma das horas extras registradas no banco de dados
def get_total_overtime():
    # Conexão com o banco de dados
    dados_conexao = ("Driver={SQLite3 ODBC Driver};"
                "Server=localhost;"
                r"Database=DB\gerenciador.db")
    conexao = pyodbc.connect(dados_conexao)

    cursor = conexao.cursor()

    cursor.execute(f"SELECT horas FROM HorasExtras")
    resultado = cursor.fetchall()  #Resultado da busca
    list = [resultado[i][0] for i, row in enumerate(resultado)]
    cursor.close()
    conexao.close()
    if sum(list) > 0:
        return list
    else:
        return 0

# Pega a média de horas extras por funcionário
def get_avg_overtime():
    return round(np.average(get_total_overtime()), 1)

# Pega as informações de horas extras por área
def get_overtime_stats():

    # Pegar todas as áreas

    # Conexão com o banco de dados
    dados_conexao = ("Driver={SQLite3 ODBC Driver};"
                "Server=localhost;"
                r"Database=DB\gerenciador.db")
    conexao = pyodbc.connect(dados_conexao)

    cursor = conexao.cursor()

    cursor.execute(f"SELECT area FROM funcionarios")
    resultado = cursor.fetchall()  #Resultado da busca
    resultado_tratado = [resultado[i][0] for i, row in enumerate(resultado)]
    areas = list(set(resultado_tratado))
    cursor.close()
    conexao.close()
    
    # Pegar a quantidade de horas extras por funcionários
    dados_conexao = ("Driver={SQLite3 ODBC Driver};"
                "Server=localhost;"
                r"Database=DB\gerenciador.db")
    conexao = pyodbc.connect(dados_conexao)

    cursor = conexao.cursor()

    cursor.execute(f"SELECT [Id_funcionario], horas FROM HorasExtras")
    infos = cursor.fetchall()  #Resultado da busca
    cursor.close()
    conexao.close()

    ids = [i[0] for i in infos]  # Lista com os ids
    hours = [i[1] for i in infos]  # Lista com a quantidade de horas extras
    id_areas = []

    for id in ids:
        dados_conexao = ("Driver={SQLite3 ODBC Driver};"
                "Server=localhost;"
                r"Database=DB\gerenciador.db")
        conexao = pyodbc.connect(dados_conexao)

        cursor = conexao.cursor()

        cursor.execute(f"SELECT area FROM funcionarios WHERE id = ?", (id))
        area = cursor.fetchval()  #Resultado da busca
        cursor.close()
        conexao.close()
        id_areas.append(area)

    dict_hours = {}

    # Agrupar as áreas e horas extras em uma só
    for area, horas in zip(id_areas, hours):
        if area not in dict_hours:
            dict_hours[area] = horas
        else:
            dict_hours[area] += horas
        
    return (list(dict_hours.keys()), list(dict_hours.values()))  # ([areas], [horas])

# Pega o total de salários por área
def get_area_salaries():
    # Conexão com o banco de dados
    dados_conexao = ("Driver={SQLite3 ODBC Driver};"
                "Server=localhost;"
                r"Database=DB\gerenciador.db")
    conexao = pyodbc.connect(dados_conexao)

    cursor = conexao.cursor()

    cursor.execute(f"SELECT area, salario FROM funcionarios")
    resultado = cursor.fetchall()  #Resultado da busca
    areas = [resultado[i][0] for i, row in enumerate(resultado)]
    salarios = [resultado[i][1] for i, row in enumerate(resultado)]
    # areas = list(set(resultado_tratado))
    cursor.close()
    conexao.close()
    
    dict = {}

    for area, sal in zip(areas, salarios):
        if area not in dict:
            dict[area] = sal
        else:
            dict[area] += sal
    
    return (list(dict.keys()), list(dict.values()))

# Pega o salário por ID de funcionário
def get_salaries_id():
    # Conexão com o banco de dados
    dados_conexao = ("Driver={SQLite3 ODBC Driver};"
                "Server=localhost;"
                r"Database=DB\gerenciador.db")
    conexao = pyodbc.connect(dados_conexao)

    cursor = conexao.cursor()

    cursor.execute(f"SELECT id, salario FROM funcionarios")
    resultado = cursor.fetchall()  #Resultado da busca
    ids = [resultado[i][0] for i, row in enumerate(resultado)]
    salarios = [resultado[i][1] for i, row in enumerate(resultado)]
    # areas = list(set(resultado_tratado))
    cursor.close()
    conexao.close()
    return (ids, salarios)

# Registra férias no id de um funcionário
def register_vacation(id, data_inicio, data_fim, motivo):
    # Conexão com o banco de dados
    dados_conexao = ("Driver={SQLite3 ODBC Driver};"
                "Server=localhost;"
                r"Database=DB\gerenciador.db")
    conexao = pyodbc.connect(dados_conexao)

    cursor = conexao.cursor()

    cursor.execute(f"""
INSERT INTO Ferias ([Id_funcionario], [dataInicio], [dataFim], motivo)
VALUES ({id}, '{data_inicio}', '{data_fim}', '{motivo}')
                   """)
    cursor.commit()

    cursor.close()
    conexao.close()

# Pega o histórico de férias de um funcionário
def get_vacations(id):
    # Conexão com o banco de dados
    dados_conexao = ("Driver={SQLite3 ODBC Driver};"
                "Server=localhost;"
                r"Database=DB\gerenciador.db")
    conexao = pyodbc.connect(dados_conexao)

    cursor = conexao.cursor()

    cursor.execute(f"SELECT [dataInicio], [dataFim] FROM Ferias WHERE [Id_funcionario] = ?", (id))
    resultado = cursor.fetchall()  #Resultado da busca
    resultado_tratado = [i for i in resultado]
    cursor.close()
    conexao.close()

    if len(resultado_tratado) > 0:
        return resultado_tratado
    else:
        return False
