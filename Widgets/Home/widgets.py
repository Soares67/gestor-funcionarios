import customtkinter as ctk
from Icons.iconspath import REFRESH_ICON
from CTkToolTip import *
from PIL import Image
import config
import functions
import numpy as np


def home_widgets(master):

    
    if len(config.get_salaries()) == 0:
        max_salary = 0
        min_salary = 0
        qty_employees = 0
        avg_salaries = 0
    else:
        qty_employees = len(config.get_funcionarios())
        avg_salaries = np.mean(config.get_salaries()).round(2)
        max_salary = max(config.get_salaries())
        min_salary = min(config.get_salaries())
    

    # Atualiza as estatísticas
    def refresh_stats():
        global qty_employees, avg_salaries, max_salary, min_salary
        if len(config.get_salaries()) == 0:
            max_salary = 0
            min_salary = 0
            qty_employees = 0
            avg_salaries = 0
        else:
            qty_employees = len(config.get_funcionarios())
            avg_salaries = np.mean(config.get_salaries()).round(2)
            max_salary = max(config.get_salaries())
            min_salary = min(config.get_salaries())

        def update_values(values_list, texts_list):
            for i, value in enumerate(values_list):
                value.configure(text=texts_list[i])
        
        update_values([qtde_emp, val_sal_mean, max_sal_val, min_sal_val], [f"{qty_employees}", f"R$ {functions.float_to_rs(avg_salaries)}",
                                                                          f"R$ {functions.float_to_rs(max_salary)}", f"R$ {functions.float_to_rs(min_salary)}"
                                                                          ])

    # Atualiza os gráficos
    def refresh_charts():
        if len(config.get_salaries()) == 0:

            gen_label.configure(image=ctk.CTkImage(Image.open(r'Charts\nfound.png'), size=(456, 334)))
            area_label.configure(image=ctk.CTkImage(Image.open(r'Charts\nfound.png'), size=(455, 334)))
            ages_label.configure(image=ctk.CTkImage(Image.open(r'Charts\nfound1.png'), size=(910, 336)))
        else:
            
            functions.update_charts()

            gen_label.configure(image=ctk.CTkImage(Image.open(r'Charts\genders_chart.png'), size=(456, 334)))
            area_label.configure(image=ctk.CTkImage(Image.open(r'Charts\areas_chart.png'), size=(455, 334)))
            ages_label.configure(image=ctk.CTkImage(Image.open(r'Charts\ages_chart.png'), size=(910, 336)))

    def refresh_page():
        refresh_stats()
        refresh_charts()
    
    # Frame do cabeçalho
    header_frame = ctk.CTkFrame(master,
                                width=1366,
                                height=52,
                                fg_color="#0891b2",
                                border_width=3,
                                border_color="black"
                                )
    header_frame.place(x=39, y=-2)

    # Texto do cabeçalho
    lb1 = ctk.CTkLabel(header_frame,
                                    text="Página Inicial",
                                    font=("Roboto", 30, "bold"),
                                    text_color="white"
                                    )
    lb1.place(x=620,y=7)

    # Frame das estatisticas
    stat_frame = ctk.CTkFrame(master,
                          width=455,
                          height=668,
                          fg_color="#FB9C8D",
                          corner_radius=0
                          )
    stat_frame.place(x=40,y=50)

    # Título da quantidade de  funcionários
    qtde_emp_title = ctk.CTkLabel(stat_frame,
                                   text="Quantidade de Funcionários",
                                   font=("Roboto", 26, "bold"),
                    text_color="black",
    )
    qtde_emp_title.place(x=53,y=40)

    # Label da quantidade de funcionários
    qtde_emp = ctk.CTkLabel(stat_frame,
                            text=f"{qty_employees}",
                            font=("Roboto", 28, "bold"),
                            width=309,
                            height=66,
                            text_color="black",
                            fg_color="white",
                            corner_radius=20
                            )
    qtde_emp.place(x=77,y=80)

    # Título do salário médio bruto
    sal_mean_title = ctk.CTkLabel(stat_frame,
                                  text="Salário Médio Bruto",
                                  font=("Roboto", 26, "bold"),
                    text_color="black"

                                  )
    sal_mean_title.place(x=110,y=196)

    # Label do salário médio bruto
    val_sal_mean = ctk.CTkLabel(stat_frame,
                            text=f"R$ {functions.float_to_rs(avg_salaries)}",
                            font=("Roboto", 28, "bold"),
                            width=309,
                            height=66,
                            text_color="black",
                            fg_color="white",
                            corner_radius=20
                            )
    val_sal_mean.place(x=77,y=236)

    # Título do maior salário
    max_sal_title = ctk.CTkLabel(stat_frame,
                                 text="Maior Salário",
                                 font=("Roboto", 26, "bold"),
                    text_color="black"
                                 )
    max_sal_title.place(x=150,y=352)

    # Label do maior salário
    max_sal_val = ctk.CTkLabel(stat_frame,
                            text=f"R$ {functions.float_to_rs(max_salary)}",
                            font=("Roboto", 28, "bold"),
                            width=309,
                            height=66,
                            text_color="black",
                            fg_color="white",
                            corner_radius=20
                            )
    max_sal_val.place(x=77,y=392)

    # Título do menor salário
    min_sal_title = ctk.CTkLabel(stat_frame,
                    text="Menor Salário",
                    font=("Roboto", 26, "bold"),
                    text_color="black"
                    )
    min_sal_title.place(x=150,y=508)

    # Label do menor salário
    min_sal_val = ctk.CTkLabel(stat_frame,
                            text=f"R$ {functions.float_to_rs(min_salary)}",
                            font=("Roboto", 28, "bold"),
                            width=309,
                            height=66,
                            text_color="black",
                            fg_color="white",
                            corner_radius=20
                            )
    min_sal_val.place(x=77,y=548)

    #Frame do gráfico de gêneros
    gen_frame = ctk.CTkFrame(master,
                             width=456,
                             height=334,
                             fg_color="green",
                             corner_radius=0,
                             )
    gen_frame.place(x=494,y=50)

    # Gráfico dos gêneros
    gen_label = ctk.CTkLabel(gen_frame,
                             text="",
                            image=ctk.CTkImage(Image.open(r'Charts\nfound.png'), size=(456, 334))
                             )
    gen_label.place(x=0,y=0)

    #Frame do gráfico de idades
    age_frame = ctk.CTkFrame(master,
                             width=1404,
                             height=336,
                             fg_color="blue",
                             corner_radius=0
                             )
    age_frame.place(x=494,y=382)

    # Gráfico das idades
    ages_label = ctk.CTkLabel(age_frame,
                              text="",
                              image=ctk.CTkImage(Image.open(r'Charts\nfound1.png'), size=(910, 336))
                              )
    ages_label.place(x=0,y=0)

    #Frame do gráfico de áreas
    area_frame = ctk.CTkFrame(master,
                             width=455,
                             height=334,
                             fg_color="red",
                             corner_radius=0
                             )
    area_frame.place(x=949,y=50)

    # Gráfico das áreas
    area_label = ctk.CTkLabel(area_frame,
                              text="",
                              image=ctk.CTkImage(Image.open(r'Charts\nfound.png'), size=(455, 334))
                              )
    area_label.place(x=0,y=0)

    #Botão de atualizar as informações
    ref_btn = ctk.CTkButton(header_frame,
                            text="",
                            image=REFRESH_ICON,
                            command=lambda: refresh_page(),
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

    # Delimitadores

    stats_del = ctk.CTkFrame(master,
                             width=3,
                             height=668,
                             fg_color="black"
                             )
    stats_del.place(x=494,y=50)

    age_del = ctk.CTkFrame(master,
                             width=1404,
                             height=3.2,
                             fg_color="black"
                             )
    age_del.place(x=494,y=382)

    gen_del = ctk.CTkFrame(master,
                             width=3,
                             height=334,
                             fg_color="black"
                             )
    gen_del.place(x=949,y=50)