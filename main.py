import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import Icons.iconspath as iconspath
import config
from CTkToolTip import *
import functions
from Widgets.Home.widgets import home_widgets
from Widgets.Register.widgets import register_widgets
from Widgets.Promote.widgets import promote_widgets
from Widgets.Overtime.widgets import overtime_widgets
from Widgets.Payroll.widgets import payroll_widgets
from Widgets.Vacation.widgets import vacation_widgets

#Classe que controla o status do admin
class AdminStatus:
    def __init__(self):
        self.logged = False

    def login(self):
        self.logged = True

    def logout(self):
        self.logged = False

    def is_logged(self):
        return self.logged


#Janela de Login ADM
class AuthAdmin(tk.Toplevel):
    def __init__(self, parent, admin_status):
        super().__init__(parent)
        self.admin_status = admin_status
        self.geometry("300x300")
        self.title("Admin Login")
        self.iconbitmap(r'Icons\imgs\icons8-admin-90.ico')
        self.configure(bg='#0891b2')
        self.resizable(False, False)
        self.senha_oculta = True

        self.lb = ctk.CTkLabel(self,
                               text="Login",
                               text_color="black",
                               font=("Roboto", 29, "bold")
                               )
        self.lb.place(x=112, y=10)

        #Entry do usuário
        self.user_entry = ctk.CTkEntry(self,
                                   width=200,
                                   height=40,
                                   placeholder_text="E-mail ou Usuário",
                                   
                                   font=("Roboto", 14, "bold"),
                                    border_width=2,
                                    border_color='#FB9C8D',
                                    corner_radius=20,
                                    fg_color="#171717",
                                    )
        self.user_entry.place(x=50, y=65)

        #Entry da senha
        self.senha_entry = ctk.CTkEntry(self,
                                width=200,
                                height=40,
                                font=("Roboto", 14, "bold"),
                                
                                placeholder_text="Senha",
                                border_width=2,
                                border_color='#FB9C8D',
                                corner_radius=20,
                                fg_color="#171717",
                                show="*"
                                )
        self.senha_entry.place(x=50, y=130)

        #Botão de recuperar senha
        self.link_recover = ctk.CTkButton(self,
                                    text="Esqueceu sua senha?",
                                    font=("Roboto", 13, "bold"),
                                    fg_color="transparent",
                                    width=8,
                                    height=8,
                                    hover_color="#155e75",
                                    text_color="white",
                                    corner_radius=20,
                                    command=lambda: self.open_recover()
                                    )
        self.link_recover.place(x=55,y=180)

        #Botão de fazer login
        self.login_btn = ctk.CTkButton(self,
                                width=70,
                                height=40,
                                text="Login",
                                font=("Roboto", 15, "bold"),
                                command=lambda: self.autenticacao(),
                                border_width=2,
                                corner_radius=20,
                                fg_color="#171717",
                                border_color='#FB9C8D',
                                hover_color='#454545',
                                   )
        self.login_btn.place(x=110, y=240)

        #Botão de mostrar a senha   (São dois botões pois altera o ícone quando pressionado)
        self.show_pass_btn = ctk.CTkButton(self,
                                           text="",
                                           image=iconspath.CLOSED_EYE_ICON,
                                           width=10,
                                           height=10,
                                           corner_radius=50,
                                           fg_color="#171717",
                                           bg_color="#171717",
                                           hover_color="#454545",
                                           command=self.show_hide
                                           )
        self.show_pass_btn.place(x=210, y=139)

        #Botão de ocultar a senha
        self.hide_pass_btn = ctk.CTkButton(self,
                                            text="",
                                            image=iconspath.EYE_ICON,
                                            width=10,
                                            height=10,
                                            corner_radius=50,
                                            fg_color="#171717",
                                            bg_color="#171717",
                                            hover_color="#454545",
                                            command=self.show_hide
                                           )
        self.hide_pass_btn.place(x=210, y=139)

    # oculta/exibe a senha e altera os ícones
    def show_hide(self):
        if self.senha_oculta:
            self.senha_entry.configure(show="")
            self.hide_pass_btn.place_forget()
            self.show_pass_btn.place(x=210, y=139)
            self.senha_oculta = False
        else:
            self.senha_entry.configure(show="*")
            self.show_pass_btn.place_forget()
            self.hide_pass_btn.place(x=210, y=139)
            self.senha_oculta = True
    
    #Autentica os admins
    def autenticacao(self):
        if len(self.user_entry.get()) >= 5:
            if len(self.senha_entry.get()) >= 8:
                if config.auth_admin(self.user_entry.get().lower(), self.senha_entry.get()):
                    messagebox.showinfo("hey", "Admin logado com sucesso")
                    self.admin_status.login()
                    config.update_last_access(self.user_entry.get().lower(), self.senha_entry.get())
                    self.destroy()
                else:
                    messagebox.showerror("Erro", "Login ou senha incorretos")
            else:
                messagebox.showwarning("Atenção", "Senha inválida")
        else:
            messagebox.showwarning("Atenção", "E-mail ou Usuário inválido")

    #Abre a janela de recuperação de senha
    def open_recover(self):
        recover_edge = RecoverEdge(self)
        recover_edge.grab_set()

#Janela para remover um administrador
class DeleteAdmin(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("384x410")
        self.iconbitmap(r'Icons\imgs\icons8-admin-90.ico')
        self.title("Deletar Admin")
        self.configure(bg='#0891b2')
        self.resizable(False, False)
    
        self.lb = ctk.CTkLabel(self,
                    text="Deletar Administrador",
                    text_color="black",
                    fg_color="transparent",
                    font=("Roboto", 23, "bold"),
                    
                    )
        self.lb.place(x=90,y=10)

        self.user_entry = ctk.CTkEntry(self,
                            width=176,
                            height=40,
                            corner_radius=20,
                            border_width=2,
                            font=("Roboto", 15, "bold"),
                            border_color='#FB9C8D',
                            fg_color="#171717",
                            text_color="white",
                            
                            placeholder_text="Usuário",
                            )
        self.user_entry.place(x=8,y=70)

        self.email_entry = ctk.CTkEntry(self,
                            width=176,
                            height=40,
                            corner_radius=20,
                            border_width=2,
                            font=("Roboto", 15, "bold"),
                            border_color='#FB9C8D',
                            fg_color="#171717",
                            text_color="white",
                            
                            placeholder_text="E-mail",
                            )
        self.email_entry.place(x=200,y=70)

        self.search_btn = ctk.CTkButton(self,
                            width=30,
                            height=40,
                            text="Buscar",
                            command=lambda: self.insert_info(self.user_entry.get().lower(),
                                                             self.email_entry.get().lower(),
                                                             self.info_txb
                                                             ),
                            border_width=2,
                            border_color='#FB9C8D',
                            corner_radius=20,
                            font=("Roboto", 16, "bold"),
                            fg_color='#171717',
                            hover_color='#454545',
                            anchor="center",
                            )
        self.search_btn.place(x=145,y=140)

        self.info_txb = ctk.CTkTextbox(self,
                                width=384,
                                height=130,
                                corner_radius=15,
                                border_width=1,
                                border_color='#FB9C8D',
                                text_color="white",
                                fg_color="#171717",
                                font=("Roboto", 17, "bold"),
                                activate_scrollbars=False,
                                wrap="none",
                                )
        self.info_txb.place(x=0,y=200)

        self.delete_btn = ctk.CTkButton(self,
                            width=30,
                            height=40,
                            text="Deletar",
                            command=lambda: self.delete_admin(self.user_entry.get().lower(),
                                                              self.email_entry.get().lower()
                                                              ),
                            border_width=2,
                            border_color="#dc2626",
                            corner_radius=20,
                            font=("Roboto", 16, "bold"),
                            fg_color='#171717',
                            text_color='#dc2626',
                            hover_color='#454545',
                            anchor="center",
                            )
        self.delete_btn.place(x=147,y=352)

    #Insere as informações do admin no textbox
    def insert_info(self, user, email, where):
        if config.verify_user(email, user):
            texto = config.get_admin_info(user, email)
            where.delete("0.0", "end")
            where.insert("0.0", texto)
        else:
            messagebox.showerror("Erro", "Dados inválidos")
    
    #Deleta o administrador
    def delete_admin(self, user, email):
        if messagebox.askyesno("Atenção", "Deseja realmente excluir esse administrador? Essa ação não poderá ser desfeita."):
            if config.delete_admin(user, email):
                messagebox.showinfo("Atenção", "Administrador exluído com sucesso.")
                self.destroy()
            else:
                if messagebox.askretrycancel("Atenção", "Ocorreu um erro ao excluir esse administrador. Gostaria de tentar novamente?"):
                    pass
                else:
                    self.destroy()
        else:
            pass

#Janela de recuperação de senha (Enviar o código)
class RecoverEdge(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("300x280")
        self.iconbitmap(r'Icons\imgs\icons8-admin-90.ico')
        self.title("Recuperar senha")
        self.configure(bg='#0891b2')
        self.resizable(False, False)
        self.senha_oculta = True
        self.c_senha_oculta = True
        self.tentativas = 0


        self.frame1 = ctk.CTkFrame(self,
                                   width=300,
                                   height=280,
                                   fg_color="#0891b2",

                                   )
        self.frame1.place(x=0,y=0)

        self.lb = ctk.CTkLabel(self.frame1,
                               text="Recuperar senha",
                               text_color="black",
                               font=("Roboto", 25, "bold")
                               )
        self.lb.place(x=52, y=10)

        #Entry do E-mail
        self.email_entry = ctk.CTkEntry(self.frame1,
                                   width=200,
                                   height=40,
                                   placeholder_text="E-mail",
                                   
                                   font=("Roboto", 14, "bold"),
                                    border_width=2,
                                    border_color='#FB9C8D',
                                    corner_radius=20,
                                    fg_color="#171717",
                                    )
        self.email_entry.place(x=50, y=65)

        #Entry do usuário
        self.user_entry = ctk.CTkEntry(self.frame1,
                                width=200,
                                height=40,
                                font=("Roboto", 14, "bold"),
                                
                                placeholder_text="Usuário",
                                border_width=2,
                                border_color='#FB9C8D',
                                corner_radius=20,
                                fg_color="#171717",
                                )
        self.user_entry.place(x=50, y=130)

        #Botão de enviar o código
        self.send_btn = ctk.CTkButton(self.frame1,
                                width=70,
                                height=40,
                                text="Enviar",
                                font=("Roboto", 15, "bold"),
                                command=lambda: self.open_check(self.email_entry.get().lower(), self.user_entry.get().lower()),
                                border_width=2,
                                corner_radius=20,
                                fg_color="#171717",
                                border_color='#FB9C8D',
                                hover_color='#454545',
                                   )
        self.send_btn.place(x=109, y=220)

        self.frame2 = ctk.CTkFrame(self,
                                   width=0,
                                   height=200,
                                   fg_color="#0891b2",

                                   )
        self.frame2.place(x=0,y=0)

        self.lb2 = ctk.CTkLabel(self.frame2,
                text="Verificar Código",
                text_color="black",
                font=("Roboto", 25, "bold")
                                )
        self.lb2.place(x=55, y=10)

        #Entry do código de confirmação
        self.code_entry = ctk.CTkEntry(self.frame2,
                        width=200,
                        height=40,
                        placeholder_text="Código recebido",
                        
                        font=("Roboto", 14, "bold"),
                        border_width=2,
                        border_color='#FB9C8D',
                        corner_radius=20,
                        fg_color="#171717",
                          )
        self.code_entry.place(x=50, y=65)

        #Botão de verificação do código
        self.check_btn = ctk.CTkButton(self.frame2,
                        width=70,
                        height=40,
                        text="Verificar",
                        font=("Roboto", 15, "bold"),
                        command=lambda: self.verify(self.email_entry.get().lower(),
                                                    self.user_entry.get().lower(),
                                                    self.code_entry.get().upper()),
                        border_width=2,
                        corner_radius=20,
                        fg_color="#171717",
                        border_color='#FB9C8D',
                        hover_color='#454545',
                          )
        self.check_btn.place(x=102, y=140)

        self.frame3 = ctk.CTkFrame(self,
                                   width=0,
                                   height=300,
                                   fg_color="#0891b2",
        )
        self.frame3.place(x=0,y=0)

        self.lb3 = ctk.CTkLabel(self.frame3,
                text="Redefinir Senha",
                text_color="black",
                font=("Roboto", 25, "bold")
                                )
        self.lb3.place(x=46, y=10)

        #Entry da nova senha
        self.senha_entry = ctk.CTkEntry(self.frame3,
                                width=176,
                                height=40,
                                corner_radius=20,
                                border_width=2,
                                border_color='#FB9C8D',
                                font=("Roboto", 15, "bold"),
                                fg_color="#171717",
                                text_color="white",
                                
                                placeholder_text="Nova Senha",
                                show="*"
                                )
        self.senha_entry.place(x=50, y=65)

        #Entry de confirmação da nova senha
        self.c_senha_entry = ctk.CTkEntry(self.frame3,
                                width=176,
                                height=40,
                                corner_radius=20,
                                border_width=2,
                                border_color='#FB9C8D',
                                font=("Roboto", 13, "bold"),
                                fg_color="#171717",
                                text_color="white",
                                
                                placeholder_text="Repetir Senha",
                                show="*"
                                )
        self.c_senha_entry.place(x=50, y=130)

        self.show_btn1 = ctk.CTkButton(self.frame3,
                                            text="",
                                            image=iconspath.CLOSED_EYE_ICON,
                                            width=10,
                                            height=10,
                                            corner_radius=50,
                                            fg_color="#171717",
                                            bg_color="#171717",
                                            hover_color="#454545",
                                            command=lambda: self.show_hide_senha(),
                                           )
        self.show_btn1.place(x=185,y=74)

        #Botão de ocultar a senha do entry da senha
        self.hide_btn1 = ctk.CTkButton(self.frame3,
                                            text="",
                                            image=iconspath.EYE_ICON,
                                            width=10,
                                            height=10,
                                            corner_radius=50,
                                            fg_color="#171717",
                                            bg_color="#171717",
                                            hover_color="#454545",
                                            command=lambda: self.show_hide_senha(),
                                            )
        self.hide_btn1.place(x=185,y=74)

        #Botão de exibir a senha do entry de confirmação de senha
        self.show_btn2 = ctk.CTkButton(self.frame3,
                                            text="",
                                            image=iconspath.CLOSED_EYE_ICON,
                                            width=10,
                                            height=10,
                                            corner_radius=50,
                                            fg_color="#171717",
                                            bg_color="#171717",
                                            hover_color="#454545",
                                            command=lambda: self.show_hide_c_senha(),                                            
                                            )
        self.show_btn2.place(x=185,y=139)

        #Botão de ocultar a senha do entry de confirmação de senha
        self.hide_btn2 = ctk.CTkButton(self.frame3,
                                            text="",
                                            image=iconspath.EYE_ICON,
                                            width=10,
                                            height=10,
                                            corner_radius=50,
                                            fg_color="#171717",
                                            bg_color="#171717",
                                            hover_color="#454545",
                                            command=lambda: self.show_hide_c_senha(),                                            
                                            )
        self.hide_btn2.place(x=185,y=139)

        #Botão de redefinir a senha
        self.red_btn = ctk.CTkButton(self.frame3,
                        width=70,
                        height=40,
                        text="Redefinir",
                        font=("Roboto", 15, "bold"),
                        command=lambda: self.redefinir(self.email_entry.get().lower(),
                                                       self.user_entry.get().lower(),
                                                       self.senha_entry.get(),
                                                       self.c_senha_entry.get(),
                                                       ),
                        border_width=2,
                        corner_radius=20,
                        fg_color="#171717",
                        border_color='#FB9C8D',
                        hover_color='#454545',
                          )
        self.red_btn.place(x=90, y=210)


    #Exibe/Esconde a senha do entry da senha
    def show_hide_senha(self):
        if self.senha_oculta:
            self.senha_entry.configure(show="")
            self.hide_btn1.place_forget()
            self.show_btn1.place(x=185,y=74)
            self.senha_oculta = False
        else:
            self.senha_entry.configure(show="*")
            self.show_btn1.place_forget()
            self.hide_btn1.place(x=185,y=74)
            self.senha_oculta = True

    #Exibe/Esconde a senha do entry de confirmação de senha
    def show_hide_c_senha(self):
        if self.c_senha_oculta:
            self.c_senha_entry.configure(show="")
            self.hide_btn2.place_forget()
            self.show_btn2.place(x=185,y=139)
            self.c_senha_oculta = False
        else:
            self.c_senha_entry.configure(show="*")
            self.show_btn2.place_forget()
            self.hide_btn2.place(x=185,y=139)
            self.c_senha_oculta = True

    #Envia o código de recuperação e abre a janela de checagem
    def open_check(self, email, user):
        if config.verify_email(email):
            if config.verify_user(email, user):
                config.recover_pass(email, user)
                messagebox.showinfo("Atenção", "Um código de verificação foi enviado para o e-mail inserido.")
                self.frame1.configure(width=0)
                self.frame2.configure(width=300)
                self.geometry("300x200")
            else:
                messagebox.showerror("Erro", "O usuário não corresponde ao e-mail inserido.")
        else:
            messagebox.showerror("Erro", "E-mail não identificado.")

    #Verifica se o código inserido está correto, e abre a janela de redefinição
    def verify(self, email, user, code_entry):
        if self.tentativas < 3:
            if config.verify_code(email, user, code_entry):
                messagebox.showinfo("Atenção", "Código confirmado com sucesso")
                config.del_code(email, user)
                self.geometry("275x270")
                self.frame2.configure(width=0)
                self.frame3.configure(width=300)
            else:
                messagebox.showerror("Erro", "O código inserido não corresponde ao código enviado por e-mail.")
                self.tentativas += 1
        else:
            messagebox.showerror("Erro", "Muitas tentativas de redefinição de senha")
            self.destroy()
            self.tentativas = 0

    #Redefine a senha
    def redefinir(self, email, user, senha1, senha2):
        if functions.check_req(senha1, senha2):
            if functions.check(senha1, senha2):
                nova_senha = senha2
                if config.update_pass(email, user, nova_senha):
                    messagebox.showinfo("Atenção", "Senha redefinida com sucesso.")
                    self.destroy()
                else:
                    messagebox.showerror("Erro", "Ocorreu um erro ao redefinir sua senha. Tente novamente.")
            else:
                messagebox.showwarning("Atenção", "As senhas não se coincidem.")
        else:
            messagebox.showwarning("Atenção", "As senhas devem ter no mínimo 8 caracteres.")
                
#Janela de funções ADM
class ADM(tk.Toplevel):
    def __init__(self, parent, admin_status):
        super().__init__(parent)
        self.admin_status = admin_status
        self.title("Administrador")
        self.geometry("577x400")
        self.iconbitmap(r'Icons\imgs\icons8-admin-90.ico')
        self.resizable(False, False)
        self.configure(bg="#0891b2")
        self.senha_oculta = True
        self.c_senha_oculta = True

        #Texto maior
        self.adm_lb = ctk.CTkLabel(self,
                      text="Administrador",
                      font=("Roboto", 27, "bold"),
                      text_color="black",
                      anchor="center",
                      )
        self.adm_lb.place(x=211, y=6)

        # Texto menor
        self.cad_lb = ctk.CTkLabel(self,
                            text="Cadastrar ADM",
                            font=("Roboto", 17, "bold"),
                            text_color="black",
                            anchor="center",
                            )
        self.cad_lb.place(x=230, y=85)

        #Entry do nome
        self.nome_entry = ctk.CTkEntry(self,
                                width=176,
                                height=40,
                                corner_radius=20,
                                border_width=2,
                                border_color='#FB9C8D',
                                font=("Roboto", 15, "bold"),
                                fg_color="#171717",
                                text_color="white",
                                
                                placeholder_text="Nome",
                                )
        self.nome_entry.place(x=4,y=130)

        #Entry do usuário
        self.user_entry = ctk.CTkEntry(self,
                                width=176,
                                height=40,
                                corner_radius=20,
                                border_width=2,
                                font=("Roboto", 15, "bold"),
                                border_color='#FB9C8D',
                                fg_color="#171717",
                                text_color="white",
                                
                                placeholder_text="Usuário",
                                )
        self.user_entry.place(x=202,y=130)

        #Entry do E-mail
        self.email_entry = ctk.CTkEntry(self,
                                width=176,
                                height=40,
                                corner_radius=20,
                                border_width=2,
                                border_color='#FB9C8D',
                                font=("Roboto", 15, "bold"),
                                fg_color="#171717",
                                text_color="white",
                                
                                placeholder_text="E-mail",
                                )
        self.email_entry.place(x=397,y=130)

        #Entry da senha
        self.senha_entry = ctk.CTkEntry(self,
                                width=176,
                                height=40,
                                corner_radius=20,
                                border_width=2,
                                border_color='#FB9C8D',
                                font=("Roboto", 15, "bold"),
                                fg_color="#171717",
                                text_color="white",
                                
                                placeholder_text="Senha",
                                show="*"
                                )
        self.senha_entry.place(x=99,y=215)

        #Entry de confirmação da senha
        self.c_senha_entry = ctk.CTkEntry(self,
                                width=176,
                                height=40,
                                corner_radius=20,
                                border_width=2,
                                border_color='#FB9C8D',
                                font=("Roboto", 15, "bold"),
                                fg_color="#171717",
                                text_color="white",
                                
                                placeholder_text="Repetir Senha",
                                show="*"
                                )
        self.c_senha_entry.place(x=315,y=215)

        #Botão de cadastrar
        self.cadastrar_btn = ctk.CTkButton(self,
                                    width=30,
                                    height=40,
                                    text="Cadastrar",
                                    command=lambda: self.onclick(
                                                                self.nome_entry.get().capitalize(),
                                                                self.user_entry.get().lower(),
                                                                self.email_entry.get().lower(),
                                                                self.senha_entry.get(),
                                                                self.c_senha_entry.get(),
                                                                ),
                                    border_width=2,
                                    border_color='#FB9C8D',
                                    corner_radius=20,
                                    font=("Roboto", 16, "bold"),
                                    fg_color='#171717',
                                    hover_color='#454545'
                                    )
        self.cadastrar_btn.place(x=238, y=300)

        #Botão de exibir a senha do entry da senha
        self.show_btn1 = ctk.CTkButton(self,
                                            text="",
                                            image=iconspath.CLOSED_EYE_ICON,
                                            width=10,
                                            height=10,
                                            corner_radius=50,
                                            fg_color="#171717",
                                            bg_color="#171717",
                                            hover_color="#454545",
                                            command=self.show_hide_senha
                                           )
        self.show_btn1.place(x=234,y=224)

        #Botão de ocultar a senha do entry da senha
        self.hide_btn1 = ctk.CTkButton(self,
                                            text="",
                                            image=iconspath.EYE_ICON,
                                            width=10,
                                            height=10,
                                            corner_radius=50,
                                            fg_color="#171717",
                                            bg_color="#171717",
                                            hover_color="#454545",
                                            command=self.show_hide_senha
                                            
                                            )
        self.hide_btn1.place(x=234,y=224)

        #Botão de exibir a senha do entry de confirmação de senha
        self.show_btn2 = ctk.CTkButton(self,
                                            text="",
                                            image=iconspath.CLOSED_EYE_ICON,
                                            width=10,
                                            height=10,
                                            corner_radius=50,
                                            fg_color="#171717",
                                            bg_color="#171717",
                                            hover_color="#454545",
                                            command=self.show_hide_c_senha
                                            
                                            )
        self.show_btn2.place(x=450,y=224)

        #Botão de ocultar a senha do entry de confirmação de senha
        self.hide_btn2 = ctk.CTkButton(self,
                                            text="",
                                            image=iconspath.EYE_ICON,
                                            width=10,
                                            height=10,
                                            corner_radius=50,
                                            fg_color="#171717",
                                            bg_color="#171717",
                                            hover_color="#454545",
                                            command=self.show_hide_c_senha
                                            
                                            )
        self.hide_btn2.place(x=450,y=224)

        #Botão para deletar um admin
        self.delete_admin = ctk.CTkButton(self,
                                          width=5,
                                          height=20,
                                          text="Deletar admin?",
                                          fg_color="transparent",
                                          text_color="white",
                                          font=("Roboto", 13, "bold"),
                                          command=lambda: self.deletar_admin(),
                                          hover_color='#155e75',
        )
        self.delete_admin.place(x=5, y=378)
    
    #Abre a janela de deletar admins
    def deletar_admin(self):
        deletar = DeleteAdmin(self)
        deletar.grab_set()

    #Exibe/Esconde a senha do entry da senha
    def show_hide_senha(self):
        if self.senha_oculta:
            self.senha_entry.configure(show="")
            self.hide_btn1.place_forget()
            self.show_btn1.place(x=234,y=224)
            self.senha_oculta = False
        else:
            self.senha_entry.configure(show="*")
            self.show_btn1.place_forget()
            self.hide_btn1.place(x=234,y=224)
            self.senha_oculta = True
        
    #Exibe/Esconde a senha do entry de confirmação de senha
    def show_hide_c_senha(self):
        if self.c_senha_oculta:
            self.c_senha_entry.configure(show="")
            self.hide_btn2.place_forget()
            self.show_btn2.place(x=450,y=224)
            self.c_senha_oculta = False
        else:
            self.c_senha_entry.configure(show="*")
            self.show_btn2.place_forget()
            self.hide_btn2.place(x=450,y=224)
            self.c_senha_oculta = True

    #Cadastra um novo Administrador
    def onclick(self, nome, usuario, email, senha1, senha2):
        if functions.check_field(usuario, 5):
            user = usuario
            if functions.check_req(senha1, senha2):
                if functions.check(senha1, senha2):
                    senha = senha2
                    try:
                        config.create_admin(nome, user, senha, email, config.timenow())
                        messagebox.showinfo("Hey", "Admin cadastrado com sucesso")
                        self.destroy()
                    except:
                        messagebox.showwarning("Erro", "Não foi possível realizar o cadastro. Tente novamente")
                else:
                    messagebox.showerror("Erro", "As senhas não se coincidem")
            else:
                messagebox.showerror("Erro", "As senhas devem possuir no mínimo 8 dígitos")
            
        else:
            messagebox.showerror("Erro", f"O Usuário deve ter no mínimo 5 caracteres")

#Janela principal
class Gestor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1400x718")
        self.title("Gerenciamento")
        self.iconbitmap(r'Icons\imgs\icons8-management-90.ico')
        self.tema_atual = "#171717"
        self.configure(bg=self.tema_atual)
        self.bar_status = "reduced"
        self.admin_status = AdminStatus()
        self.resizable(False, False)

        #Home
        home_widgets(self)
        
        #Frame da opção de férias
        self.ferias_frame = ctk.CTkFrame(self,
                                         width=0,
                                         height=720,
                                         fg_color=self.tema_atual,
                                         )
        self.ferias_frame.place(x=52,y=0)
        vacation_widgets(self.ferias_frame)

        #Frame da opção de Promover
        self.promover_frame = ctk.CTkFrame(self,
                                         width=0,
                                         height=720,
                                         fg_color=self.tema_atual,
                                         )
        self.promover_frame.place(x=52,y=0)
        promote_widgets(self.promover_frame)

        #Frame da opção de Horas extras
        self.hora_extra_frame = ctk.CTkFrame(self,
                                         width=0,
                                         height=720,
                                         fg_color=self.tema_atual,
                                         )
        self.hora_extra_frame.place(x=52,y=0)
        overtime_widgets(self.hora_extra_frame)

        #Frame da opção de Folha de pagamento
        self.folha_pagamento_frame = ctk.CTkFrame(self,
                                         width=0,
                                         height=720,
                                         fg_color=self.tema_atual,
                                         )
        self.folha_pagamento_frame.place(x=52,y=0)
        payroll_widgets(self.folha_pagamento_frame)

        #Frame da opção de Cadastrar
        self.cadastrar_frame = ctk.CTkFrame(self,
                                         width=0,
                                         height=720,
                                         fg_color=self.tema_atual,
                                         )
        self.cadastrar_frame.place(x=52,y=0)
        register_widgets(self.cadastrar_frame)


        # Fundo da barra lateral inicial
        self.sidebar_bg = ctk.CTkFrame(self,
                              fg_color='#0891b2',
                              width=55,
                              height=1000,
                            )
        self.sidebar_bg.place(x=2, y=-3)

        # Delimitador da barra lateral
        self.sidebar_del = ctk.CTkFrame(self,
                                        width=3,
                                        height=1000
                                        )
        self.sidebar_del.place(x=50,y=0)
        
        # Botão da página inicial
        self.homepage_btn = ctk.CTkButton(master=self.sidebar_bg,
                                         width=45,
                                         height=45,
                                         text="",
                                         image=iconspath.HOME_ICON,
                                         fg_color="transparent",
                                         hover_color="#155e75",
                                         command= self.gohome,
                                         )
        self.tooltipx = CTkToolTip(self.homepage_btn, "Página inicial", delay=0.1)
        self.homepage_btn.pack(pady=5)

        #Botão de cadastro
        self.cadastro_btn = ctk.CTkButton(self.sidebar_bg,
                                       width=45,
                                       height=45,
                                       fg_color="transparent",
                                       hover_color="#155e75",
                                       text="",
                                       image=iconspath.CADASTRO_ICON,
                                       command=lambda: functions.open_close_frame(self.cadastro_btn, self.states)
                                       )
        self.cadastro_btn.pack(pady=30)
        self.cadastro_btn.name = "cadastrar"
        self.tooltip1 = CTkToolTip(self.cadastro_btn, "Cadastrar", delay=0.1)

        #Botão de Promover
        self.promover_btn = ctk.CTkButton(self.sidebar_bg,
                                       width=45,
                                       height=45,
                                       fg_color="transparent",
                                       hover_color="#155e75",
                                       text="",
                                       image=iconspath.PROMOVER_ICON,
                                       command=lambda: functions.open_close_frame(self.promover_btn, self.states)
                                       )
        self.promover_btn.pack(pady=30)
        self.promover_btn.name = "promover"
        self.tooltip5 = CTkToolTip(self.promover_btn, "Promover/Demitir", delay=0.1)

        #Botão de Folha de pagamento
        self.folha_pagamento_btn = ctk.CTkButton(self.sidebar_bg,
                                       width=45,
                                       height=45,
                                       fg_color="transparent",
                                       hover_color="#155e75",
                                       text="",
                                       image=iconspath.FOLHA_PAGAMENTO_ICON,
                                       command=lambda: functions.open_close_frame(self.folha_pagamento_btn, self.states)
                                       )
        self.folha_pagamento_btn.pack(pady=30)
        self.folha_pagamento_btn.name = "folha pagamento"
        self.tooltip2 = CTkToolTip(self.folha_pagamento_btn, "Folha de Pagamento", delay=0.1)

        #Botão de Horas extras
        self.hora_extra_btn = ctk.CTkButton(self.sidebar_bg,
                                       width=45,
                                       height=45,
                                       fg_color="transparent",
                                       hover_color="#155e75",
                                       text="",
                                       image=iconspath.HORA_EXTRA_ICON,
                                       command=lambda: functions.open_close_frame(self.hora_extra_btn, self.states)
                                       )
        self.hora_extra_btn.pack(pady=30)
        self.hora_extra_btn.name = "hora extra"
        self.tooltip4 = CTkToolTip(self.hora_extra_btn, "Horas Extras", delay=0.1)

        #Botão de ferias
        self.ferias_btn = ctk.CTkButton(self.sidebar_bg,
                                       width=45,
                                       height=45,
                                       fg_color="transparent",
                                       hover_color="#155e75",
                                       text="",
                                       image=iconspath.FERIAS_ICON,
                                       command=lambda: functions.open_close_frame(self.ferias_btn, self.states)
                                       )
        self.ferias_btn.pack(pady=30)
        self.ferias_btn.name = "ferias"
        self.tooltip6 = CTkToolTip(self.ferias_btn, "Férias", delay=0.1)

        #Linha que separa as opções de admin das demais opções
        self.limitador = ctk.CTkFrame(self.sidebar_bg,
                                      width=30,
                                      height=3,
                                      fg_color="#FB9C8D",
                                      corner_radius=20,
                                      )
        self.limitador.pack(pady=30)

        #Botão admin (Autenticar/Ações)
        self.admin_btn = ctk.CTkButton(self.sidebar_bg,
                                       width=45,
                                       height=45,
                                       fg_color="transparent",
                                       hover_color="#155e75",
                                       text="",
                                       image=iconspath.ADMIN_ICON,
                                       command=self.admin_cmd
                                       )
        self.admin_btn.pack(pady=30)
        self.tooltip7 = CTkToolTip(self.admin_btn, "Administrador", delay=0.1)

        #Controlador dos frames
        self.states = {
            "ferias": [self.ferias_frame, "reduced"],
            "promover": [self.promover_frame, "reduced"],
            "hora extra": [self.hora_extra_frame, "reduced"],
            "folha pagamento": [self.folha_pagamento_frame, "reduced"],
            "cadastrar": [self.cadastrar_frame, "reduced"]

        }
               
    # Vai para a página inicial
    def gohome(self):
        # Fecha os demais frames
        for i in self.states:
            if self.states[i][1] == "expanded":
                self.states[i][0].configure(width=1)
                self.states[i][1] = "reduced"

        # Atualiza os status dos demais frames
  
    #Abre a janela de adm (Se estiver logado), se não estiver, abre a janela de autenticação
    def admin_cmd(self):
        if not self.admin_status.is_logged():
            auth = AuthAdmin(self, self.admin_status)
            auth.grab_set()
        else:
            adm = ADM(self, self.admin_status)
            adm.grab_set()


if __name__ == "__main__":
    gestor = Gestor()
    gestor.mainloop()
