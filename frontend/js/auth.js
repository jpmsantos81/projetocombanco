// ============================================================
// js/auth.js — Funções compartilhadas de autenticação
// Descrição: Protege páginas e envia o JWT nas chamadas à API.
// ============================================================

// Redireciona para o login se não houver token salvo
function protegerPagina() {
  const token = localStorage.getItem('token')
  if (!token) {
    window.location.href = 'login.html'
  }
}

// Envia o token junto com a requisição e encerra a sessão se ele expirou
async function fetchAutenticado(url, opcoes = {}) {
  const token = localStorage.getItem('token')
  const resposta = await fetch(url, {
    ...opcoes,
    headers: {
      ...(opcoes.headers || {}),
      Authorization: `Bearer ${token || ''}`
    }
  })

  if (resposta.status === 401) {
    localStorage.removeItem('token')
    window.location.href = 'login.html'
  }

  return resposta
}

// Apaga o token e encerra a sessão
function sair() {
  localStorage.removeItem('token')
  window.location.href = 'login.html'
}
