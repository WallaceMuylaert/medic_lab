from django.conf import settings
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import TiposExames,PedidosExames,SolicitacaoExame
from datetime import datetime
from django.contrib import messages
from django.contrib.messages import constants
import os


@login_required
def solicitar_exames(request):
    tipos_exames = TiposExames.objects.all()
    if request.method == "GET":
        return render(request, 'solicitar_exames.html', {'tipos_exames': tipos_exames})
    else:
        exames_id = request.POST.getlist('exames')
        solicitacao_exames = TiposExames.objects.filter(id__in=exames_id)
        #preco_total = solicitacao_exames.aggregate(total=Sum('preco'))['total']

        preco_total = 0
        for exame in solicitacao_exames:
            if exame.disponivel:
                preco_total += exame.preco
        
        data = datetime.now()
        data_formatada = data.strftime('%d/%m/%Y')

        return render(request, 'solicitar_exames.html', {'solicitacao_exames': solicitacao_exames, 'preco_total': preco_total, 'tipos_exames': tipos_exames,'data':data_formatada})

@login_required
def fechar_pedido(request):
    #print(request.POST)
    exames_id = request.POST.getlist('exames')
    #print(exames_id)
    solicitacao_exames = TiposExames.objects.filter(id__in=exames_id)

    pedido_exame = PedidosExames(
        usuario = request.user,
        data = datetime.now()
    )

    pedido_exame.save()

    for exame in solicitacao_exames:
        solicitacao_exames_temp = SolicitacaoExame(
            usuario = request.user,
            exame = exame,
            status = "E"
        )
        solicitacao_exames_temp.save()
        pedido_exame.exames.add(solicitacao_exames_temp)
        
    pedido_exame.save()

    messages.add_message(request, constants.SUCCESS, 'Pedido de exame concluído com sucesso')
    return redirect('/exames/gerenciar_pedidos/')

@login_required
def gerenciar_pedidos(request):
    pedidos_exames = PedidosExames.objects.filter(usuario=request.user)
    return render(request, 'gerenciar_pedidos.html', {'pedidos_exames':pedidos_exames})

@login_required
def cancelar_pedido(request, pedido_id):
    pedido = PedidosExames.objects.get(id=pedido_id)

    if not pedido.usuario == request.user:
        messages.add_message(request, constants.ERROR, 'Esse pedido não é seu')
        return redirect('/exames/gerenciar_pedidos/')

    pedido.agendado = False
    pedido.save()
    messages.add_message(request, constants.SUCCESS, 'Pedido excluído com sucesso')
    return redirect('/exames/gerenciar_pedidos/')

@login_required
def gerenciar_exames(request):
    exames = SolicitacaoExame.objects.filter(usuario=request.user)
    return render(request, 'gerenciar_exames.html', {'exames':exames})

@login_required
def permitir_abrir_exame(request, exame_id):
    exame = SolicitacaoExame.objects.get(id=exame_id)
	
    #validar se o exame é do usuário
    if exame.usuario != request.user:
        messages.add_message(request, constants.ERROR, "Você não tem permissão para acessar este exame.")
        return redirect('/exames/gerenciar_exames/')

    if not exame.requer_senha:
        # verificar se o pdf existe
        return redirect(exame.resultado.url)

    else: 
        return redirect(f'/exames/solicitar_senha_exame/{exame.id}')

@login_required
def solicitar_senha_exame(request, exame_id):
    exame = SolicitacaoExame.objects.get(id=exame_id)
    if request.method == "GET":
        return render(request, 'solicitar_senha_exame.html', {'exame': exame})
    elif request.method == "POST":
        senha = request.POST.get("senha")

		#Validar se o exame é do usuário
        if exame.usuario != request.user:
            messages.add_message(request, constants.ERROR, "Você não tem permissão para acessar este exame.")
            return redirect('/exames/gerenciar_exames/')
        
        if senha == exame.senha:
            return redirect(exame.resultado.url)
        else:
            messages.add_message(request, constants.ERROR, 'Senha inválida')
            return redirect(f'/exames/solicitar_senha_exame/{exame.id}')