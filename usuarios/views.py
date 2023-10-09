from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib.auth import authenticate,login


def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    elif request.method == "POST":
        primeiro_nome = request.POST.get("primeiro_nome")
        ultimo_nome = request.POST.get("ultimo_nome")
        username = request.POST.get("username")
        senha = request.POST.get("senha")
        email = request.POST.get("email")
        confirmar_senha = request.POST.get("confirmar_senha")

        if not senha == confirmar_senha:
            messages.add_message(request, constants.ERROR, "As senhas não são iguais !")
            return redirect('/usuarios/cadastro')
        
        if len(senha) < 6:
            messages.add_message(request, constants.ERROR, "Sua senha deve conter mais de 6 caracteres !")
            return redirect('/usuarios/cadastro')
        
        # Verificar se o username já existe
        if User.objects.filter(username=username).exists():
            messages.add_message(request, constants.ERROR, "Username já existe !")
            return redirect('/usuarios/cadastro')
        
        if User.objects.filter(email=email).exists():
            messages.add_message(request, constants.ERROR, "Email ja cadastrado !")
            return redirect('/usuarios/cadastro')

        try:    
            user = User.objects.create_user(
            first_name = primeiro_nome,
            last_name = ultimo_nome, 
            username = username,
            email = email,
            password = senha)

        except:
            messages.add_message(request, constants.ERROR, "Não foi possivel realizar o cadastro. Contate o nosso suporte!")
            return redirect('/usuarios/cadastro')
        
        messages.add_message(request, constants.SUCCESS, "Cadastrado(a) com sucesso!")
        return render(request, 'login.html')
    
def logar(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        username = request.POST.get("username")
        senha = request.POST.get("senha")

        user = authenticate(username=username, password=senha)

        if user:
            """Logar"""
            login(request, user)
            return redirect('/exames/solicitar_exames/')
        else:
            """Não logar"""
            messages.add_message(request, constants.ERROR, "Username ou Senha invalidos!")
            return redirect('/usuarios/login')
