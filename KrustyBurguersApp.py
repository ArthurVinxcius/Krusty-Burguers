#Krusty's App
import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.config_tela()
        self.login()

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
        self.login_label = ctk.CTkLabel(self.frame_login, text="Welcome to Krusty's App", text_color= "blue", font=("Arial", 20)).place(x=50, y=50)

        self.usuario_entry = ctk.CTkEntry(self.frame_login, placeholder_text="Usuario", width=250, height= 35, font=("Arial", 14)).place(x=40, y=150)

        self.usuario_label = ctk.CTkLabel(self.frame_login, text="*Campo obrigatório", height=0,text_color="blue", font=("Arial", 10)).place(x=45, y=188)

        self.senha_entry = ctk.CTkEntry(self.frame_login, placeholder_text="Senha", width=250, height= 35, font=("Arial", 14), show = "*").place(x=40, y=205)

        self.senha_label = ctk.CTkLabel(self.frame_login, text="*Campo obrigatório", height=0,text_color="blue", font=("Arial", 10)).place(x=45, y=243)

        self.lembrar_check = ctk.CTkCheckBox(self.frame_login, checkbox_width=20, checkbox_height=20, text="Lembrar de mim", font=("Arial", 14)).place(x=45, y=270)

        self.login_button = ctk.CTkButton(self.frame_login, text="Login", width=200, height=30, font=("Arial", 14)).place(x=65, y= 310)


    #tela de registro
        def cadastro():

            def back():
                #Remover frame de cadastro
                frame_cadastro.pack_forget()
                
                #Retornar para a tela de login
                self.frame_login.pack(side = "top", expand = True, fill = "y")   

            #removendo login frame
            self.frame_login.pack_forget()

            #cadastro frame
            frame_cadastro = ctk.CTkFrame(self, fg_color=["white","grey"], width=350, height=600)
            frame_cadastro.pack(side = "top", expand = True, fill = "y")
            
            cadastro_label = ctk.CTkLabel(frame_cadastro, text="Welcome to Krusty's App", text_color= "blue", font=("Arial", 20)).place(x=50, y=50)

            email_entry = ctk.CTkEntry(frame_cadastro, placeholder_text="Insira seu e-mail", width=250, height= 35, font=("Arial", 14)).place(x=40, y=150)

            email_label = ctk.CTkLabel(frame_cadastro, text="*Campo obrigatório", height=0,text_color="blue", font=("Arial", 10)).place(x=45, y=188)

            user_entry = ctk.CTkEntry(frame_cadastro, placeholder_text="Insira o nome da Empresa", width=250, height= 35, font=("Arial", 14)).place(x=40, y=205)

            user_label = ctk.CTkLabel(frame_cadastro, text="*Campo obrigatório", height=0,text_color="blue", font=("Arial", 10)).place(x=45, y=243)

            senha_entry = ctk.CTkEntry(frame_cadastro, placeholder_text="Senha", width=250, height= 35, font=("Arial", 14), show = "*").place(x=40, y=260)

            senha_label = ctk.CTkLabel(frame_cadastro, text="*Campo obrigatório", height=0,text_color="blue", font=("Arial", 10)).place(x=45, y=300)

            c_senha_entry = ctk.CTkEntry(frame_cadastro, placeholder_text="Digite novamente a senha", width=250, height= 35, font=("Arial", 14), show = "*").place(x=40, y=317)

            termo_de_uso = ctk.CTkCheckBox(frame_cadastro, checkbox_width=20, checkbox_height=20, text="Aceito os termos de uso", font=("Arial", 14)).place(x=45, y=370)

            confirmar_button = ctk.CTkButton(frame_cadastro, text="Confirmar", width=200, height=30, font=("Arial", 14)).place(x=65, y= 410)
    
            voltar_button = ctk.CTkButton(frame_cadastro, text="Voltar", width=150, height=25, font=("Arial", 14), command=back).place(x=90, y= 450)
            
        self.cadastro_button = ctk.CTkButton(self.frame_login, text="Cadastre-se", width=200, height=30, font=("Arial", 14), command = cadastro).place(x=65, y= 350)


if __name__ == "__main__":    
    app = App()
    app.mainloop()


#tela de "esqueceu sua senha?"

#validação de usuario

#validação de senha

#validação de email

#validação de CNPJ

#Tela de configurações

#Tela de informações

#Tela de cadastro de produtos

#Impressão de arquivo