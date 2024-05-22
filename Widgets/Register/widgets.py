import customtkinter as ctk
from Icons.iconspath import EMPLOYEES_IMG, REFRESH_ICON
import functions
import messagebox as msg
import config

# Função principal
def register_widgets(master):

    # Control Vars
    actual_filter = None
    labels = []
    lista_funcionarios = config.get_funcionarios()
    
    # Exibe os nomes dos funcionários
    def list_employees(frame, lista):
        for i in lista:
            name = ctk.CTkLabel(frame, font=("Arial", 18, "bold"), text_color="black", text=i)
            name.pack(pady=2)
            labels.append(name)

    # Limpa os nomes
    def clear_names():
        for label in labels:
            label.destroy()

    # Atualiza a lista de nomes
    def refresh_func():
        global lista_funcionarios
        clear_names()
        lista_funcionarios = config.get_funcionarios()
        list_employees(emp_list, lista_funcionarios)

    # Aplica o filtro de ordem e atualiza a lista
    def onclick(var):
        if var == "A-Z":
            clear_names()
            lista_funcionarios = config.get_funcionarios()
            lista_funcionarios.sort()
            list_employees(emp_list, lista_funcionarios)
        elif var == "Z-A":
            clear_names()
            lista_funcionarios = config.get_funcionarios()
            lista_funcionarios.sort(reverse=True)
            list_employees(emp_list, lista_funcionarios)

    # Função do botão de registro
    def register_checker(name, bn_date, email, area, position, salary, gender):
        if functions.check_name(name):
            if functions.check_date(bn_date):
                if gender != "Gênero":
                  if functions.check_email(email):
                      if functions.check_field(area, 2):
                          if functions.check_field(position, 2):
                              if functions.check_salary(salary):
                                if msg.askyesnocancel("Atenção", f"""
O funcionário será cadastrado com os seguintes dados:
                                                     
Nome: {name}
Data de nascimento: {bn_date}
Genero: {gender}
E-mail: {email}
Área: {area}
Cargo: {position}
Salário: {salary}

Deseja confirmar a ação?
"""):
                                    try:
                                        if config.create_user(name.capitalize(),
                                                           bn_date,
                                                           gender,
                                                           email,
                                                           area,
                                                           position,
                                                           functions.convert_salary(salary),
                                                           config.timenow()[:10]):
                                            msg.showinfo("Atenção", "Funcionário cadastrado com sucesso")
                                            name_entry.delete(0, "end")
                                            bdt_entry.delete(0, "end")
                                            gen_options.set("Gênero")
                                            email_entry.delete(0, "end")
                                            area_entry.delete(0, "end")
                                            pos_entry.delete(0, "end")
                                            wag_entry.delete(0, "end")
                                    except:
                                        msg.showerror("Erro", "Não foi possível realizar o cadastro. Tente novamente")
                          else:
                              msg.showwarning("Erro", "O campo de cargo deve ter no mínimo 2 dígitos")
                      else:
                              msg.showwarning("Erro", "O campo de área deve ter no mínimo 2 dígitos")
                else:
                    msg.showwarning("Erro", "Escolha uma opção para o gênero")

    # Frame da imagem
    img_frame = ctk.CTkFrame(master,
                             fg_color="#FB9C8D",
                             width=404,
                             height=300,
                             corner_radius=0
                             )
    img_frame.place(x=0,y=0)

    # Imagem
    image_lb = ctk.CTkLabel(img_frame,
                            text="",
                            image=EMPLOYEES_IMG
                            )
    image_lb.place(x=15,y=20)

    # Frame da lista de funcionários
    list_frame = ctk.CTkFrame(master,
                              fg_color="#fb9c8d",
                              width=400,
                              height=418,
                              corner_radius=0
                              )
    list_frame.place(x=0,y=300)

    # Frame do cabeçalho da lista de funcionários
    list_header_frame = ctk.CTkFrame(list_frame,
                                     fg_color="#0891b2",
                                     width=410,
                                     height=50,
                                     corner_radius=0
                                    )
    list_header_frame.place(x=0,y=0)

    # Cabeçalho da lista de funcionários
    list_header = ctk.CTkLabel(list_header_frame,
                               text="Funcionários",
                               font=("Arial", 26, "bold"),
                               text_color="white"
                               )
    list_header.place(x=117,y=12)

    # Filtro de ordem dos funcionários
    search_filter = ctk.CTkComboBox(list_header_frame,
                                    width=100,
                                    height=40,
                                    values=["A-Z", "Z-A"],
                                    font=("Arial", 13, "bold"),
                                    dropdown_font=("Arial", 13, "bold"),
                                    corner_radius=20,
                                    variable=actual_filter,
                                    fg_color="#171717",
                                    button_color="#FB9C8D",
                                    button_hover_color="#d47770",
                                    command=lambda actual_filter: onclick(actual_filter),
                                    border_color="#FB9C8D"
                                    )
    search_filter.set("Filtro")
    search_filter.place(x=300,y=5)

    # Botão de atualizar a lista de funcionários
    refresh_button = ctk.CTkButton(list_header_frame,
                                   text="",
                                   width=40,
                                   height=48,
                                   image=REFRESH_ICON,
                                   command=lambda: refresh_func(),
                                   corner_radius=50,
                                   fg_color="transparent",
                                   hover_color="#155e75"
                                   )
    refresh_button.place(x=13,y=1)

    # Lista de funcionários
    emp_list = ctk.CTkScrollableFrame(list_frame,
                                      width=370,
                                      height=348,
                                      fg_color="#cbd5e1",
                                      )
    emp_list.place(x=4,y=54)

    # Frame principal
    main_frame = ctk.CTkFrame(master,
                              fg_color="#0891b2",
                              width=948,
                              height=718,
                              corner_radius=0,
                              )
    main_frame.place(x=400,y=0)

    # Título do frame principal
    title = ctk.CTkLabel(main_frame,
                         text="Registrar Funcionário",
                         font=("Arial", 30, "bold"),
                         text_color="white"
                         )
    title.place(x=331,y=29)
    
    # Entry do nome
    name_entry = ctk.CTkEntry(main_frame,
                              width=365,
                              height=56,
                              placeholder_text="Nome completo",
                              font=("Arial", 16, "bold"),
                              corner_radius=20,
                              border_color="#FB9C8D",
                            fg_color="#171717"
                              )
    name_entry.place(x=55, y=117)

    # Entry da data de nascimento
    bdt_entry = ctk.CTkEntry(main_frame,
                              width=365,
                              height=56,
                              placeholder_text="Data de nascimento",
                              font=("Arial", 16, "bold"),
                              corner_radius=20,
                              border_color="#FB9C8D",
                            fg_color="#171717"
                              )
    bdt_entry.place(x=55,y=230)

    # Opções de gênero
    gen_options = ctk.CTkComboBox(main_frame,
                                  width=365,
                                  height=56,
                                  values=["Masculino", "Feminino", "Outros"],
                                  font=("Arial", 16, "bold"),
                                  dropdown_font=("Arial", 16, "bold"),
                                  corner_radius=20,
                                  border_color="#FB9C8D",
                                fg_color="#171717",
                                button_color="#FB9C8D",
                                button_hover_color="#d47770"
                                  )
    gen_options.set("Gênero")
    gen_options.place(x=55,y=343)

    # Entry do email
    email_entry = ctk.CTkEntry(main_frame,
                              width=365,
                              height=56,
                              placeholder_text="E-mail",
                              font=("Arial", 16, "bold"),
                              corner_radius=20,
                              border_color="#FB9C8D",
                            fg_color="#171717"
                              )
    email_entry.place(x=55, y=456)

    # Entry da área
    area_entry = ctk.CTkEntry(main_frame,
                              width=365,
                              height=56,
                              placeholder_text="Área",
                              font=("Arial", 16, "bold"),
                              corner_radius=20,
                              border_color="#FB9C8D",
                            fg_color="#171717"
                              )
    area_entry.place(x=524, y=174)

    # Entry do cargo
    pos_entry = ctk.CTkEntry(main_frame,
                              width=365,
                              height=56,
                              placeholder_text="Cargo",
                              font=("Arial", 16, "bold"),
                              corner_radius=20,
                              border_color="#FB9C8D",
                            fg_color="#171717"
                              )
    pos_entry.place(x=524, y=287)

    # Entry do salário
    wag_entry = ctk.CTkEntry(main_frame,
                              width=365,
                              height=56,
                              placeholder_text="Salário",
                              font=("Arial", 16, "bold"),
                              corner_radius=20,
                              border_color="#FB9C8D",
                            fg_color="#171717"
                              )
    wag_entry.place(x=524, y=400)

    # botão de cadastrar
    reg_btn = ctk.CTkButton(main_frame,
                            width=170,
                            height=56,
                            text="Cadastrar",
                            font=("Arial", 20, "bold"),
                            corner_radius=20,
                            border_color="#FB9C8D",
                            hover_color="#155e75",
                            border_width=2,
                            fg_color="#171717",
                            command=lambda: register_checker(name_entry.get(),
                                                             bdt_entry.get(),
                                                             email_entry.get(),
                                                             area_entry.get(),
                                                             pos_entry.get(),
                                                             wag_entry.get(),
                                                             gen_options.get()
                                                             )
                            )
    reg_btn.place(x=387,y=610)

    # Delimitadores (bordas)
    img_right = ctk.CTkFrame(master,
                             width=2,
                             height=300,
                             fg_color="#171717"
                             )
    img_right.place(x=398,y=0)

    img_down = ctk.CTkFrame(master,
                             width=400,
                             height=2,
                             fg_color="#171717"
                             )
    img_down.place(x=0,y=300)

    list_top = ctk.CTkFrame(master,
                             width=400,
                             height=3,
                             fg_color="#171717"
                             )
    list_top.place(x=0,y=347)

    list_right = ctk.CTkFrame(master,
                             width=2,
                             height=420,
                             fg_color="#171717"
                             )
    list_right.place(x=400,y=347)

    list_employees(emp_list, lista_funcionarios)

