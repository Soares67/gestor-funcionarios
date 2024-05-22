import customtkinter as ctk
from Calendar.ctk_calendar_stat import CTkCalendarStat
from Icons.iconspath import SEARCH_ICON
import functions, config
import messagebox as msg


def vacation_widgets(master):
    data = {(1, 1, 1901): 10}
    
    def get_vagacations(id):
        global data
        data = functions.interval_to_sequence(config.get_vacations(id))


    def change_calendar():
        # Atualiza as informações do calendário
        try:
            id = int(id_entry.get())
        except:
            msg.showerror("Erro", "Insira um ID válido")
            return
        if not config.get_vacations(id):
            msg.showerror("Erro", "ID não encontrado.")
            return
        else:
            get_vagacations(id)
            global data
            mark_calendar.data = data
            mark_calendar.replot_current_month()


    # Registra férias no id de um funcionário
    def register():
        try:
            id = int(id_entry.get())
        except:
            msg.showwarning("Erro", "Insira um ID válido.")
            return
        
        if functions.check_date(start_date_entry.get(), alert=False):
            if functions.check_date(end_date_entry.get(), alert=False):
                start_date = start_date_entry.get()
                end_date = end_date_entry.get()

                if opts.get() != "Motivo":
                    motivo = opts.get()
                else:
                    msg.showwarning("Erro", "Insira um motivo válido.")
                    return
                
                try:
                    # Cadastrar
                    config.register_vacation(id, start_date, end_date, motivo)
                    msg.showinfo("Sucesso", "Férias registradas com sucesso.")

                    # Limpar os campos
                    id_entry.delete(0, "end")
                    start_date_entry.delete(0, "end")
                    end_date_entry.delete(0, "end")
                    opts.set("Motivo")
                except Exception as e:
                    msg.showerror("Erro", "Ocorreu um erro ao cadastrar as férias. Tente novamente.")
                    raise e
                


            else:
                msg.showwarning("Erro", "Insira uma data de término válida.")
                return
        else:
            msg.showwarning("Erro", "Insira uma data de início válida.")
            return


    # Frame do cabeçalho
    header_frame = ctk.CTkFrame(master,
                                width=1363,
                                height=53,
                                border_width=3,
                                border_color="black",
                                fg_color="#0891b2",
                                corner_radius=0
                                )
    header_frame.place(x=-5, y=-3)

    # Texto do cabeçalho
    header_text = ctk.CTkLabel(header_frame,
                               text="Férias",
                               font=("Roboto", 30, "bold"),
                               text_color="white",

                               )
    header_text.place(x=635,y=9)


    # Frame do formulário
    form_frame = ctk.CTkFrame(master,
                              width=674,
                              height=670,
                              fg_color="#0891b2",
                              corner_radius=0
                              )
    form_frame.place(x=0,y=49)

    # Texto do formulário
    header_text = ctk.CTkLabel(form_frame,
                               text="Agendar Férias",
                               font=("Roboto", 27, "bold"),
                               text_color="black",

                               )
    header_text.place(x=237,y=13)

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
    id_entry.place(x=132,y=93)

    # Botão de pesquisar
    search_btn = ctk.CTkButton(form_frame,
                               width=10,
                               height=10,
                               text="",
                               image=SEARCH_ICON,
                               corner_radius=20,
                               fg_color="#171717",
                               bg_color="#171717",
                               command=lambda: change_calendar(),
                               hover_color="#404040"
                               )
    search_btn.place(x=468,y=100)

    # Entry da data de início
    start_date_entry = ctk.CTkEntry(form_frame,
                            width=400,
                            height=55,
                            placeholder_text="Data de início",
                            corner_radius=20,
                            font=("Roboto", 16, "bold"),
                            fg_color="#171717",
                            border_color="#FB9C8D"
                            )
    start_date_entry.place(x=132,y=200)

    # Entry da data de término
    end_date_entry = ctk.CTkEntry(form_frame,
                            width=400,
                            height=55,
                            placeholder_text="Data de término",
                            corner_radius=20,
                            font=("Roboto", 16, "bold"),
                            fg_color="#171717",
                            border_color="#FB9C8D"
                            )
    end_date_entry.place(x=132,y=307)

    # Dropdown do motivo
    opts = ctk.CTkComboBox(form_frame,
                            width=400,
                            height=55,
                            corner_radius=20,
                            values=["Férias anuais",
                                    "Assuntos pessoais",
                                    "Educação ou aperfeiçoamento profissional",
                                    "Religião ou feriado religioso",
                                    "Férias antecipadas",
                                    "Reserva de férias acumuladas",
                                    "Licença médica",
                                    "Outros"
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
    opts.place(x=132,y=414)

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
                            command=lambda: register(),
                            hover_color="#404040"

                             )
    save_btn.place(x=243,y=521)



    # Frame do calendário
    cal_frame = ctk.CTkFrame(master,
                              width=677,
                              height=670,
                              fg_color="white",
                              corner_radius=0
                              )
    cal_frame.place(x=673,y=49)


    # Calendário Marcador
    mark_calendar = CTkCalendarStat(cal_frame,
                                    width=677,
                                    height=670,
                                    corner_radius=0,
                                    data=data,
                                    data_colors=("green", "red", "blue"),
                                    title_bar_button_fg_color="#FB9C8D",
                                    title_bar_button_hover_color="#d47770",
                                    )
    
    mark_calendar.place(x=0,y=0)

    # Delimitador

    del1 = ctk.CTkFrame(master,
                        width=3,
                        height=675,
                        fg_color="black"
                        )
    del1.place(x=672,y=49)