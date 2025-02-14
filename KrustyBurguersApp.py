import customtkinter as ctk
import sqlite3 as sql
from tkinter import *
from tkinter import messagebox, PhotoImage
from PIL import Image

class BackEnd():
    def conecta_banco(self):
        self.conn = sql.connect("KrustyBurguer.db")
        self.cursor = self.conn.cursor()
        print("Conectado ao banco de dados")
    def desconecta_banco(self):
        self.cursor.close()
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
        self.conn.commit()
        self.desconecta_banco()
   
    def cadastro_usuario(self):
        
        self.nome=self.user_entry.get()
        self.email=self.email_entry.get()
        self.senha=self.senha_entry.get()
        self.confirma_senha=self.c_senha_entry.get()

        self.conecta_banco()

        self.cursor.execute("""
        INSERT INTO Usuários (Nome, Email, Senha, Confirma_Senha) VALUES (?,?,?,?)
        """, (self.nome, self.email, self.senha, self.confirma_senha))

        
        try:
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
        except:
            messagebox.showerror(title="CADASTRO", message="Não foi possível coletar seus dados.\nTente novamente.")    
   
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
            if (self.nome in self.verifica_dados and self.senha in self.verifica_dados):
                self.main_frame()
                self.desconecta_banco()
            else:
                messagebox.showerror(title="LOGIN", message="Usuário ou senha incorretos.")
                self.desconecta_banco()
        except:
            messagebox.showerror(title="LOGIN", message="Usuário ou senha incorretos.")
            self.desconecta_banco()
        
        limpa_entry()
   
    def troca_de_senha(self):

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
                
        except:
            messagebox.showerror(title="TROCA DE SENHA", messagebox="Não foi possível trocar a sua senha.\nTente novamente.")
            self.desconecta_banco()

class App(ctk.CTk, BackEnd):
    def __init__(self):
        super().__init__()
        
        self.config_tela()
        self.login()
        self.cria_tabela()

    def config_tela(self):
        
        self.geometry("800x600")
        self.title("Krusty's App")
        self.resizable(False, False)
        
    def login(self):
        
        self.img = ctk.CTkImage(light_image = Image.open("Imagens\\f_background.png"), dark_image= Image.open("Imagens\\f_background.png"), size=(800,600))
        self.background = ctk.CTkLabel(self, image=self.img, text= None).place(x = 0, y = 0)
        
        self.frame_login = ctk.CTkFrame(self, fg_color=["#FDFDFD","#0D0D0D"], width=350, height=600)
        self.frame_login.pack(side = "right")

        self.usuario_imag = ctk.CTkImage(light_image=Image.open("Imagens\\username.png"), dark_image=Image.open("Imagens\\username.png"), size=(114, 27))
        self.usuario_imag = ctk.CTkLabel(self.frame_login, image=self.usuario_imag, text = None).place(x= 38.07,y=216.19)

        self.usuario_entry = ctk.CTkEntry(self.frame_login, placeholder_text_color=None, fg_color=["#FDFDFD","#0D0D0D"], border_width = 2, border_color="#9C00D4", corner_radius= 100, width=300, height= 25, font=("Sometype Mono Bold", 14)) 
        self.usuario_entry.place(relx=0.5, y=255, anchor = "center")

        self.senha_img = ctk.CTkImage(light_image=Image.open("Imagens\\password.png"), dark_image=Image.open("Imagens\\password.png"), size=(80, 26))
        self.senha_img = ctk.CTkLabel(self.frame_login, image=self.senha_img, text=None).place(x=38.07, y=290.03)

        self.senha_entry = ctk.CTkEntry(self.frame_login, placeholder_text_color=None, fg_color=["#FDFDFD","#0D0D0D"], border_width = 2, border_color="#9C00D4", corner_radius= 100, width=300, height= 25, font=("Sometype Mono Bold", 14), show = "*")
        self.senha_entry.place(relx = 0.5, y=330, anchor = "center")

        self.lembrar_check = ctk.CTkCheckBox(self.frame_login, checkbox_width=12.36, checkbox_height=12.36, border_color = "#9C00D4", border_width= 1.35, corner_radius= 2, checkmark_color="#9C00D4", text="Manter usuário", text_color= "#9C00D4", fg_color=["#FDFDFD","#0D0D0D"], hover = False, font=("Sometype Mono SemiBold", 12.26))
        self.lembrar_check.place(x=37.5, y=364.49)

        self.login_button = ctk.CTkImage(light_image=Image.open("Imagens\\BotãoDeLogin.png"), dark_image=Image.open("Imagens\\BotãoDeLogin.png"), size=(114, 34))
        self.login_button = ctk.CTkButton(self.frame_login, image= self.login_button, text=None, bg_color=["#FDFDFD","#0D0D0D"], fg_color=["#FDFDFD","#0D0D0D"], hover= None, width=1, height=1, command=self.verifica_login)
        self.login_button.place(relx = 0.5, y= 452.86, anchor = "center")

        self.cadastro_button = ctk.CTkButton(self.frame_login, text="CADASTRE-SE", text_color= "#9C00D4", fg_color=["#FDFDFD","#0D0D0D"], width=1, height=1, hover = False, font=("Sometype Mono Bold", 10.21), command=self.cadastro)
        self.cadastro_button.place(relx=0.5, y= 511.46, anchor = "center")

        self.esqueceu_button = ctk.CTkButton(self.frame_login, text="Esqueceu sua senha?",text_color= "#9C00D4", fg_color=["#FDFDFD","#0D0D0D"], width=1, height=1, hover = False, font=("Sometype Mono SemiBold", 12.26), command = self.esqueceu_senha)
        self.esqueceu_button.place(x=185.48, y= 364.49)

        self.creditos = ctk.CTkLabel(self.frame_login, text="Development by ArthurVinxcius and isjustjefferson", text_color= "#9C00D4", font=("Sometype Mono Bold", 10.21)).place(relx = 0.5, y= 578.37, anchor = "center")

        self.login_title = ctk.CTkImage(light_image=Image.open("Imagens\\Title.png"), dark_image=Image.open("Imagens\\Title.png"), size=(206, 75))
        self.login_title = ctk.CTkLabel(self.frame_login, image= self.login_title, text = None).place(x = 26.49, y = 18.63)

        self.boneco_grande = ctk.CTkImage(light_image=Image.open("Imagens\\BonecoGrande.png"), dark_image=Image.open("Imagens\\BonecoGrande.png"),size=(70, 70))
        self.boneco_grande = ctk.CTkLabel(self.frame_login, image=self.boneco_grande, text=None).place(relx = 0.5, y=158.34, anchor = "center")

    def cadastro(self):

        def back():
            self.frame_cadastro.pack_forget()
            self.frame_login.pack(side = "right")
            self.limpa_entradas()

        self.frame_login.pack_forget()

        self.frame_cadastro = ctk.CTkFrame(self, fg_color=["#FDFDFD","#0D0D0D"], width=350, height=600)
        self.frame_cadastro.pack(side = "right")
            
        self.boneco_grande = ctk.CTkImage(light_image=Image.open("Imagens\\BonecoGrande.png"), dark_image=Image.open("Imagens\\BonecoGrande.png"),size=(70, 70))
        self.boneco_grande = ctk.CTkLabel(self.frame_cadastro, image=self.boneco_grande, text=None).place(relx = 0.5, y=70, anchor = "center")

        self.cadastro_label = ctk.CTkLabel(self.frame_cadastro, text="REALIZE SEU CADASTRO", text_color= "#9C00D4", font=("Sometype Mono Bold", 15))
        self.cadastro_label.place(relx=0.5, y=125, anchor = "center")

        self.email_entry = ctk.CTkEntry(self.frame_cadastro, placeholder_text="Insira seu e-mail", placeholder_text_color = "#9C00D4", fg_color=["#FDFDFD","#0D0D0D"], border_width = 2, border_color="#9C00D4", text_color= "#9C00D4", corner_radius= 100, width=300, height= 25, font=("Sometype Mono Bold", 14))
        self.email_entry.place(relx=0.5, y=170, anchor = "center")

        self.user_entry = ctk.CTkEntry(self.frame_cadastro, placeholder_text="Insira o nome da Empresa", placeholder_text_color = "#9C00D4", fg_color=["#FDFDFD","#0D0D0D"], border_width = 2, text_color= "#9C00D4", border_color="#9C00D4", corner_radius= 100, width=300, height= 25, font=("Sometype Mono Bold", 14))
        self.user_entry.place(relx= 0.5, y=225, anchor = "center")

        self.senha_entry = ctk.CTkEntry(self.frame_cadastro, placeholder_text="Insira sua senha", placeholder_text_color = "#9C00D4", text_color= "#9C00D4", fg_color=["#FDFDFD","#0D0D0D"], border_width = 2, border_color="#9C00D4", corner_radius= 100, width=300, height= 25, font=("Sometype Mono Bold", 14), show = "*")
        self.senha_entry.place(relx=0.5, y=280, anchor = "center")

        self.c_senha_entry = ctk.CTkEntry(self.frame_cadastro, placeholder_text="Confirme sua senha", placeholder_text_color = "#9C00D4", fg_color=["#FDFDFD","#0D0D0D"], border_width = 2, border_color="#9C00D4", text_color= "#9C00D4", corner_radius= 100, width=300, height= 25, font=("Sometype Mono Bold", 14), show = "*")
        self.c_senha_entry.place(relx=0.5, y=337, anchor = "center")

        self.termo_de_uso = ctk.CTkCheckBox(self.frame_cadastro, checkbox_width=14, checkbox_height=14, border_color = "#9C00D4", border_width= 2, corner_radius= 2, checkmark_color="#9C00D4", text="Aceito os Termos de Uso", text_color= "#9C00D4", fg_color=["#FDFDFD","#0D0D0D"], hover = False, font=("Sometype Mono SemiBold", 14))
        self.termo_de_uso.place(relx=0.5, y=380, anchor = "center")

        self.confirmar_button = ctk.CTkImage(light_image=Image.open("Imagens\\BotãodeConfirmar.png"), dark_image=Image.open("Imagens\\BotãodeConfirmar.png"), size=(148, 33.01))
        self.confirmar_button = ctk.CTkButton(self.frame_cadastro, image= self.confirmar_button, text=None, width=1, height=1, fg_color=["#FDFDFD","#0D0D0D"], hover = None, command=self.cadastro_usuario)
        self.confirmar_button.place(relx=0.5, y= 450, anchor = "center")  

        self.voltar_button = ctk.CTkButton(self.frame_cadastro, text="VOLTAR", text_color= "#9C00D4", fg_color=["#FDFDFD","#0D0D0D"], width=1, height=1, hover = False, font=("Sometype Mono Bold", 10.21), command=back)
        self.voltar_button.place(relx=0.5, y= 500, anchor = "center")

        self.creditos = ctk.CTkLabel(self.frame_cadastro, text="Development by ArthurVinxcius and isjustjefferson", text_color= "#9C00D4", font=("Sometype Mono Bold", 10.21)).place(relx = 0.5, y= 578.37, anchor = "center")   

    def esqueceu_senha(self):

        def back():
            
            #Remover frame de esqueceu
            self.frame_esqueceu.pack_forget()
            
            #Retornar para a tela de login
            self.frame_login.pack(side = "right")
            self.limpa_entradas()
        
        self.frame_login.pack_forget()
        
        self.frame_esqueceu = ctk.CTkFrame(self, fg_color=["#FDFDFD","#0D0D0D"], width=350, height=600)
        self.frame_esqueceu.pack(side = "right")

        self.boneco_grande = ctk.CTkImage(light_image=Image.open("Imagens\\BonecoGrande.png"), dark_image=Image.open("Imagens\\BonecoGrande.png"),size=(70, 70))
        self.boneco_grande = ctk.CTkLabel(self.frame_esqueceu, image=self.boneco_grande, text=None).place(relx = 0.5, y=70, anchor = "center")

        self.esqueceu_label = ctk.CTkLabel(self.frame_esqueceu, text="CONFIRME SUA IDENTIDADE", text_color= "#9C00D4", font=("Sometype Mono Bold", 15))
        self.esqueceu_label.place(relx=0.5, y=125, anchor = "center")

        self.email_entry = ctk.CTkEntry(self.frame_esqueceu, placeholder_text="Insira seu e-mail", placeholder_text_color = "#9C00D4", fg_color=["#FDFDFD","#0D0D0D"], border_width = 2, border_color="#9C00D4", text_color= "#9C00D4", corner_radius= 100, width=300, height= 25, font=("Sometype Mono Bold", 14))
        self.email_entry.place(relx=0.5, y=170, anchor = "center")

        self.user_entry = ctk.CTkEntry(self.frame_esqueceu, placeholder_text="Insira o nome da Empresa", placeholder_text_color = "#9C00D4", fg_color=["#FDFDFD","#0D0D0D"], border_width = 2, text_color= "#9C00D4", border_color="#9C00D4", corner_radius= 100, width=300, height= 25, font=("Sometype Mono Bold", 14))
        self.user_entry.place(relx= 0.5, y=225, anchor = "center")

        self.senha_entry = ctk.CTkEntry(self.frame_esqueceu, placeholder_text="Nova senha", placeholder_text_color = "#9C00D4", text_color= "#9C00D4", fg_color=["#FDFDFD","#0D0D0D"], border_width = 2, border_color="#9C00D4", corner_radius= 100, width=300, height= 25, font=("Sometype Mono Bold", 14), show = "*")
        self.senha_entry.place(relx=0.5, y=280, anchor = "center")

        self.c_senha_entry = ctk.CTkEntry(self.frame_esqueceu, placeholder_text="Confirme a nova senha", placeholder_text_color = "#9C00D4", fg_color=["#FDFDFD","#0D0D0D"], border_width = 2, border_color="#9C00D4", text_color= "#9C00D4", corner_radius= 100, width=300, height= 25, font=("Sometype Mono Bold", 14), show = "*")
        self.c_senha_entry.place(relx=0.5, y=337, anchor = "center")

        self.confirmar_button = ctk.CTkImage(light_image=Image.open("Imagens\\BotãodeConfirmar.png"), dark_image=Image.open("Imagens\\BotãodeConfirmar.png"), size=(148, 33.01))
        self.confirmar_button = ctk.CTkButton(self.frame_esqueceu, image= self.confirmar_button, text=None, width=1, height=1, fg_color=["#FDFDFD","#0D0D0D"], hover = None, command=self.troca_de_senha)
        self.confirmar_button.place(relx=0.5, y= 430, anchor = "center")  

        self.voltar_button = ctk.CTkButton(self.frame_esqueceu, text="VOLTAR", text_color= "#9C00D4", fg_color=["#FDFDFD","#0D0D0D"], width=1, height=1, hover = False, font=("Sometype Mono Bold", 10.21), command=back)
        self.voltar_button.place(relx=0.5, y= 480, anchor = "center")

        self.creditos = ctk.CTkLabel(self.frame_esqueceu, text="Development by ArthurVinxcius and isjustjefferson", text_color= "#9C00D4", font=("Sometype Mono Bold", 10.21)).place(relx = 0.5, y= 578.37, anchor = "center")

    def main_frame(self):
        cost = 0
        faturamento = 0
        lucro = faturamento-cost
        quantidade = ['0','1','2','3']

        def back():
            self.frame_principal.pack_forget()
            self.frame_login.pack(side = "right")
            self.limpa_entradas

        def selecao_de_produtos():
            faturamento=0
            if self.hamburguer.get()=="Krusty-Catupiry":
                self.preco_hamburguer=30
            elif self.hamburguer.get()=="Krusty-D_Cheddar":
                self.preco_hamburguer=30
            elif self.hamburguer.get()=="Krusty-tchola":
                self.preco_hamburguer=40
            self.hamburgueres=int(self.qtd_hamburguer.get())

            faturamento+=self.preco_hamburguer*self.hamburgueres

            if self.bebida.get()=="Coca":
                self.preco_bebida=10
            elif self.bebida.get()=="Fanta":
                self.preco_bebida=7
            elif self.bebida.get()=="Pepsi":
                self.preco_bebida=7
            self.bebidas=int(self.qtd_bebida.get())

            faturamento+=self.preco_bebida*self.bebidas

            if self.sobremesa.get()=="Picolé":
                self.preco_sobremesa=2
            elif self.sobremesa.get()=="Sorvete":
                self.preco_sobremesa=9
            elif self.sobremesa.get()=="Brownie":
                self.preco_sobremesa=10
            self.sobremesas=int(self.qtd_sobremesa.get())

            faturamento+=self.preco_sobremesa*self.sobremesas

            if self.fritas.get()=="c/Bacon":
                self.preco_frita=10
            elif self.fritas.get()=="c/Cheddar":
                self.preco_frita=10
            elif self.fritas.get()=="c/ketchup":
                self.preco_frita=10
            self.batatas_fritas=int(self.qtd_fritas.get())

            faturamento+=self.preco_frita*self.batatas_fritas

            self.hamburguer.set("Krusty-Catupiry")
            self.qtd_hamburguer.set(0)
            self.bebida.set("Coca")
            self.qtd_bebida.set(0)
            self.sobremesa.set("Picolé")
            self.qtd_sobremesa.set(0)
            self.fritas.set("c/Bacon")
            self.qtd_fritas.set(0)
            messagebox.showinfo(title="PRODUTOS", message=f"A compra foi de R${faturamento}")

        self.frame_login.pack_forget()

        self.frame_principal= ctk.CTkFrame(self, fg_color=["#FDFDFD","#0D0D0D"], corner_radius=0, width=800, height=600)
        self.frame_principal.pack(side = "top")

        self.perfil_imag = ctk.CTkImage(light_image=Image.open("Imagens\\logomarca.png"), dark_image=Image.open("Imagens\\logomarca.png"), size=(125, 125))
        self.perfil_imag = ctk.CTkLabel(self.frame_principal, bg_color=["#FDFDFD","#0D0D0D"], image=self.perfil_imag, text = None).place(relx= 0.5,y=100, anchor = "center")

        '''self.custo = ctk.CTkLabel(self.frame_principal, bg_color= ["#FDFDFD","#0D0D0D"], text= "CUSTO:", text_color= "#9C00D4", font=("Sometype Mono Bold", 20)). place(relx = 0.27, y=550, anchor = "center")
        self.custo_result = ctk.CTkLabel(self.frame_principal, bg_color= ["#FDFDFD","#0D0D0D"], text=str(cost), text_color= "#9C00D4", font=("Sometype Mono Bold", 20)).place(relx = 0.27, y=575, anchor = "center")

        self.faturamento= ctk.CTkLabel(self.frame_principal, bg_color= ["#FDFDFD","#0D0D0D"], text= "FATURAMENTO:", text_color= "#9C00D4", font=("Sometype Mono Bold", 20)). place(relx = 0.5, y=550, anchor = "center")
        self.faturamento_result= ctk.CTkLabel(self.frame_principal, bg_color= ["#FDFDFD","#0D0D0D"], text= str(faturamento), text_color= "#9C00D4", font=("Sometype Mono Bold", 20)). place(relx = 0.5, y=575, anchor = "center")

        self.lucro = ctk.CTkLabel(self.frame_principal, bg_color= ["#FDFDFD","#0D0D0D"], text= "LUCRO:", text_color= "#9C00D4", font=("Sometype Mono Bold", 20)). place(relx = 0.73, y=550, anchor = "center")
        self.lucro_result = ctk.CTkLabel(self.frame_principal, bg_color= ["#FDFDFD","#0D0D0D"], text=str(lucro), text_color= "#9C00D4", font=("Sometype Mono Bold", 20)). place(relx = 0.73, y=575, anchor = "center")

        self.cad_produto = ctk.CTkButton(self.frame_principal, bg_color= ["#FDFDFD","#0D0D0D"], fg_color= ["#FDFDFD","#0D0D0D"], text= "CADASTRAR PRODUTO", text_color= "#9C00D4", font=("Sometype Mono Bold", 13), width= 1, height= 1, hover= None).place(relx = 0.5, y = 485, anchor = "center")'''

        self.confirmar_compra = ctk.CTkImage(light_image=Image.open("Imagens\\BotãodeConfirmar.png"), dark_image=Image.open("Imagens\\BotãodeConfirmar.png"), size=(148, 33.01))
        self.confirmar_compra = ctk.CTkButton(self.frame_principal, image= self.confirmar_compra, text=None, width=1, height=1, fg_color=["#FDFDFD","#0D0D0D"], hover = None, command=selecao_de_produtos).place(relx = 0.5, y = 440, anchor = "center")

        self.voltar_button = ctk.CTkButton(self.frame_principal, text="VOLTAR", text_color= "#9C00D4", fg_color=["#FDFDFD","#0D0D0D"], width=1, height=1, hover = False, font=("Sometype Mono Bold", 15), command=back)
        self.voltar_button.place(x=10, y= 10)

        self.nome_hamburguer = ctk.CTkLabel(self.frame_principal, bg_color= ["#FDFDFD","#0D0D0D"], text= "HAMBÚRGUER:", text_color= "#9C00D4", font=("Sometype Mono Bold", 20)). place(relx = 0.27, y=225, anchor = "center")
        self.hamburguer=ctk.CTkComboBox(self.frame_principal, values=["Krusty-Catupiry", "Krusty-D_Cheddar", "Krusty-tchola"],border_color= "#9C00D4", button_color= "#9C00D4",fg_color= ["#FDFDFD","#0D0D0D"], bg_color= ["#FDFDFD","#0D0D0D"])
        self.hamburguer.place(relx = 0.5, y = 225, anchor = "center")
        self.qtd_hamburguer=ctk.CTkComboBox(self.frame_principal, values=quantidade,border_color= "#9C00D4", button_color= "#9C00D4",fg_color= ["#FDFDFD","#0D0D0D"], bg_color= ["#FDFDFD","#0D0D0D"])
        self.qtd_hamburguer.place(relx = 0.73, y = 225, anchor = "center")

        self.nome_bebida = ctk.CTkLabel(self.frame_principal, bg_color= ["#FDFDFD","#0D0D0D"], text= "BEBIDAS:", text_color= "#9C00D4", font=("Sometype Mono Bold", 20)). place(relx = 0.27, y=275, anchor = "center")
        self.bebida=ctk.CTkComboBox(self.frame_principal, values=["Coca", "Fanta", "Pepsi"],border_color= "#9C00D4", button_color= "#9C00D4",fg_color= ["#FDFDFD","#0D0D0D"], bg_color= ["#FDFDFD","#0D0D0D"])
        self.bebida.place(relx = 0.5, y = 275,anchor = "center")
        self.qtd_bebida=ctk.CTkComboBox(self.frame_principal, values=quantidade,border_color= "#9C00D4", button_color= "#9C00D4",fg_color= ["#FDFDFD","#0D0D0D"], bg_color= ["#FDFDFD","#0D0D0D"])
        self.qtd_bebida.place(relx = 0.73, y = 275, anchor = "center")
        
        self.nome_sobremesa = ctk.CTkLabel(self.frame_principal, bg_color= ["#FDFDFD","#0D0D0D"], text= "SOBREMESAS:", text_color= "#9C00D4", font=("Sometype Mono Bold", 20)). place(relx = 0.27, y=325, anchor ="center")
        self.sobremesa=ctk.CTkComboBox(self.frame_principal, values=["Picolé", "Sorvete", "Brownie"],border_color= "#9C00D4", button_color= "#9C00D4",fg_color= ["#FDFDFD","#0D0D0D"], bg_color= ["#FDFDFD","#0D0D0D"])
        self.sobremesa.place(relx = 0.5, y = 325, anchor = "center")
        self.qtd_sobremesa= ctk.CTkComboBox(self.frame_principal, values=quantidade,border_color= "#9C00D4", button_color= "#9C00D4",fg_color= ["#FDFDFD","#0D0D0D"], bg_color= ["#FDFDFD","#0D0D0D"])
        self.qtd_sobremesa.place(relx = 0.73, y = 325, anchor = "center")

        self.nome_fritas = ctk.CTkLabel(self.frame_principal, bg_color= ["#FDFDFD","#0D0D0D"], text= "FRITAS:", text_color= "#9C00D4", font=("Sometype Mono Bold", 20)). place(relx = 0.27, y=375, anchor = "center")
        self.fritas=ctk.CTkComboBox(self.frame_principal, values=["c/Bacon", "c/Cheddar", "c/ketchup"],border_color= "#9C00D4", button_color= "#9C00D4",fg_color= ["#FDFDFD","#0D0D0D"], bg_color= ["#FDFDFD","#0D0D0D"])
        self.fritas.place(relx= 0.5, y = 375, anchor = "center")
        self.qtd_fritas=ctk.CTkComboBox(self.frame_principal, values=quantidade,border_color= "#9C00D4", button_color= "#9C00D4",fg_color= ["#FDFDFD","#0D0D0D"], bg_color= ["#FDFDFD","#0D0D0D"])
        self.qtd_fritas.place(relx = 0.73, y = 375, anchor = "center")

    def limpa_entradas(self):
        
        self.email_entry.delete(0, END)
        self.user_entry.delete(0, END)
        self.senha_entry.delete(0, END)
        self.c_senha_entry.delete(0, END)
        
if __name__ == "__main__":    
    app = App()
    app.mainloop()