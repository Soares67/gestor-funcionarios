import messagebox as msg
import config
import string
import matplotlib.pyplot as plt
import os


#Abre/Fecha um frame
def open_close_frame(botao, states):
    """Expande/Encolhe um frame
    
    Args:
        botao (tk.Button): Botão que fará a ação
        states (dict): dicionário com o formato: {tk.Frame: "epanded/reduced"}
    """
    if states[botao.name][1] == "reduced":
        m_frame = states[botao.name][0]
        m_frame.configure(width=1380)
        states[botao.name][1] = "expanded"
        for i in states:
            if states[i][0] != m_frame and states[i][1] == "expanded":
                states[i][0].configure(width=1)
                states[i][1] = "reduced"
            else:
                pass
    elif states[botao.name][1] == "expanded":
        m_frame = states[botao.name][0]
        m_frame.configure(width=1)
        states[botao.name][1] = "reduced"

#Verifica se duas senhas se coincidem     
def check(senha1, senha2):
    """Checa se duas senhas se coincidem
    
    Args:
        senha1 (str): Primeira senha
        senha2 (str): Segunda senha
    
    Returns:
        bool
    """
    if senha1 == senha2:
        return True
    else:
        return False

#Verifica se as senhas atendem aos requisitos
def check_req(senha1, senha2):
    """Checa se duas senhas possuem no mínimo 8 dígitos
    
    Args:
        senha1 (str): Primeira senha
        senha2 (str): Seguinda senha

    Returns:
        bool
    """
    if len(senha1) >= 8 and len(senha2) >= 8:
        return True
    else:
        return False

#Verifica se um campo atende os requisitos
def check_field(field, min_len):
    """Checa se um campo possui a qtde mínima de dígitos
    
    Args:
        field (str): Campo que será checado
        min_len (int): Quantidade mínima de caracteres
    
    Returns:
        bool
    """
    if len(field) >= min_len:
        return True
    else:
        return False

# Checa um campo de nomes
def check_name(name):
    """Verifica se um nome está em um formato válido.

    Args:
        name (str): O nome a ser verificado.

    Returns:
        bool: True se o nome estiver em um formato válido, False caso contrário.
    """
    if name:  # Não pode estar em branco
        if len(name.strip()) >= 5:  # No mínimo 5 dígitos
            if len(name.split()) >= 2:  # No mínimo 2 palavras (deve ser composto)
                return True
            else:
               msg.showwarning("Erro", "O nome deve ter pelo menos duas palavras")
               return False
        else:
            msg.showwarning("Erro", "O nome deve ter no mínimo 5 caracteres")
            return False
    else:
        msg.showwarning("Erro", "O nome não pode estar em branco")
        return False
            
# Checa um campo de datas com regras específicas
def check_date(date, alert = True):
    """Verifica se a data fornecida está no formato válido (DD/MM/AAAA) e se está dentro dos limites permitidos.

    Args:
        date (str): A data no formato DD/MM/AAAA a ser verificada.

    Returns:
        bool: True se a data estiver no formato válido e dentro dos limites permitidos, False caso contrário.
    """
    if date:  # Não pode estar em branco
        parts = date.split("/")
        if len(parts) == 3:  # DD/MM/AAAA
            day, month, year = parts
            try:
                day = int(day)
                month = int(month)
                year = int(year)
            except ValueError:
                if alert:
                    msg.showwarning("Erro", "A data deve conter apenas números")
                return False
            
            if 1 <= month <= 12:  # Mês deve estar entre 1 e 12
                if int(config.timenow()[6:10]) - year <= 70:
                    if 1 <= day <= 31:  # Dia deve estar entre 1 e 31
                        if month == 2:  # Fevereiro
                            if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:  # Ano bissexto
                                max_days = 29
                            else:
                                max_days = 28
                            if day <= max_days:
                                return True
                            else:
                                if alert:
                                    msg.showwarning("Erro", "Dia inválido para fevereiro")
                                return False
                        elif month in [4, 6, 9, 11]:  # Abril, junho, setembro, novembro
                            if day <= 30:
                                return True
                            else:
                                if alert:
                                    msg.showwarning("Erro", "Dia inválido para o mês")
                                return False
                        else:
                            return True
                    else:
                        if alert:
                            msg.showwarning("Erro", "Dia deve estar entre 1 e 31")
                        return False
                else:
                    if alert:
                        msg.showwarning("Erro", "A idade máxima é de 70 anos")
                    return False
            else:
                if alert:
                    msg.showwarning("Erro", "Mês deve estar entre 1 e 12")
                return False
        else:
            if alert:
                msg.showwarning("Erro", "Data deve estar no formato DD/MM/AAAA")
            return False
    else:
        if alert:
            msg.showwarning("Erro", "O campo deve estar preenchido")
        return False

# Checa se um email é válido
def check_email(email):
    """Verifica se um endereço de email é válido de acordo com os critérios especificados.

    Args:
        email (str): O endereço de email a ser verificado.

    Returns:
        bool: True se o endereço de email for válido, False caso contrário.
    """
    SERVERS = [
    "gmail.com",
    "outlook.com",
    "yahoo.com",
    "icloud.com",
    "aol.com",
    "hotmail.com"
]
    if email:  # Não pode estar em branco
        if len(email) >= 15:  # No mínimo 15 dígitos
            if email.endswith(".com"):
                # Verifica se a local part do email é válida
                for i in email.split("@")[0]:
                    if i in string.ascii_lowercase or i in string.ascii_uppercase or i in string.digits or i == ".":
                        pass
                    else:
                        msg.showwarning("Erro", f"O email digitado possui dígitos inválidos: {i}")
                        return False
                # Verifica se o servidor do email é válido
                valido = False  # Variável de controle
                for server in SERVERS:
                    if server in email:
                        valido = True
                        break
                if valido:
                    valido = False
                    return True
                else:
                    msg.showwarning("Erro", "O servidor do email é inválido")
                    return False
                
            else:
                msg.showwarning("Erro", "O email deve terminar com (.com)")
                return False
        else:
            msg.showwarning("Erro", "O email deve ter no mínimo 15 dígitos")
            return False
    else:
        msg.showwarning("Erro", "O email não pode estar em branco")
        return False

# Checa um campo de salário
def check_salary(salary):
    """
    Verifica se o salário fornecido atende aos critérios.

    Args:
        salary (float or str): O salário a ser verificado.

    Returns:
        bool: True se o salário atender aos critérios, False caso contrário.
    """
    if len(str(salary).replace(",", "").replace(".", "")) >= 4:  # Deve ter no mínimo 4 dígtos
        return True
    else:
        msg.showwarning("Erro", "O salário deve ter no mínimo 4 dígitos")
        return False

# Converte um número padrão brasileiro em float
def convert_salary(salary):
    """Converte um formato de string de salário padrão brasileiro para float.

    Args:
        salary (str): O salário no formato de string

    Returns:
        float: O salário convertido para float.
    """
    try:
        salary = float(salary.replace(".", "").replace(",", "."))  # No caso de "1.200,50"
    except:
        salary = float(salary.replace(",", "."))  # No caso de "1200,50"
    else:
        salary = float(salary)  # No caso de nenhuma das alternativas acima
    finally:
        return salary

# Cria e salva o gráfico dos gêneros
def plotnsave_genders():
    """Cria e salva um gráfico de pizza com as estatísticas de gênero dos funcionários

    Args:
        qty (list): Quantidade de funcionários na seguinte ordem: [Masculino, Feminino, Outros]
    
    """
    colors = ["#60a5fa", "#f472b6", "#9ca3af"]
    genders = ["Masculino", "Feminino", "Outros"]

    fig, ax = plt.subplots(figsize=(4,3))

    ax.pie(config.get_gender_stats(), labels=genders, startangle=80, autopct="%1.1f%%", colors=colors)
    ax.set_title("Funcionários por gênero")
    
    plt.savefig(r"Charts\genders_chart.png")

# Cria e salva o gráfico das áreas
def plotnsave_areas():
    """Plota e salva um gráfico de donut com as estatísticas de áreas dos funcionários

    Args:
        areas (list): Lista com os nomes das áreas dos funcionários
        qty_areas (list): Lista com a quantidade de funcionários nas respectivas áreas
    
    """
    area_colors = ["#34d399", "#a78bfa", "#fb7185", "#818cf8", "#facc15", "#fb923c", "#22d3ee", "#a3e635", "#63B3ED", "#f8a5c2"]

    fig, ax = plt.subplots(figsize=(4,3))
    areas, qty_areas = config.get_area_stats()

    ax.pie(qty_areas, labels=areas, startangle=90, autopct="%1.1f%%", colors=area_colors, wedgeprops=dict(width=0.57))
    ax.set_title("Funcionários por área")

    plt.savefig(r"Charts\areas_chart.png")

# Cria e salva o gráfico das idades
def plotnsave_ages():
    """Plota um gráfico de barras com as estatísticas das idades dos funcionários

    Args:
        unique_ages (list): Lista de todas as idades únicas dos funcionários (os números não se repetem)
        qty_ages (list): Lista com a quantidade de ocorrências das idades únicas dos funcionários
    
    """

    colors = [
    "#34d399", "#a78bfa", "#fb7185", "#818cf8", "#facc15",
    "#ff6b6b", "#7f9cf5", "#f3a683", "#63b3ed", "#f8a5c2",
    "#00adb5", "#ffc75f", "#8338ec", "#f6416c", "#ffafcc",
    "#00f5d4", "#ff9f1c", "#7ed6df", "#8ac926", "#ff9b54",
    "#1982c4", "#d4a5a5", "#303960", "#d00000", "#8c5383",
    "#34c8ff", "#eb4d4b", "#3ae374", "#d35400", "#9b59b6",
    "#45aaf2", "#ff9f43", "#8e44ad", "#2ecc71", "#f368e0",
    "#10ac84", "#ff793f", "#2f3640", "#ff5252", "#22a6b3",
    "#f39c12", "#2d3436", "#e74c3c", "#1289a7", "#ffda79",
    "#ff6b81", "#00a8ff", "#6ab04c", "#f7d794", "#70a1ff",
    "#ff9ff3", "#70a1ff", "#70a1ff", "#2c2c54", "#f7f1e3",
    "#58b19f", "#ffa502", "#ff7f50", "#7efff5", "#474787",
    "#ced6e0", "#ffcccc", "#ff7979", "#badc58", "#f8a5c2",
    "#f3a683", "#ff9ff3", "#7ed6df", "#b33771", "#6d214f",
    "#8c7ae6", "#d63031", "#fbc531", "#4cd137", "#c56cf0",
    "#54a0ff", "#00d8d6", "#ff3f34", "#ffcccc", "#9c88ff",
    "#00cec9", "#fbc531", "#6ab04c", "#eb4d4b", "#ff3f34",
    "#c8d6e5", "#44bd32", "#2d3436", "#a29bfe", "#ff3f34",
    "#c8d6e5", "#6c5ce7", "#e15f41", "#34ace0", "#00a8ff",
    "#ff3f34", "#34ace0", "#ff6b6b", "#22a6b3", "#1dd1a1",
    "#54a0ff", "#6ab04c", "#ff5252", "#ff793f", "#f368e0",
    "#00a8ff", "#f39c12", "#273c75", "#130f40", "#95afc0"
]
    
    fig, ax = plt.subplots(figsize=(12,3))

    unique_ages, qty_ages = config.get_all_ages()

    ax.bar(unique_ages, qty_ages, label=colors[:len(unique_ages)], color=colors[:len(unique_ages)])

    ax.set_ylabel('Quantidade')
    ax.set_title('Funcionários por idade')
    ax.set_xticks(unique_ages)

    plt.savefig(r"Charts\ages_chart")

# Atualiza as informações dos gráficos
def update_charts():
    def delete_file(path_list):
        for path in path_list:
            if os.path.exists(path):
                os.remove(path)
    
    delete_file([r'Charts\genders_chart.png', r'Charts\areas_chart.png', r'Charts\ages_chart.png'])

    plotnsave_genders()
    plotnsave_areas()
    plotnsave_ages()

# Converte um float em padrão brasileiro
def float_to_rs(salary):
    """Converte um número float em padrão brasileiro

    Args:
        salary (float): Número que será convertido
    
    Returns:
        Número formatado
    """
    return f"{salary:,.2f}".replace(".", ",").replace(",", ".", 1)

# Cria e salva o gráfico das horas extras por área
def plotnsave_overtime():
    areas, horas = config.get_overtime_stats()

    colors = [
    "#34d399", "#a78bfa", "#fb7185", "#818cf8", "#facc15",
    "#ff6b6b", "#7f9cf5", "#f3a683", "#63b3ed", "#f8a5c2",
    "#00adb5", "#ffc75f", "#8338ec", "#f6416c", "#ffafcc",
    "#00f5d4", "#ff9f1c", "#7ed6df", "#8ac926", "#ff9b54",
]
    
    bar_labels = colors[:len(areas)]
    bar_colors = colors[:len(areas)]

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(areas, horas, label=bar_labels, color=bar_colors)
    ax.set_ylabel("Quantidade")
    plt.savefig(r"Charts\overtime_chart")

# Cria e salva o gráfico de salários por área
def plotnsave_salaries():
    areas, salaries = config.get_area_salaries()
    colors = ["#34d399", "#a78bfa", "#fb7185", "#818cf8", "#facc15", "#fb923c", "#22d3ee", "#a3e635", "#63B3ED", "#f8a5c2"]
    bar_labels = colors[:len(areas)]
    bar_colors = colors[:len(areas)]

    fig, ax = plt.subplots(figsize=(6, 3))
    ax.bar(areas, salaries, label=bar_labels, color=bar_colors)
    ax.set_ylabel("Quantidade")
    ax.set_title('Total de Salários por Área')
    plt.savefig(r"Charts\area_salary_chart")

# Cria e salva o gráfico de salários por ID
def plotnsave_salaries_id():

    ids, salaries = config.get_salaries_id()
    colors = [
    "#34d399", "#a78bfa", "#fb7185", "#818cf8", "#facc15",
    "#ff6b6b", "#7f9cf5", "#f3a683", "#63b3ed", "#f8a5c2",
    "#00adb5", "#ffc75f", "#8338ec", "#f6416c", "#ffafcc",
    "#00f5d4", "#ff9f1c", "#7ed6df", "#8ac926", "#ff9b54",
    "#1982c4", "#d4a5a5", "#303960", "#d00000", "#8c5383",
    "#34c8ff", "#eb4d4b", "#3ae374", "#d35400", "#9b59b6",
    "#45aaf2", "#ff9f43", "#8e44ad", "#2ecc71", "#f368e0",
    "#10ac84", "#ff793f", "#2f3640", "#ff5252", "#22a6b3",
    "#f39c12", "#2d3436", "#e74c3c", "#1289a7", "#ffda79",
    "#ff6b81", "#00a8ff", "#6ab04c", "#f7d794", "#70a1ff",
    "#ff9ff3", "#70a1ff", "#70a1ff", "#2c2c54", "#f7f1e3",
    "#58b19f", "#ffa502", "#ff7f50", "#7efff5", "#474787",
    "#ced6e0", "#ffcccc", "#ff7979", "#badc58", "#f8a5c2",
    "#f3a683", "#ff9ff3", "#7ed6df", "#b33771", "#6d214f",
    "#8c7ae6", "#d63031", "#fbc531", "#4cd137", "#c56cf0",
    "#54a0ff", "#00d8d6", "#ff3f34", "#ffcccc", "#9c88ff",
    "#00cec9", "#fbc531", "#6ab04c", "#eb4d4b", "#ff3f34",
    "#c8d6e5", "#44bd32", "#2d3436", "#a29bfe", "#ff3f34",
    "#c8d6e5", "#6c5ce7", "#e15f41", "#34ace0", "#00a8ff",
    "#ff3f34", "#34ace0", "#ff6b6b", "#22a6b3", "#1dd1a1",
    "#54a0ff", "#6ab04c", "#ff5252", "#ff793f", "#f368e0",
    "#00a8ff", "#f39c12", "#273c75", "#130f40", "#95afc0"
]

    bar_labels = colors[:len(ids)]
    bar_colors = colors[:len(ids)]

    fig, ax = plt.subplots(figsize=(15, 4))
    ax.bar(ids, salaries, label=bar_labels, color=bar_colors)
    ax.set_ylabel("Salário")
    plt.xticks(rotation=75)
    ax.set_xticks(ids)
    ax.set_title('Salário Bruto por Funcionário')
    plt.savefig(r"Charts\salary_chart")

# Converte um intervalo em uma sequência
def interval_to_sequence(intervals):
    def is_leap_year(year):
        """Verifica se um ano é bissexto.

        Args:
            year (int): O ano a ser verificado.

        Returns:
            bool: True se o ano for bissexto, False caso contrário.
        """
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    def days_in_month(month, year):
        """Obtém o número de dias em um determinado mês de um ano.

        Args:
            month (int): O mês (1 a 12).
            year (int): O ano.

        Returns:
            int: O número de dias no mês especificado.
        """
        if month in {1, 3, 5, 7, 8, 10, 12}:
            return 31
        elif month in {4, 6, 9, 11}:
            return 30
        elif month == 2:
            return 29 if is_leap_year(year) else 28

    def convert(start_date, end_date):
        """Converte um intervalo de datas em um dicionário com a sequência de datas entre os intervalos.

        Args:
            start_date (str): Data inicial do intervalo no formato DD/MM/YYYY
            end_date (str): Data final do intervalo no formato DD/MM/YYYY

        Returns:
            dict: Dicionário com a sequência de datas.
        """
        start_day, start_month, start_year = map(int, start_date.split('/'))
        end_day, end_month, end_year = map(int, end_date.split('/'))

        result_dict = {}
        current_day = start_day
        current_month = start_month
        current_year = start_year

        while current_year < end_year or (current_year == end_year and current_month <= end_month):
            days_in_current_month = days_in_month(current_month, current_year)
            while current_day <= days_in_current_month and (
                    (current_year < end_year) or 
                    (current_year == end_year and current_month < end_month) or 
                    (current_year == end_year and current_month == end_month and current_day <= end_day)):
                result_dict[(current_day, current_month, current_year)] = 10
                current_day += 1
            current_day = 1
            current_month += 1
            if current_month == 13:
                current_month = 1
                current_year += 1

        return result_dict

    final_result = {}
    for start_date, end_date in intervals:
        interval_result = convert(start_date, end_date)
        final_result.update(interval_result)

    return final_result
