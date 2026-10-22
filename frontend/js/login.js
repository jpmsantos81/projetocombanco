const API = 'http://127.0.0.1:8000'
const formLogin = document.getElementById('form-login')
const mensagemLogin = document.getElementById('mensagem-login')
const botaoLogin = document.getElementById('botao-login')

formLogin.addEventListener('submit', async (evento) => {
  evento.preventDefault()
  mensagemLogin.classList.add('d-none')
  botaoLogin.disabled = true
  botaoLogin.textContent = 'Entrando...'

  const dados = {
    email: document.getElementById('email').value.trim(),
    senha: document.getElementById('senha').value
  }

  try {
    const resposta = await fetch(`${API}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(dados)
    })
    const resultado = await resposta.json()

    if (!resposta.ok) {
      mensagemLogin.textContent = resultado.erro || resultado.detail || 'Confira seu e-mail e senha.'
      mensagemLogin.className = 'alert alert-danger'
      return
    }

    localStorage.setItem('token', resultado.access_token)
    window.location.href = 'dashboard.html'
  } catch (erro) {
    mensagemLogin.textContent = 'Não foi possível conectar à API. Confirme que o servidor está rodando.'
    mensagemLogin.className = 'alert alert-danger'
  } finally {
    botaoLogin.disabled = false
    botaoLogin.textContent = 'Entrar'
  }
})
