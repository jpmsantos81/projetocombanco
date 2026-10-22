const API = 'http://127.0.0.1:8000'
const formCadastro = document.getElementById('form-cadastro')
const mensagemCadastro = document.getElementById('mensagem-cadastro')
const botaoCadastro = document.getElementById('botao-cadastro')

function mostrarMensagemCadastro(texto, tipo) {
  mensagemCadastro.textContent = texto
  mensagemCadastro.className = `alert alert-${tipo}`
}

formCadastro.addEventListener('submit', async (evento) => {
  evento.preventDefault()
  mensagemCadastro.classList.add('d-none')
  botaoCadastro.disabled = true
  botaoCadastro.textContent = 'Cadastrando...'

  const usuario = {
    nome: document.getElementById('nome').value.trim(),
    email: document.getElementById('email').value.trim(),
    senha: document.getElementById('senha').value
  }

  try {
    const resposta = await fetch(`${API}/usuarios`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(usuario)
    })
    const resultado = await resposta.json()

    if (!resposta.ok) {
      const detalhe = typeof resultado.detail === 'string'
        ? resultado.detail
        : resultado.erro || 'Confira os dados e tente novamente.'
      mostrarMensagemCadastro(`Não foi possível cadastrar: ${detalhe}`, 'danger')
      return
    }

    mostrarMensagemCadastro('Cadastro realizado com sucesso. Voltando para o início...', 'success')
    formCadastro.reset()
    window.setTimeout(() => {
      window.location.href = 'index.html'
    }, 1200)
  } catch (erro) {
    mostrarMensagemCadastro(
      'Não foi possível conectar à API. Confirme que o servidor está rodando e tente novamente.',
      'danger'
    )
  } finally {
    botaoCadastro.disabled = false
    botaoCadastro.textContent = 'Cadastrar'
  }
})
