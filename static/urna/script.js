// Adiciona o número ao campo de resultado, limitando a no máximo 2 caracteres.
function insert(num) {
  var numero = document.getElementById('resultado').innerHTML;
  if (numero.length < 2) {
      document.getElementById('resultado').innerHTML = numero + num;
  }

  
  atualizarEstadoBotao();
  pesquisar()
}

// Define o voto como "Branco" e limpa informações de candidato.
function branco(voto) {
  var resultado = document.getElementById('resultado').innerHTML;
  document.getElementById('resultado').innerHTML = voto;
  document.getElementById('p-nome').innerHTML = '';
  document.getElementById('p-partido').innerHTML = '';

  atualizarEstadoBotao();
}

// Corrige o último caractere do resultado ou limpa completamente se for "VOTO EM BRANCO".
function corrige() {
  var resultadoElement = document.getElementById('resultado');
  var resultado = resultadoElement.textContent.trim();

  

  if (resultado === 'VOTO EM BRANCO') {
      resultadoElement.textContent = '';
      document.getElementById('p-nome').innerHTML = '';
      document.getElementById('p-partido').innerHTML = '';
  } else {
      resultadoElement.textContent = resultado.substring(0, resultado.length - 1);
      document.getElementById('p-nome').innerHTML = '';
      document.getElementById('p-partido').innerHTML = '';
  }

  atualizarEstadoBotao();
}

// Realiza uma pesquisa AJAX para obter informações do candidato com base no número do candidato.
function pesquisar() {
  var numeroCandidato = document.getElementById('resultado').innerHTML;
  var buscarCandidatoUrl = document.getElementById('resultado').dataset.buscarCandidatoUrl;
  var resultado = document.getElementById('resultado').textContent.trim();

  document.getElementById('p-nome').innerHTML = '';
  document.getElementById('p-partido').innerHTML = '';

  if (resultado.length === 2) {
    $.ajax({
      url: buscarCandidatoUrl,
      type: 'GET',
      data: { 'numeroCandidato': numeroCandidato },
      dataType: 'json',
      success: function (response) {
          document.getElementById('p-nome').innerHTML = response.nome;
          document.getElementById('p-partido').innerHTML = response.partido;
      },
      error: function (error) {
          console.log('Erro na requisição AJAX:', error);
      }
  });
  }

  

  atualizarEstadoBotao();
}

// Atualiza o estado do botão de confirmação com base no conteúdo do resultado.
function atualizarEstadoBotao() {
  var resultado = document.getElementById('resultado').textContent.trim();
  var botaoConfirmar = document.getElementById('botao-confirmar');

  if (resultado.length === 2 || resultado === 'VOTO EM BRANCO') {
      botaoConfirmar.removeAttribute('disabled');
  } else {
      botaoConfirmar.setAttribute('disabled', 'disabled');
  }
}

// Confirma o voto, define o número do candidato no campo oculto e envia o formulário.
function confirmar() {
  var resultado = document.getElementById('resultado').textContent.trim();

  document.getElementById('voto').value = resultado;

  document.querySelector('form').submit();
}

// Atualiza o estado do botão ao carregar o DOM.
document.addEventListener('DOMContentLoaded', function() {
  atualizarEstadoBotao();
});