#Krusty's App
import customtkinter as ctk
import sqlite3 as sql
from tkinter import *
from tkinter import messagebox, PhotoImage
from PIL import Image

#banco de dados
class BackEnd():
    #função que conecta ao banco de dados
    def conecta_banco(self):
        self.conn = sql.connect("KrustyBurguer.db")
        self.cursor = self.conn.cursor()
        print("Conectado ao banco de dados")
    #função que desconecta ao banco de dados
    def desconecta_banco(self):
        self.cursor.close()
        self.conn.close()
        print("Desconectado ao banco de dados")
    #função que cria a tabela de Usuários
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
        self.conn.commit()
        self.desconecta_banco()
    
    #função de cadastro de usuários
    def cadastro_usuario(self):
        def back():
            #Remover frame de cadastro
            self.frame_cadastro.pack_forget()
            
            #Retornar para a tela de login
            self.frame_login.pack(side = "top", expand = True, fill = "y")
        
        def limpa_entry():
            self.user_entry.delete(0, END)
            self.email_entry.delete(0, END)
            self.senha_entry.delete(0, END)
            self.c_senha_entry.delete(0, END)
        
        self.nome=self.user_entry.get()
        self.email=self.email_entry.get()
        self.senha=self.senha_entry.get()
        self.confirma_senha=self.c_senha_entry.get()

        self.conecta_banco()

        self.cursor.execute("""
        INSERT INTO Usuários (Nome, Email, Senha, Confirma_Senha) VALUES (?,?,?,?)
        """, (self.nome, self.email, self.senha, self.confirma_senha))

        self.cursor.execute("""
        SELECT * FROM Usuários WHERE (Nome=? AND Senha=?)
        """, (self.nome, self.senha))
        
        self.verifica_dados=self.cursor.fetchone()
        
        try:
            if(self.nome in self.verifica_dados or self.senha in self.verifica_dados):
                messagebox.showerror(title="CADASTRO", message="Nome e Email já existentes.")
            if (self.nome=="" or self.email=="" or self.senha=="" or self.confirma_senha==""):
                messagebox.showerror(title="CADASTRO", message="Nem todos os campos foram preenchidos.")
            elif (self.senha!=self.confirma_senha):
                messagebox.showerror(title="CADASTRO", message="Coloque senhas iguais.")
            elif (len(self.senha)<8):
                messagebox.showerror(title="CADASTRO", message="A senha deve ter 8 caracteres.")
            else:
                self.conn.commit()
                messagebox.showinfo(title="CADASTRO", message=f"Cadastro de {self.nome} concluído com sucesso!")
                self.desconecta_banco()
                back()
        except:
            messagebox.showerror(title="CADASTRO", message="Não foi possível coletar seus dados.\nTente novamente.")
            limpa_entry()    

    #função de login
    def verifica_login(self):
        def limpa_entry():
            self.usuario_entry.delete(0, END)
            self.senha_entry.delete(0, END)
        
        self.nome=self.usuario_entry.get()
        self.senha=self.senha_entry.get()

        self.conecta_banco()

        self.cursor.execute("""
        SELECT * FROM Usuários WHERE (Nome=? AND Senha=?)
        """, (self.nome, self.senha))
        
        self.verifica_dados=self.cursor.fetchone()

        try:
            if(self.nome in self.verifica_dados and self.senha in self.verifica_dados):
                messagebox.showinfo(title="LOGIN", message="Login realizado com sucesso!")
                self.desconecta_banco()
        except:
            messagebox.showerror(title="LOGIN", message="Usuário ou senha incorretos.")
            self.desconecta_banco()
        
        limpa_entry()
    
    def troca_de_senha(self):
        def back():
            #Remover frame de esqueceu
            self.frame_esqueceu.pack_forget()
            
            #Retornar para a tela de login
            self.frame_login.pack(side = "top", expand = True, fill = "y")
        def limpa_entry():
            self.user_entry.delete(0, END)
            self.email_entry.delete(0, END)
            self.senha_entry.delete(0, END)
            self.c_senha_entry.delte(0, END)

        self.nome=self.user_entry.get()
        self.email=self.email_entry.get()
        self.senha=self.senha_entry.get()
        self.confirma_senha=self.c_senha_entry.get()

        self.conecta_banco()
        self.cursor.execute("""
        SELECT * FROM Usuários WHERE (Nome=? AND Email=?)
        """, (self.nome, self.email))
        self.verifica_dados=self.cursor.fetchone()
       
        try:
            if (self.nome=="" or self.email=="" or self.senha=="" or self.confirma_senha==""):
                messagebox.showerror(title="TROCA DE SENHA", message="Nem todos os campos foram preenchidos.")
                self.desconecta_banco()
            elif(self.verifica_dados==None):
                messagebox.showerror(title="TROCA DE SENHA", message="Usuário não encontrado")
                self.desconecta_banco()
            elif (self.senha!=self.confirma_senha):
                messagebox.showerror(title="TROCA DE SENHA", message="Coloque senhas iguais.")
                self.desconecta_banco()
            elif (len(self.senha)<8):
                messagebox.showerror(title="TROCA DE SENHA", messagebox="Coloque uma senha com maios de 8 caracteres.")
                self.desconecta_banco()
            elif(self.nome in self.verifica_dados and self.email in self.verifica_dados):
                self.cursor.execute("""
                UPDATE Usuários SET Senha=?, Confirma_Senha=? WHERE Nome=?""", (self.senha, self.confirma_senha, self.nome))
                self.conn.commit()
                messagebox.showinfo(title="TROCA DE SENHA", message="Troca de senha realizada com sucesso!")
                self.desconecta_banco()
                back()
        except:
            messagebox.showerror(title="TROCA DE SENHA", messagebox="Não foi possível trocar a sua senha.\nTente novamente.")
            self.desconecta_banco()
            limpa_entry()

class App(ctk.CTk, BackEnd):
    def __init__(self):
        super().__init__()
        
        self.config_tela()
        self.login() #dentro da função login temos as chamadas para as funções de cadastro e esqueceu_senha então não é necessário chamar essas funções aqui
        self.cria_tabela()

    #configuração da tela
    def config_tela(self):
        
        self.geometry("800x600")
        self.title("Krusty's App")
        self.iconbitmap("Krusty.ico")
        self.resizable(False, False)
        

    #tela de login
    def login(self):
        
        #Background
        self.img = ctk.CTkImage(light_image = Image.open("f_background.png"), dark_image= Image.open("f_background.png"), size=(800,600))
        self.background = ctk.CTkLabel(self, image=self.img, text= None).place(x = 0, y = 0)
        '''self.img = PhotoImage(file="background1.png")
        self.background = ctk.CTkLabel(self, image=self.img, text = None)
        self.background.place(x=0, y=0)'''
        '''self.logomarca = ctk.CTkImage(light_image= Image.open("logomarca3.png"), dark_image = Image.open("logomarca3.png"), size = (250, 250))
        self.logomarca = ctk.CTkLabel(self.background, image=self.logomarca, text=None, width=100,bg_color="transparent", height=100).place(x=(600-350)/2, y=150)'''

        #login frame
        self.frame_login = ctk.CTkFrame(self, fg_color=["#FDFDFD","#0D0D0D"], width=350, height=600)
        self.frame_login.pack(side = "right")

        self.usuario_imag = ctk.CTkImage(light_image=Image.open("username.png"), dark_image=Image.open("username.png"), size=(114, 27))
        self.usuario_imag = ctk.CTkLabel(self.frame_login, image=self.usuario_imag, text = None).place(x= 38.07,y=216.19)

        self.usuario_entry = ctk.CTkEntry(self.frame_login, placeholder_text_color=None, fg_color=["#FDFDFD","#0D0D0D"], border_width = 2, border_color="#9C00D4", corner_radius= 100, width=300, height= 25, font=("Sometype Mono Bold", 14)) #tentar colocar width=1 com a imagem pra testar se da certo
        self.usuario_entry.place(relx=0.5, y=255, anchor = "center")

        '''self.usuario_label = ctk.CTkLabel(self.frame_login, text="*Campo obrigatório", height=0,text_color="blue", font=("Arial", 10))
        self.usuario_label.place(x=45, y=188)'''

        self.senha_img = ctk.CTkImage(light_image=Image.open("password.png"), dark_image=Image.open("password.png"), size=(80, 26))
        self.senha_img = ctk.CTkLabel(self.frame_login, image=self.senha_img, text=None).place(x=38.07, y=290.03)

        self.senha_entry = ctk.CTkEntry(self.frame_login, placeholder_text_color=None, fg_color=["#FDFDFD","#0D0D0D"], border_width = 2, border_color="#9C00D4", corner_radius= 100, width=300, height= 25, font=("Sometype Mono Bold", 14), show = "*")
        self.senha_entry.place(relx = 0.5, y=330, anchor = "center")

        '''self.senha_label = ctk.CTkLabel(self.frame_login, text="*Campo obrigatório", height=0,text_color="blue", font=("Arial", 10))
        self.senha_label.place(x=45, y=243)'''

        self.lembrar_check = ctk.CTkCheckBox(self.frame_login, checkbox_width=12.36, checkbox_height=12.36, border_color = "#9C00D4", border_width= 1.35, corner_radius= 2, checkmark_color="#9C00D4", text="Manter usuário", text_color= "#9C00D4", fg_color=["#FDFDFD","#0D0D0D"], hover = False, font=("Sometype Mono SemiBold", 12.26))
        self.lembrar_check.place(x=37.5, y=364.49)

        self.login_button = ctk.CTkImage(light_image=Image.open("BotãoDeLogin.png"), dark_image=Image.open("BotãoDeLogin.png"), size=(114, 34))
        self.login_button = ctk.CTkButton(self.frame_login, image= self.login_button, text=None, bg_color=["#FDFDFD","#0D0D0D"], fg_color=["#FDFDFD","#0D0D0D"], hover= None, width=1, height=1, command=self.verifica_login)
        self.login_button.place(relx = 0.5, y= 452.86, anchor = "center")

        self.cadastro_button = ctk.CTkButton(self.frame_login, text="CADASTRE-SE", text_color= "#9C00D4", fg_color=["#FDFDFD","#0D0D0D"], width=1, height=1, hover = False, font=("Sometype Mono Bold", 10.21), command=self.cadastro)
        self.cadastro_button.place(relx=0.5, y= 511.46, anchor = "center")

        self.esqueceu_button = ctk.CTkButton(self.frame_login, text="Esqueceu sua senha?",text_color= "#9C00D4", fg_color=["#FDFDFD","#0D0D0D"], width=1, height=1, hover = False, font=("Sometype Mono SemiBold", 12.26), command = self.esqueceu_senha)
        self.esqueceu_button.place(x=185.48, y= 364.49)

        self.creditos = ctk.CTkLabel(self.frame_login, text="Development by ArthurVinxcius and isjustjefferson", text_color= "#9C00D4", font=("Sometype Mono Bold", 10.21)).place(relx = 0.5, y= 578.37, anchor = "center")

        self.login_title = ctk.CTkImage(light_image=Image.open("Title.png"), dark_image=Image.open("Title.png"), size=(206, 75))
        self.login_title = ctk.CTkLabel(self.frame_login, image= self.login_title, text = None).place(x = 26.49, y = 18.63)

        self.boneco_grande = ctk.CTkImage(light_image=Image.open("BonecoGrande.png"), dark_image=Image.open("BonecoGrande.png"),size=(70, 70))
        self.boneco_grande = ctk.CTkLabel(self.frame_login, image=self.boneco_grande, text=None).place(relx = 0.5, y=158.34, anchor = "center")

    #tela de registro
    def cadastro(self):

        def back():
            #Remover frame de cadastro
            self.frame_cadastro.pack_forget()
            
            #Retornar para a tela de login
            self.frame_login.pack(side = "right")   

        #removendo login frame
        self.frame_login.pack_forget()

        #cadastro frame
        self.frame_cadastro = ctk.CTkFrame(self, fg_color=["#FDFDFD","#0D0D0D"], width=350, height=600)
        self.frame_cadastro.pack(side = "right")
            
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
            self.frame_login.pack(side = "right")

        self.frame_login.pack_forget()

        #esqueceu frame
        self.frame_esqueceu = ctk.CTkFrame(self, fg_color=["#FDFDFD","#0D0D0D"], width=350, height=600)
        self.frame_esqueceu.pack(side = "right")

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

        self.confirmar_button = ctk.CTkButton(self.frame_esqueceu, text="Confirmar", width=200, height=30, font=("Arial", 14), command=self.troca_de_senha)
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