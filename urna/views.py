from django.shortcuts import render
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.http import JsonResponse

from .models import Candidato, Eleitor

# View UrnaHome

class UrnaHomeView(View):
    def get(self, request):
        numeroCandidatos = Candidato.objects.count()
        return render(request, "urna/urna_home.html", {"candidatos": numeroCandidatos})

# Views de candidatos

class CandidatoListView(ListView):
    template_name = 'urna/candidato/candidato_list.html'
    model = Candidato
    
class CandidatoCreateView(CreateView):
    template_name = 'urna/candidato/candidato_form.html'
    model = Candidato
    fields = ["numero", "nome", "partido"]
    success_url = reverse_lazy("candidato_list")

class CandidatoUpdateView(UpdateView):
    template_name = 'urna/candidato/candidato_form.html'
    model = Candidato
    fields = ["numero", "nome", "partido"]
    success_url = reverse_lazy("candidato_list")
    
class CandidatoDeleteView(DeleteView):
    template_name = 'urna/candidato/candidato_confirm_delete.html'
    model = Candidato
    success_url = reverse_lazy("candidato_list")
    
# Views de eleitores

class EleitorListView(ListView):
    template_name = 'urna/eleitor/eleitor_list.html'
    model = Eleitor
    
class EleitorCreateView(CreateView):
    template_name = 'urna/eleitor/eleitor_form.html'
    model = Eleitor
    fields = ["tituloEleitor", "nome"]
    success_url = reverse_lazy("eleitor_list")
    
class EleitorDeleteView(DeleteView):
    template_name = 'urna/eleitor/eleitor_confirm_delete.html'
    model = Eleitor
    success_url = reverse_lazy("eleitor_list")
    
# Views de votação

# View para consultar titulo de eleitor
class SecaoEleitoralView(View):
    def get(self, request):
        
        
        return render(request, "urna/votacao/secao_eleitoral.html")

    def post(self, request, *args, **kwargs):
        tituloEleitor = request.POST.get('tituloEleitor')
        
        if tituloEleitor:
            
            # Caso o eleitor exista
            try:
                eleitor = Eleitor.objects.get(tituloEleitor=tituloEleitor)
                # Verifica se o eleitor já votou, caso sim renderiza para página de voto registrado
                if eleitor.voto:
                    return render(request, "urna/votacao/voto_registrado.html", {"eleitor": eleitor, "votoEleitor": True})
                else:
                    # Caso o eleitor não tenha votado ele redireciona para rota de votação enviando o titulo como query
                    return redirect("votacao", tituloEleitor=eleitor.tituloEleitor)
            # Caso eleitor não esteja cadastrado ele redireciona para página de eleitor 404
            except Eleitor.DoesNotExist:
                return render(
                    request, "urna/eleitor/eleitor_404.html", {"eleitor": tituloEleitor}
                )

        return render(request, "urna/votacao/secao_eleitoral.html")

# View de votação
class VotacaoView(View):
    def get(self, request, tituloEleitor):
        
        try:
            eleitor = Eleitor.objects.get(tituloEleitor=tituloEleitor)
            # Verifica se o eleitor recibido como query existe
            if eleitor:
                # Verifica se o eleitor já votou, caso sim renderiza para página de voto registrado
                if eleitor.voto:
                    return render(request, "urna/votacao/voto_registrado.html", {"eleitor": eleitor, "votoEleitor": True})
                # Caso não, é armazenado o título do eleitor na sessão do usuário e renderizado a página de votação
                else:
                    request.session['eleitor'] = eleitor.tituloEleitor
                    return render(request, "urna/votacao/votacao.html")
        # Caso eleitor não esteja cadastrado ele redireciona para página de eleitor 404
        except Eleitor.DoesNotExist:
            return render(
                request, "urna/eleitor/eleitor_404.html", {"eleitor": tituloEleitor}
            )
            
            
    def post(self, request, tituloEleitor):
        voto = request.POST.get('voto') # Recebe o voto do formulario hidden da votação
        tituloEleitor = request.session.get('eleitor', None) # Recebo o titulo de eleitor da sessão do usuário
        
        # Caso exista os dados necessários
        if (voto, tituloEleitor):
            try:
                eleitor = Eleitor.objects.get(tituloEleitor=tituloEleitor)

                # Se o voto for branco é adicionado o voto ao eleitor
                if voto == 'VOTO EM BRANCO':
                    eleitor.adicionarVoto("Branco")
                else:
                    # Se existir um candidato com o número existente é adicionado o voto para o Candidato e o número ao voto do eleitor
                    try:
                        candidato = Candidato.objects.get(numero=voto)
                        candidato.adicionarVoto()
                        eleitor.adicionarVoto(candidato.numero)
                    # Caso não exista, o voto é considerado nulo, e é adicionado ao eleitor
                    except Candidato.DoesNotExist:
                        eleitor.adicionarVoto("Nulo")
                        
                # Ao final da votação é renderizada uma página de voto registrado
                return render(
                    request, "urna/votacao/voto_registrado.html", {"eleitor": eleitor}
                )
                
            # Caso eleitor não esteja cadastrado ele redireciona para página de eleitor 404
            except Eleitor.DoesNotExist:
                return render(
                    request, "urna/eleitor/eleitor_404.html", {"eleitor": tituloEleitor}
                )
                
        return render(request, "urna/votacao/votacao.html")

# View para buscar candidato a partir do template votação    
class BuscarCandidatoView(View):
    def get(self, request):
        # Obtém o número do candidato da solicitação GET
        numero_candidato = request.GET.get('numeroCandidato')

        try:
            # Tenta encontrar um candidato com o número fornecido
            candidato = Candidato.objects.get(numero=numero_candidato)
            
            # Se encontrado, cria um dicionário com os detalhes do candidato
            detalhes_candidato = {'nome': candidato.nome, 'partido': candidato.partido}
        except Candidato.DoesNotExist:
            # Se o candidato não for encontrado, define detalhes vazios
            detalhes_candidato = {'nome': '', 'partido': ''}

        # Retorna os detalhes do candidato como uma resposta JSON
        return JsonResponse(detalhes_candidato)
    
# View para apresentar o relatório da votação
class ResultadoVotacaoView(View):
    def get(self, request):
        candidatos = Candidato.objects.all()
        eleitores = Eleitor.objects.all()
        eleitoresApts = f"{len(eleitores):04d}"
        votoNominais = 0
        totalVotos = 0
        totalNulos = 0
        totalBrancos = 0
        
        for eleitor in eleitores:
            if eleitor.voto != "Nulo" and eleitor.voto != "Branco" and eleitor.voto is not None and eleitor.voto != "":
                votoNominais += 1
                
            if eleitor.voto:
                totalVotos += 1
            
            if eleitor.voto == "Nulo":
                totalNulos += 1
            elif eleitor.voto == "Branco":
                totalBrancos += 1
            
        
        return render(
            request, 
            "urna/votacao/resultado_votacao.html", 
            {
                "candidatos": candidatos, 
                "eleitores": eleitores, 
                "eleitoresApts": eleitoresApts,
                "votosNominais": votoNominais,
                "totalNulos": totalNulos,
                "totalBrancos": totalBrancos,
                "totalVotos": totalVotos,
                
            }
        )
        