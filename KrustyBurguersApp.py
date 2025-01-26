#Krusty's App
import customtkinter as ctk

#tela de login
login = ctk.CTk()
login.geometry("800x600")

#login frames
frame = ctk.CTkFrame(login, fg_color=["white","grey"], width=350, height=600)
frame.pack(side = "top", expand = True, fill = "y") #expand e fill trazem responsividade para o frame

#login frames widgets
login_label = ctk.CTkLabel(frame, text="Welcome to Krusty's App", text_color= "blue", font=("Arial", 20)).place(x=50, y=50)

usuario_entry = ctk.CTkEntry(frame, placeholder_text="Usuario", width=250, height= 35, font=("Arial", 14)).place(x=40, y=150)

usuario_label = ctk.CTkLabel(frame, text="*Campo obrigatório", height=0,text_color="blue", font=("Arial", 10)).place(x=45, y=188)

senha_entry = ctk.CTkEntry(frame, placeholder_text="Senha", width=250, height= 35, font=("Arial", 14), show = "*").place(x=40, y=205)

senha_label = ctk.CTkLabel(frame, text="*Campo obrigatório", height=0,text_color="blue", font=("Arial", 10)).place(x=45, y=243)

lembrar_check = ctk.CTkCheckBox(frame, checkbox_width=20, checkbox_height=20, text="Lembrar de mim", font=("Arial", 14)).place(x=45, y=270)

login_button = ctk.CTkButton(frame, text="Login", width=200, height=30, font=("Arial", 14)).place(x=65, y= 310)

Cadastro_button = ctk.CTkButton(frame, text="Cadastre-se", width=200, height=30, font=("Arial", 14)).place(x=65, y= 350)

#tela de registro

#tela de "esqueceu sua senha?"

#validação de usuario

#validação de senha

#validação de email

#validação de CNPJ

#Tela de configurações

#Tela de informações

#Tela de cadastro de produtos

#Impressão de arquivo


#inicialização do app
app = login
app.title("Krusty's App")
app.mainloop()