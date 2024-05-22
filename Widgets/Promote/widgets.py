import customtkinter as ctk
import private
from Icons.iconspath import PROMOTED_ICON, FIRED_ICON
import config
import functions
import messagebox as msg

def promote_widgets(master):

    # Insere o resultado da busca no campo de resultado
    def insert_text():
        if functions.check_field(searcher_entry.get(), 1):
            key = searcher_entry.get()

            try:
                data = config.get_employee_info(key)
                res = f"""
        Nome: {data[1]}

        ID: {data[0]}
                            
        Data de nascimento: {data[2]}
                            
        Email: {data[4]}
                            
        Área: {data[5]}
                            
        Cargo: {data[6]}
                            
        Salário: R$ {functions.float_to_rs(data[7])}
                            
        Data de admissão: {data[8]}
                            
        Status de emprego: {data[9]}
        """
                res_txb.delete("0.0", "end")
                res_txb.insert(0.0, res)

            except IndexError:
                msg.showerror("Erro", "Funcionário não encontrado. Verifique a chave de busca e tente novamente.")
        else:
            msg.showwarning("Atenção", "Insira uma chave de busca (ID ou Email)")

    # Função que configura os botôes das abas
    def configure_seg_button(buttons: dict):
        for item in buttons:
            buttons[item].configure(width=50)  # Aumenta a largura
            buttons[item].configure(height=40)  # Aumenta a altura
            buttons[item].configure(font=("Roboto", 15, "bold"))  # Muda a fonte e o tamanho do texto
            buttons[item].configure(border_width=1)  # Adiciona uma borda
            buttons[item].configure(border_color="white")  # Muda a cor da borda
            buttons[item].configure(text_color="white")  # Muda a cor do texto

    # Remove o texto guia
    def remove_placeholder(event):
        if obs.get("0.0", "end") == "Observações / Comentários\n":
            obs.delete("0.0", "end")

    # Adiciona o texto guia
    def place_placeholder(event):
        if len(obs.get("0.0", "end")) < 2:
            obs.insert("0.0", "Observações / Comentários")

    # Demite um funcionário
    def onclick_fire():
        id = searcher_entry.get()
        try:
            id = int(id)
            if opts2.get() != "Motivo":
                if obs.get("0.0", "end") == "Observações / Comentários\n":
                    obs_res = None
                else:
                    obs_res = obs.get("0.0", "end")
                if msg.askyesnocancel("ATENÇÃO", f"""O funcionário {config.get_employee_info(id)[1]} será demitido.
Motivo: {opts2.get()}
Justificativa: {obs_res}

Você confirma essa ação?"""):
                    if config.fire_employee(id, opts2.get(), obs_res):
                        msg.showinfo("Sucesso", "O funcionário foi demitido com sucesso")
                        opts2.set("Motivo")
                        obs.delete("0.0", "end")
                        obs.insert("0.0", "Observações / Comentários")
                    else:
                        msg.showwarning("Erro", "Ocorreu um erro ao demitir o funcionário")
                        opts2.set("Motivo")
                        obs.delete("0.0", "end")
                        obs.insert("0.0", "Observações / Comentários")
                else:
                    opts2.set("Motivo")
                    obs.delete("0.0", "end")
                    obs.insert("0.0", "Observações / Comentários")
                    pass
                    
            else:
                msg.showwarning("Atenção", "Escolha um motivo válido")

        except ValueError:
            msg.showwarning("Erro", "Insira um valor válido no campo de busca de ID")

    # Promove um funcionário
    def onclick_promote():
        id = searcher_entry.get()
        try:
            id = int(id)
            motivo = opts.get()
            novo_salario = float(new_sal_entry.get())
            if len(new_pos_entry.get()) > 1:
                if len(new_sal_entry.get()) >= 4:
                    if motivo != "Motivo":
                        if msg.askyesnocancel("Atenção", f"""O funcionário {config.get_employee_info(id)[1]} será promovido com as seguintes informações:
                                                
Novo cargo: {new_pos_entry.get()}
Novo salário: R$ {functions.float_to_rs(novo_salario)}
Justificativa: {motivo}

Você confirma as informações?"""):
                            if config.promote_employee(id,
                                                   config.get_employee_info(id)[6],
                                                   new_pos_entry.get(),
                                                   motivo,
                                                   config.get_employee_info(id)[7],
                                                   novo_salario
                                                   ):
                                msg.showinfo("Sucesso", "O funcionário foi promovido com sucesso.")
                            else:
                                msg.showerror("Erro", "Ocorreu um erro ao promover o funcionário. Verifique as informações e tente novamente.")
                        else:
                            pass
                    else:
                        msg.showwarning("Atenção", "Insira um motivo válido.")
                else:
                    msg.showwarning("Atenção", "Preencha corretamente o campo do novo salário.")
            else:
                msg.showwarning("Atenção", "Preencha corretamente o campo do novo cargo.")
        except:
            msg.showerror("Erro", "Verifique as informações e tente novamente.")
                                
    # Frame do cabeçalho
    header_frame = ctk.CTkFrame(master,
                                width=1356,
                                height=52,
                                fg_color="#0891b2",
                                border_width=3,
                                border_color="black"
                                )
    header_frame.place(x=-3,y=-2)

    # Texto do cabeçalho
    header_text = ctk.CTkLabel(header_frame,
                               text="Promover / Demitir Funcionário",
                               font=("Roboto", 30, "bold"),
                               text_color="white"
                               )
    header_text.place(x=474,y=9)

    # Frame do buscador
    searcher_frame = ctk.CTkFrame(master,
                                  width=674,
                                  height=668,
                                  fg_color="#0891b2",
                                  corner_radius=0
                                  )
    searcher_frame.place(x=0,y=50)
    
    # Texto do buscador
    lb1 = ctk.CTkLabel(searcher_frame,
                       text="Buscar Funcionário",
                       font=("Roboto", 30, "bold"),
                       text_color="white",
                       )
    lb1.place(x=195,y=35)

    # Entry do buscador
    searcher_entry = ctk.CTkEntry(searcher_frame,
                                  width=432,
                                  height=60,
                                  placeholder_text="ID",
                                  corner_radius=20,
                                  font=("Arial", 16, "bold"),
                                  border_color="#FB9C8D",
                                  fg_color="#171717"
                                  )
    searcher_entry.place(x=119,y=90)
    searcher_entry.bind("<Return>", lambda event: insert_text())

    # botão de buscar
    search_btn = ctk.CTkButton(searcher_frame,
                               width=150,
                               height=50,
                               text="Buscar",
                               font=("Arial", 16, "bold"),
                               corner_radius=20,
                               border_width=2,
                               border_color="#FB9C8D",
                               command=lambda: insert_text(),
                               fg_color="#171717",
                               text_color="white"
                               )
    search_btn.place(x=243,y=187)

    # TextBox onde é exibido o resultado da busca
    res_txb = ctk.CTkTextbox(searcher_frame,
                             width=680,
                             height=400,
                             activate_scrollbars=False,
                             font=("Arial", 18, "bold"),
                             text_color="black",
                             fg_color="#e4e4e7",
                             )
    res_txb.place(x=0,y=270)

    # Frame das abas de ações
    tabs_frame = ctk.CTkFrame(master,
                                  width=674,
                                  height=669,
                                  fg_color="#0891b2",
                                  corner_radius=0
                                  )
    tabs_frame.place(x=674,y=50)

    # Abas de opções
    tabs = ctk.CTkTabview(tabs_frame,
                          width=674,
                          height=673,
                          fg_color="#0891b2",
                        segmented_button_fg_color="#0891b2",
                        segmented_button_selected_hover_color="#454545",
                        segmented_button_unselected_color="#171717",
                        segmented_button_selected_color="#5d5d5d",
                        segmented_button_unselected_hover_color="#454545"
                          )
    tabs.place(x=0,y=0)
    
    # Abas
    tabs.add("Promover")
    tabs.add("Demitir")
    configure_seg_button(tabs._segmented_button._buttons_dict)


    # Frame da imagem da aba promover
    img_promote_frame = ctk.CTkFrame(tabs.tab("Promover"),
                                     width=342,
                                     height=342,
                                     fg_color="red"
                                     )
    img_promote_frame.place(x=0,y=10)

    # Imagem
    img_promoted = ctk.CTkLabel(tabs.tab("Promover"),
                                text="",
                                image=PROMOTED_ICON
                                )
    img_promoted.place(x=0,y=10)

    # Entry do novo cargo
    new_pos_entry = ctk.CTkEntry(tabs.tab("Promover"),
                                 width=280,
                                 height=50,
                                 placeholder_text="Novo cargo",
                                 corner_radius=20,
                                 font=("Roboto", 16, "bold"),
                                 fg_color="#171717",
                                 border_color="#FB9C8D"
                                 )
    new_pos_entry.place(x=364,y=39)

    # Entry do novo salário
    new_sal_entry = ctk.CTkEntry(tabs.tab("Promover"),
                                 width=280,
                                 height=50,
                                 placeholder_text="Novo salário",
                                 corner_radius=20,
                                 font=("Roboto", 16, "bold"),
                                 fg_color="#171717",
                                 border_color="#FB9C8D"
                                 )
    new_sal_entry.place(x=364,y=163)

    # Opções de motivo
    opts = ctk.CTkComboBox(tabs.tab("Promover"),
                            width=280,
                            height=50,
                            corner_radius=20,
                            values=["Desempenho excepcional",
                                    "Conclusão de treinamento ou certificação",
                                    "Tempo de serviço",
                                    "Aquisição de novas habilidades",
                                    "Liderança e iniciativa",
                                    "Excelência no atendimento ao cliente",
                                    ],
                            font=("Roboto", 16, "bold"),
                            dropdown_font=("Roboto", 16, "bold"),
                            border_color="#FB9C8D",
                            dropdown_text_color="white",
                            dropdown_fg_color="#171717",
                            fg_color="#171717",
                            button_color="#FB9C8D",
                            button_hover_color="#d47770"
                           )
    opts.set("Motivo")
    opts.place(x=364,y=288)

    # Botão de salvar
    save_btn = ctk.CTkButton(tabs.tab("Promover"),
                             width=150,
                             height=50,
                             corner_radius=20,
                             font=("Roboto", 16, "bold"),
                             text="Salvar",
                            fg_color="#171717",
                            border_width=2,
                            border_color="#FB9C8D",
                            command=lambda: onclick_promote()
                             )
    save_btn.place(x=288,y=465)


    # Frame da imagem da aba demitir
    img_fire_frame = ctk.CTkFrame(tabs.tab("Demitir"),
                                     width=342,
                                     height=342,
                                     fg_color="red"
                                     )
    img_fire_frame.place(x=0,y=10)

    # Imagem
    fired_img = ctk.CTkLabel(tabs.tab("Demitir"),
                             text="",
                             image=FIRED_ICON
                             )
    fired_img.place(x=0,y=10)

    # Opções de motivo
    opts2 = ctk.CTkComboBox(tabs.tab("Demitir"),
                            width=280,
                            height=50,
                            corner_radius=20,
                            values=["Pedido de demissão voluntária",
                                    "Desempenho insatisfatório",
                                    "Violação das políticas da empresa",
                                    "Abandono de emprego",
                                    "Conclusão de contrato ou projeto",
                                    "Redução de quadro de funcionários",
                                    "Má conduta",
                                    "Aposentadoria",
                                    "Incompatibilidade com a cultura da empresa",
                                    "Razões pessoais",
                                    "Outros (especifique)"
                                    ],
                            font=("Roboto", 16, "bold"),
                            dropdown_font=("Roboto", 16, "bold"),
                            border_width=2,
                            border_color="#FB9C8D",
                            dropdown_text_color="white",
                            dropdown_fg_color="#171717",
                            fg_color="#171717",
                            button_color="#FB9C8D",
                            button_hover_color="#d47770"
                           )
    opts2.set("Motivo")
    opts2.place(x=364,y=43)

    # Campo de observações e comentários extras
    obs = ctk.CTkTextbox(tabs.tab("Demitir"),
                         width=280,
                         height=215,
                         font=("Roboto", 16, "bold"),
                         border_width=2,
                         border_color="#FB9C8D"
                         )
    obs.insert("0.0", "Observações / Comentários")
    obs.place(x=364,y=139)
    obs.bind("<FocusIn>", remove_placeholder)
    obs.bind("<FocusOut>", place_placeholder)

    # Botão de salvar
    save_btn2 = ctk.CTkButton(tabs.tab("Demitir"),
                             width=150,
                             height=50,
                             corner_radius=20,
                             font=("Roboto", 16, "bold"),
                             text="Salvar",
                            fg_color="#171717",
                            border_width=2,
                            border_color="#FB9C8D",
                            command=lambda: onclick_fire()

                             )
    save_btn2.place(x=288,y=465)


    # Delimitadores (Bordas)
    center = ctk.CTkFrame(master,
                              width=6,
                              height=668,
                              fg_color="black"
                              )
    center.place(x=674,y=50)

    res_up = ctk.CTkFrame(master,
                              width=677,
                              height=2,
                              fg_color="black"
                              )
    res_up.place(x=0,y=320)

    promoted_up = ctk.CTkFrame(master,
                               width=344,
                               height=2,
                               fg_color="black"
                               )
    promoted_up.place(x=680,y=113)

    promoted_left = ctk.CTkFrame(master,
                               width=2,
                               height=348,
                               fg_color="black"
                               )
    promoted_left.place(x=1022,y=113)

    promoted_down = ctk.CTkFrame(master,
                               width=344,
                               height=2,
                               fg_color="black"
                               )
    promoted_down.place(x=680,y=459)