import customtkinter as ctk
from PIL import Image
from CTkToolTip import * 
from Icons.iconspath import REFRESH_ICON
import numpy as np
import config, functions

def payroll_widgets(master):

    total_payroll = sum(config.get_salaries())

    if len(config.count_vacations()) == 0:
         total_vac = 0
    else:
        avg_salaries = np.mean(config.get_salaries()).round(2)
        valor_ferias = (avg_salaries / 30) * (1 + (1/3))
        total_vac = sum(config.count_vacations()) * valor_ferias

    # Atualiza as estatísticas
    def refresh_stats():
        global total_payroll
        global total_vac
        total_payroll = sum(config.get_salaries())  # Atualizar o total
        total_payroll_field.configure(text=f"R$ {functions.float_to_rs(total_payroll)}")  # Atualizar a informação na tela

        avg_salaries = np.mean(config.get_salaries()).round(2)
        valor_ferias = (avg_salaries / 30) * (1 + (1/3))
        total_vac = sum(config.count_vacations()) * valor_ferias
        total_vac_field.configure(text=f"R$ {functions.float_to_rs(total_vac)}")

    # Atualiza os gráficos
    def refresh_charts():
        if len(config.get_salaries())  == 0:
            chart1.configure(image=ctk.CTkImage(Image.open(r'Charts\nfound2.png'), size=(690, 255)))
            chart2.configure(image=ctk.CTkImage(Image.open(r'Charts\nfound3.png'), size=(1346, 413)))
        
        else:

            functions.plotnsave_salaries()  # Atualizar o gráfico
            functions.plotnsave_salaries_id()  # Atualizar o gráfico

            chart1.configure(image=ctk.CTkImage(Image.open(r'Charts\area_salary_chart.png'), size=(690, 255)))  # Mostrar o gráfico atualizado
            chart2.configure(image=ctk.CTkImage(Image.open(r'Charts\salary_chart.png'), size=(1346, 413)))  # Mostrar o gráfico atualizado

    # Atualiza as informações da página
    def refresh():
        refresh_stats()
        refresh_charts()

    # Frame do cabeçalho
    header_frame = ctk.CTkFrame(master,
                                width=1360,
                                height=53,
                                fg_color="#0891b2",
                                corner_radius=0,
                                border_width=3,
                                border_color="black"
                                )
    header_frame.place(x=-5,y=-3)

    # Texto do cabeçalho
    lb1 = ctk.CTkLabel(header_frame,
                       text="Folha de Pagamento",
                       font=("Roboto", 30, "bold"),
                       text_color="white"
                       )
    lb1.place(x=540, y=9)

    #Botão de atualizar as informações
    ref_btn = ctk.CTkButton(header_frame,
                            text="",
                            image=REFRESH_ICON,
                            command=lambda: refresh(),
                            corner_radius=20,
                            width=20,
                            height=20,
                            fg_color="transparent",
                            border_color="white",
                            border_width=2,
                            hover_color="#155e75"
    )
    ref_tooltip = CTkToolTip(ref_btn, "Atualizar página", 0.1)
    ref_btn.place(x=1200,y=7)


    # Frame do total
    total_frame = ctk.CTkFrame(master,
                               width=336,
                               height=255,
                               fg_color="white",
                               corner_radius=0
                               )
    total_frame.place(x=0,y=50)

    # Texto do total
    lb2 = ctk.CTkLabel(total_frame,
                       text="Total Folha de Pagamento",
                       font=("Roboto", 26, "bold"),
                       text_color="black"
                       )
    lb2.place(x=2, y=19)

    # Campo do total
    total_payroll_field = ctk.CTkLabel(total_frame,
                       text=f"R$ {functions.float_to_rs(total_payroll)}",
                       font=("Roboto", 26, "bold"),
                       text_color="black",
                       width=180,
                       height=70,
                       fg_color="#bfbfbf",
                       corner_radius=20
                       )
    total_payroll_field.place(x=53, y=80)
    

    # Frame do total férias
    total1_frame = ctk.CTkFrame(master,
                               width=336,
                               height=255,
                               fg_color="white",
                               corner_radius=0
                               )
    total1_frame.place(x=335,y=50)

    # Texto do total férias
    lb3 = ctk.CTkLabel(total1_frame,
                       text="Total Férias",
                       font=("Roboto", 26, "bold"),
                       text_color="black"
                       )
    lb3.place(x=90, y=19)

    # Campo do total férias
    total_vac_field = ctk.CTkLabel(total1_frame,
                       text=f"R$ {functions.float_to_rs(total_vac)}",
                       font=("Roboto", 26, "bold"),
                       text_color="black",
                       width=180,
                       height=70,
                       fg_color="#bfbfbf",
                       corner_radius=20
                       )
    total_vac_field.place(x=63, y=80)


    # Frame do total por área
    total2_frame = ctk.CTkFrame(master,
                               width=690,
                               height=255,
                               fg_color="pink",
                               corner_radius=0
                               )
    total2_frame.place(x=672,y=50)

    chart1 = ctk.CTkLabel(total2_frame,
                         text="",
                         image=ctk.CTkImage(Image.open(r'Charts\nfound2.png'), size=(690, 255))
                         )
    chart1.place(x=0,y=0)


    # Frame do salário bruto por funcionário
    total3_frame = ctk.CTkFrame(master,
                               width=1360,
                               height=413,
                               fg_color="white",
                               corner_radius=0,
                               )
    total3_frame.place(x=0,y=305)

    # Gráfico
    chart2 = ctk.CTkLabel(total3_frame,
                         text="",
                         image=ctk.CTkImage(Image.open(r'Charts\nfound3.png'), size=(1346, 413))
                         )
    chart2.place(x=0,y=0)

    
    # Delimitadores

    del1 = ctk.CTkFrame(master,
                        width=3,
                        height=255,
                        fg_color="black"
                        )
    del1.place(x=335,y=50)

    del2 = ctk.CTkFrame(master,
                        width=3,
                        height=255,
                        fg_color="black"
                        )
    del2.place(x=670,y=50)

    del3 = ctk.CTkFrame(master,
                        width=1360,
                        height=3,
                        fg_color="black"
                        )
    del3.place(x=0,y=305)

