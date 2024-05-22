import customtkinter as ctk
from PIL import Image
from Icons.iconspath import SEARCH_ICON, REFRESH_ICON
import messagebox as msg
import config
import functions
from CTkToolTip import *

def overtime_widgets(master):

    if config.get_total_overtime() == 0:
        total_hours = 0
        hours_avg = 0
    else:
        total_hours = round(sum(config.get_total_overtime()), 1)  # Total de horas extras
        hours_avg = config.get_avg_overtime()  # Média de horas extras
    focus_id = None  # ID do funcionário em foco
    
    # Procura o nome do funcionálio pelo ID
    def search_employee():
        try:
            id = int(id_entry.get())
        
        except ValueError:
            id = None
            msg.showwarning("Atenção", "Insira um valor válido para o ID.")
        if id is not None:
                global focus_id
                focus_id = id
                id_entry.delete(0, "end")
                id_entry.insert(0, config.get_employee_name(id))
        else:
             pass
    
    # Atualiza as estatísticas da pagina
    def refresh_stats():
        global total_hours, hours_avg
        if config.get_total_overtime() == 0:
            total_hours = 0
            hours_avg = 0
        else:
            total_hours = round(sum(config.get_total_overtime()), 1)  # Total de horas extras
            hours_avg = config.get_avg_overtime()  # Média de horas extras

            total_lb.configure(text=f"{total_hours}")
            avg_lb.configure(text=f"{hours_avg}")
        

    # Atualiza o gráfico
    def refresh_chart():
        """Atualiza o gráfico
        """
        if config.get_total_overtime() == 0:
            chart.configure(image=ctk.CTkImage(Image.open(r'Charts\nfound4.png'), size=(460, 310)))
        else:

            functions.plotnsave_overtime()

            chart.configure(image=ctk.CTkImage(Image.open(r'Charts\overtime_chart.png'), size=(460, 310)))

    # Atualiza as informações da página
    def refresh_page():
        refresh_stats()
        refresh_chart()

    # Faz o registro de uma hora extra
    def register_overtime():
        """Valida e trata os campos de registro, inserindo os dados na tabela do banco de dados.
        """
        try:
            employee_id = int(id_entry.get())

        except ValueError:
            global focus_id

            if focus_id is not None:
                employee_id = focus_id
            else:
                msg.showerror("Erro", "Insira um ID válido.")
                return
        
        
        data_registro = date_entry.get()
        if data_registro.count("/") == 2:
            if len(data_registro.split("/")[0]) == 2:
                if len(data_registro.split("/")[1]) == 2:
                    if len(data_registro.split("/")[2]) == 4:
                        data = data_registro

                        # Validar e tratar a quantidade de horas
                        horas = qty_entry.get()
                        try:
                            if "," in horas:
                                horas = horas.replace(",", ".")
                            horas = float(horas)
                        except ValueError:
                            msg.showerror("Erro", "Insira um valor válido na quantidade de horas.")
                            return
                        
                        # Validar e tratar o motivo
                        motivo = opts.get()
                        if motivo != "Motivo":
                            motivo = motivo
                        else:
                            msg.showerror("Erro", "Insira uma opção vlaida para o motivo")
                            return
                        
                        # Registrar as horas extras
                        try:
                            config.register_overtime(employee_id, data, horas, motivo)
                            msg.showinfo("Sucesso", "As informações foram salvas com sucesso!")

                            # Limpar todos os campos
                            id_entry.delete(0, "end")
                            date_entry.delete(0, "end")
                            qty_entry.delete(0, "end")
                            opts.set("Motivo")


                        except:
                            msg.showerror("Erro", "Ocorreu um erro ao salvar as informações. Tente novamente.")

                    else:
                        msg.showerror("Erro", "Insira uma data válida, no formato DD/MM/YYYY")
                        return
                else:
                    msg.showerror("Erro", "Insira uma data válida, no formato DD/MM/YYYY")
                    return
            else:
                msg.showerror("Erro", "Insira uma data válida, no formato DD/MM/YYYY")
                return
        else:
            msg.showerror("Erro", "Insira uma data válida, no formato DD/MM/YYYY")
            return


    # Frame das estatísticas
    stats_frame = ctk.CTkFrame(master,
                               width=482,
                               height=718,
                               fg_color="#FB9C8D",
                               corner_radius=0
    )
    stats_frame.place(x=0,y=0)

    # Label do título total
    title_total_lb = ctk.CTkLabel(stats_frame,
                            text="Total de horas extras",
                            font=("Roboto", 26, "bold"),
                            text_color="black"
                            )
    title_total_lb.place(x=96,y=32)

    # Label do total
    total_lb = ctk.CTkLabel(stats_frame,
                            width=200,
                            height=57,
                            text=f"{total_hours}",
                            font=("Roboto", 28, "bold"),
                            text_color="black",
                            fg_color="white",
                            corner_radius=20
                            )
    total_lb.place(x=130,y=74)

    # Label do título da média
    title_avg_lb = ctk.CTkLabel(stats_frame,
                            text="Média por funcionário",
                            font=("Roboto", 26, "bold"),
                            text_color="black"
                            )
    title_avg_lb.place(x=95,y=190)

    # Label da média
    avg_lb = ctk.CTkLabel(stats_frame,
                            width=200,
                            height=57,
                            text=f"{hours_avg}",
                            font=("Roboto", 28, "bold"),
                            text_color="black",
                            fg_color="white",
                            corner_radius=20
                            )
    avg_lb.place(x=130,y=232)

    # Label do título do grafico
    title_chart_lb = ctk.CTkLabel(stats_frame,
                            text="Horas extras por área",
                            font=("Roboto", 26, "bold"),
                            text_color="black"
                            )
    title_chart_lb.place(x=95,y=348)

    # Frame do gráfico
    chart_frame = ctk.CTkFrame(stats_frame,
                               width=473,
                               height=323,
                               fg_color="white",
                               border_color="white",
                               border_width=3,
                               corner_radius=10
                               )
    chart_frame.place(x=5,y=390)

    # Gráfico
    chart = ctk.CTkLabel(chart_frame,
                         text="",
                         image=ctk.CTkImage(Image.open(r'Charts\nfound4.png'), size=(460, 310))
                         )
    chart.place(x=7,y=7)


    # Frame do formulário
    form_frame = ctk.CTkFrame(master,
                              width=870,
                              height=718,
                              fg_color="#0891b2",
                              corner_radius=0
    )
    form_frame.place(x=482,y=0)

    #Botão de atualizar as informações
    ref_btn = ctk.CTkButton(stats_frame,
                            text="",
                            image=REFRESH_ICON,
                            command=lambda: refresh_page(),
                            corner_radius=20,
                            width=20,
                            height=20,
                            fg_color="transparent",
                            border_color="white",
                            border_width=2,
                            hover_color="#e28c7f"
    )
    ref_tooltip = CTkToolTip(ref_btn, "Atualizar página", 0.1)
    ref_btn.place(x=420,y=5)

    # Label do cabeçalho
    header_lb = ctk.CTkLabel(form_frame,
                             text="Registrar hora extra",
                             font=("Roboto", 32, "bold"),
                             text_color="white"
                             )
    header_lb.place(x=290,y=22)

    # Entry do ID
    id_entry = ctk.CTkEntry(form_frame,
                            width=400,
                            height=55,
                            placeholder_text="ID do funcionário",
                            corner_radius=20,
                            font=("Roboto", 16, "bold"),
                            fg_color="#171717",
                            border_color="#FB9C8D"
                            )
    id_entry.place(x=245,y=104)

    # Botão de pesquisar
    search_btn = ctk.CTkButton(form_frame,
                               width=10,
                               height=10,
                               text="",
                               image=SEARCH_ICON,
                               corner_radius=20,
                               fg_color="#171717",
                               bg_color="#171717",
                               command=lambda: search_employee(),
                               hover_color="#404040"
                               )
    search_btn.place(x=583,y=112)

    # Entry da data
    date_entry = ctk.CTkEntry(form_frame,
                            width=400,
                            height=55,
                            placeholder_text="Data de registro",
                            corner_radius=20,
                            font=("Roboto", 16, "bold"),
                            fg_color="#171717",
                            border_color="#FB9C8D"
                            )
    date_entry.place(x=245,y=224)

    # Entry da quantidade
    qty_entry = ctk.CTkEntry(form_frame,
                            width=400,
                            height=55,
                            placeholder_text="Quantidade de horas",
                            corner_radius=20,
                            font=("Roboto", 16, "bold"),
                            fg_color="#171717",
                            border_color="#FB9C8D"
                            )
    qty_entry.place(x=245,y=344)

    # Dropdown do motivo
    opts = ctk.CTkComboBox(form_frame,
                            width=400,
                            height=55,
                            corner_radius=20,
                            values=["Trabalho adicional",
                                    "Projeto urgente",
                                    "Compensação",
                                    "Treinamento",
                                    "Eventos especiais",
                                    "Outros",
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
    opts.place(x=245,y=464)

    # Botão de salvar
    save_btn = ctk.CTkButton(form_frame,
                             width=150,
                             height=55,
                             corner_radius=20,
                             font=("Roboto", 16, "bold"),
                             text="Salvar",
                            fg_color="#171717",
                            border_width=2,
                            border_color="#FB9C8D",
                            command=lambda: register_overtime()

                             )
    save_btn.place(x=384,y=584)

    # Delimitadores

    del1 = ctk.CTkFrame(master,
                        width=3,
                        height=718,
                        fg_color="black"
                        )
    del1.place(x=482,y=0)