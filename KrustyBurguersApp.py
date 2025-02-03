#Krusty's App
import customtkinter as ctk
import sqlite3 as sql

#criação do banco de dados
class BackEnd():
    def conecta_banco(self):
        self.conn = sql.connect("KrustyBurguer.db")
        self.cursor = self.conn.cursor()
        print("Conectado ao banco de dados")
    def desconecta_banco(self):
        self.conn.close()
        print("Desconectado ao banco de dados")
    def cria_tabela(self):
        self.conecta_banco()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Usuários (
            Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            Nome TEXT NOT NULL,
            Email TEXT NOT NULL,
            Senha TEXT NOT NULL,
            Confirma_Senha TEXT NOT NULL               
        );
        """)
    def cadastro_usuario(self):
        self.nome=self.user_entry.get()
        self.email=self.email_entry.get()
        self.senha=self.senha_entry.get()
        self.confirma_senha=self.c_senha_entry.get()

        print(self.nome)

class App(ctk.CTk, BackEnd):
    def __init__(self):
        super().__init__()
        
        self.config_tela()
        self.login() #dentro da função login temos as chamadas para as funções de cadastro e esqueceu_senha então não é necessário chamar essas funções aqui
        
    #configuração da tela
    def config_tela(self):
        
        self.geometry("800x600")
        self.title("Krusty's App")

    #tela de login
    def login(self):

        #login frame
        self.frame_login = ctk.CTkFrame(self, fg_color=["white","grey"], width=350, height=600)
        self.frame_login.pack(side = "top", expand = True, fill = "y")

        #login frames widgets
        self.login_label = ctk.CTkLabel(self.frame_login, text="Welcome to Krusty's App", text_color= "blue", font=("Arial", 20))
        self.login_label.place(x=50, y=50)

        self.usuario_entry = ctk.CTkEntry(self.frame_login, placeholder_text="Usuario", width=250, height= 35, font=("Arial", 14))
        self.usuario_entry.place(x=40, y=150)

        self.usuario_label = ctk.CTkLabel(self.frame_login, text="*Campo obrigatório", height=0,text_color="blue", font=("Arial", 10))
        self.usuario_label.place(x=45, y=188)

        self.senha_entry = ctk.CTkEntry(self.frame_login, placeholder_text="Senha", width=250, height= 35, font=("Arial", 14), show = "*")
        self.senha_entry.place(x=40, y=205)

        self.senha_label = ctk.CTkLabel(self.frame_login, text="*Campo obrigatório", height=0,text_color="blue", font=("Arial", 10))
        self.senha_label.place(x=45, y=243)

        self.lembrar_check = ctk.CTkCheckBox(self.frame_login, checkbox_width=20, checkbox_height=20, text="Lembrar de mim", font=("Arial", 14))
        self.lembrar_check.place(x=45, y=270)

        self.login_button = ctk.CTkButton(self.frame_login, text="Login", width=200, height=30, font=("Arial", 14))
        self.login_button.place(x=65, y= 310)

        self.cadastro_button = ctk.CTkButton(self.frame_login, text="Cadastre-se", width=200, height=30, font=("Arial", 14), command=self.cadastro)
        self.cadastro_button.place(x=65, y= 350)

        self.esqueceu_button = ctk.CTkButton(self.frame_login, text="Esqueceu sua senha?", width=200, height=30, font=("Arial", 14), command = self.esqueceu_senha)
        self.esqueceu_button.place(x=65, y= 390)

    #tela de registro
    def cadastro(self):

        def back():
            #Remover frame de cadastro
            self.frame_cadastro.pack_forget()
            
            #Retornar para a tela de login
            self.frame_login.pack(side = "top", expand = True, fill = "y")   

        #removendo login frame
        self.frame_login.pack_forget()

        #cadastro frame
        self.frame_cadastro = ctk.CTkFrame(self, fg_color=["white","grey"], width=350, height=600)
        self.frame_cadastro.pack(side = "top", expand = True, fill = "y")
            
        self.cadastro_label = ctk.CTkLabel(self.frame_cadastro, text="Welcome to Krusty's App", text_color= "blue", font=("Arial", 20))
        self.cadastro_label.place(x=50, y=50)

        self.email_entry = ctk.CTkEntry(self.frame_cadastro, placeholder_text="Insira seu e-mail", width=250, height= 35, font=("Arial", 14))
        self.email_entry.place(x=40, y=150)

        self.email_label = ctk.CTkLabel(self.frame_cadastro, text="*Campo obrigatório", height=0,text_color="blue", font=("Arial", 10))
        self.email_label.place(x=45, y=188)

        self.user_entry = ctk.CTkEntry(self.frame_cadastro, placeholder_text="Insira o nome da Empresa", width=250, height= 35, font=("Arial", 14))
        self.user_entry.place(x=40, y=205)

        self.user_label = ctk.CTkLabel(self.frame_cadastro, text="*Campo obrigatório", height=0,text_color="blue", font=("Arial", 10))
        self.user_label.place(x=45, y=243)

        self.senha_entry = ctk.CTkEntry(self.frame_cadastro, placeholder_text="Senha", width=250, height= 35, font=("Arial", 14), show = "*")
        self.senha_entry.place(x=40, y=260)

        self.senha_label = ctk.CTkLabel(self.frame_cadastro, text="*Campo obrigatório", height=0,text_color="blue", font=("Arial", 10))
        self.senha_label.place(x=45, y=300)

        self.c_senha_entry = ctk.CTkEntry(self.frame_cadastro, placeholder_text="Digite novamente a senha", width=250, height= 35, font=("Arial", 14), show = "*")
        self.c_senha_entry.place(x=40, y=317)

        self.termo_de_uso = ctk.CTkCheckBox(self.frame_cadastro, checkbox_width=20, checkbox_height=20, text="Aceito os termos de uso", font=("Arial", 14))
        self.termo_de_uso.place(x=45, y=370)

        self.confirmar_button = ctk.CTkButton(self.frame_cadastro, text="Confirmar", width=200, height=30, font=("Arial", 14), command=self.cadastro_usuario)
        self.confirmar_button.place(x=65, y= 410)  

        self.voltar_button = ctk.CTkButton(self.frame_cadastro, text="Voltar", width=150, height=25, font=("Arial", 14), command=back)
        self.voltar_button.place(x=90, y= 450)    

    #tela de "esqueceu sua senha?"
    def esqueceu_senha(self):

        def back():
            #Remover frame de esqueceu
            self.frame_esqueceu.pack_forget()
            
            #Retornar para a tela de login
            self.frame_login.pack(side = "top", expand = True, fill = "y")

        self.frame_login.pack_forget()

        #esqueceu frame
        self.frame_esqueceu = ctk.CTkFrame(self, fg_color=["white","grey"], width=350, height=600)
        self.frame_esqueceu.pack(side = "top", expand = True, fill = "y")

        self.esqueceu_label = ctk.CTkLabel(self.frame_esqueceu, text="Confirme que é você", text_color= "blue", font=("Arial", 20))
        self.esqueceu_label.place(x=50, y=50)

        self.email_entry = ctk.CTkEntry(self.frame_esqueceu, placeholder_text="Insira seu e-mail", width=250, height= 35, font=("Arial", 14))
        self.email_entry.place(x=40, y=150)

        self.email_label = ctk.CTkLabel(self.frame_esqueceu, text="*Campo obrigatório", height=0,text_color="blue", font=("Arial", 10))
        self.email_label.place(x=45, y=188)

        self.user_entry = ctk.CTkEntry(self.frame_esqueceu, placeholder_text="Insira o nome da Empresa", width=250, height= 35, font=("Arial", 14))
        self.user_entry.place(x=40, y=205)

        self.user_label = ctk.CTkLabel(self.frame_esqueceu, text="*Campo obrigatório", height=0,text_color="blue", font=("Arial", 10))
        self.user_label.place(x=45, y=243)

        self.senha_entry = ctk.CTkEntry(self.frame_esqueceu, placeholder_text="Nova senha", width=250, height= 35, font=("Arial", 14), show = "*")
        self.senha_entry.place(x=40, y=260)

        self.senha_label = ctk.CTkLabel(self.frame_esqueceu, text="*Campo obrigatório", height=0,text_color="blue", font=("Arial", 10))
        self.senha_label.place(x=45, y=300)

        self.c_senha_entry = ctk.CTkEntry(self.frame_esqueceu, placeholder_text="Confirme a nova senha", width=250, height= 35, font=("Arial", 14), show = "*")
        self.c_senha_entry.place(x=40, y=317)

        self.confirmar_button = ctk.CTkButton(self.frame_esqueceu, text="Confirmar", width=200, height=30, font=("Arial", 14))
        self.confirmar_button.place(x=65, y= 370)

        self.voltar_button = ctk.CTkButton(self.frame_esqueceu, text="Voltar", width=150, height=25, font=("Arial", 14), command = back)
        self.voltar_button.place(x=90, y= 410)

if __name__ == "__main__":    
    app = App()
    app.mainloop()

#validação de usuario

#validação de senha

#validação de email

#Menu de configurações

#DashBoard

#Tela de cadastro de produtos

#Impressão de arquivo em pdf

#transformar em executável