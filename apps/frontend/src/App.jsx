import { useEffect, useState } from 'react'
import AuthModal from './components/AuthModal'
import ProfessorProfile from './components/ProfessorProfile'
import DisciplinasList from './components/DisciplinasList'
import StacksTable from './components/StacksTable'
import ImageAndCarousel from './components/ImageAndCarousel'
import Sidebar from './components/Sidebar'
import VideoComponent from './components/VideoComponent'
import InteractiveExamples from './components/InteractiveExamples'
import HoteisRaw from './components/HoteisRaw'

const API_BASE = import.meta.env.VITE_API_BASE_URL || '/api/v1'
const TOKEN_KEY = 'reservas_access_token'

export default function App() {
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(true)
  const [account, setAccount] = useState(null)
  const [checkingSession, setCheckingSession] = useState(true)
  const [authMode, setAuthMode] = useState(null)
  const [authError, setAuthError] = useState('')
  const [authMessage, setAuthMessage] = useState('')

  useEffect(() => {
    fetch(`${API_BASE}/sobre`)
      .then((res) => {
        if (!res.ok) {
          throw new Error('Falha ao se conectar com a API')
        }
        return res.json()
      })
      .then((json) => {
        setData(json)
        setLoading(false)
      })
      .catch((err) => {
        setError(err.message)
        setLoading(false)
      })
  }, [])

  useEffect(() => {
    const token = sessionStorage.getItem(TOKEN_KEY)
    if (!token) {
      setCheckingSession(false)
      return
    }

    fetch(`${API_BASE}/auth/me`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((response) => {
        if (response.status === 401) {
          sessionStorage.removeItem(TOKEN_KEY)
          return null
        }
        if (!response.ok) {
          throw new Error('Não foi possível verificar a sessão')
        }
        return response.json()
      })
      .then((profile) => {
        if (profile) setAccount(profile)
      })
      .catch(() => {
        setAccount(null)
      })
      .finally(() => setCheckingSession(false))
  }, [])

  function abrirAutenticacao(mode) {
    setAuthError('')
    setAuthMessage('')
    setAuthMode(mode)
  }

  function sair() {
    sessionStorage.removeItem(TOKEN_KEY)
    setAccount(null)
    setAuthMode(null)
    setAuthError('')
    setAuthMessage('')
  }

  async function enviarAutenticacao(form) {
    setAuthError('')
    setAuthMessage('')
    const isRegister = authMode === 'register'
    try {
      const response = await fetch(
        `${API_BASE}/auth/${isRegister ? 'register' : 'login'}`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(
            isRegister
              ? { nome: form.nome, email: form.email, senha: form.senha }
              : { email: form.email, senha: form.senha },
          ),
        },
      )

      if (isRegister) {
        if (!response.ok) {
          setAuthError(
            'Confira o nome, o e-mail e a senha (mínimo 8 caracteres e até 72 bytes).',
          )
          return false
        }
        const result = await response.json()
        setAuthMessage(result.message)
        setAuthMode('login')
        return true
      }

      if (!response.ok) {
        setAuthError('E-mail ou senha inválidos.')
        return false
      }
      const result = await response.json()
      const profileResponse = await fetch(`${API_BASE}/auth/me`, {
        headers: { Authorization: `Bearer ${result.access_token}` },
      })
      if (!profileResponse.ok) {
        setAuthError('Não foi possível iniciar a sessão. Tente novamente.')
        return false
      }
      const profile = await profileResponse.json()
      sessionStorage.setItem(TOKEN_KEY, result.access_token)
      setAccount(profile)
      setAuthMode(null)
      return true
    } catch {
      setAuthError('Não foi possível conectar ao serviço de autenticação.')
      return false
    }
  }

  return (
    <div className="bg-light min-vh-100 pb-5">
      {/* Navbar de Exemplo */}
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm mb-4 sticky-top">
        <div className="container">
          <a className="navbar-brand d-flex align-items-center" href="#">
            <span className="fs-4 fw-bold text-primary">Rede Hoteleira</span>
            <span className="ms-2 badge bg-secondary text-wrap small">Estágio II</span>
          </a>
          <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarNav">
            <ul className="navbar-nav me-auto">
              <li className="nav-item">
                <a className="nav-link active" href="#">Home</a>
              </li>
              <li className="nav-item">
                <a className="nav-link" href="#tutorial-components">Tutorial</a>
              </li>
            </ul>
            <div className="d-flex align-items-center gap-2">
              {account ? (
                <>
                  <span className="badge text-bg-secondary">
                    {account.is_admin ? 'Administrador' : 'Hóspede'}
                  </span>
                  <button
                    className="btn btn-outline-primary btn-sm px-3"
                    type="button"
                    onClick={() => abrirAutenticacao('profile')}
                  >
                    Perfil
                  </button>
                  <button
                    className="btn btn-primary btn-sm px-3"
                    type="button"
                    onClick={sair}
                  >
                    Sair
                  </button>
                </>
              ) : (
                <>
                  <button
                    className="btn btn-outline-primary btn-sm px-3"
                    type="button"
                    onClick={() => abrirAutenticacao('login')}
                    disabled={checkingSession}
                  >
                    Entrar
                  </button>
                  <button
                    className="btn btn-primary btn-sm px-3"
                    type="button"
                    onClick={() => abrirAutenticacao('register')}
                    disabled={checkingSession}
                  >
                    Criar conta
                  </button>
                </>
              )}
            </div>
          </div>
        </div>
      </nav>

      {/* Cabecalho Principal */}
      <div className="container">
        <header className="mb-5 p-4 bg-white rounded shadow-sm">
          <div className="row align-items-center">
            <div className="col-md-8">
              <h1 className="display-5 text-primary fw-bold">Sistemas de Informação - Estágio II</h1>
              <p className="lead text-secondary mb-0">Projeto Monorepo Base (Boilerplate de Inicialização)</p>
            </div>
            <div className="col-md-4 text-md-end mt-3 mt-md-0">
              <div className="d-flex justify-content-md-end gap-2">
                <button className="btn btn-sm btn-outline-secondary" onClick={() => window.location.reload()}>
                  Recarregar Dados
                </button>
              </div>
            </div>
          </div>
          <hr className="my-4" />
          <div className="row g-3">
            <div className="col-md-3 col-sm-6">
              <strong>Equipe:</strong> <span className="text-secondary ms-1">{data?.equipe || 'Alpha'}</span>
            </div>
            <div className="col-md-3 col-sm-6">
              <strong>Professor:</strong> <span className="text-secondary ms-1">{data?.professor?.nome || 'Ronildo Silva'}</span>
            </div>
            <div className="col-md-3 col-sm-6">
              <strong>Ano:</strong> <span className="text-secondary ms-1">{data?.ano || '2026'}</span>
            </div>
            <div className="col-md-3 col-sm-6">
              <strong>Semestre:</strong> <span className="text-secondary ms-1">{data?.semestre || '2'}</span>
            </div>
          </div>
        </header>

        {loading && (
          <div className="text-center my-5 py-5">
            <div className="spinner-border text-primary" role="status">
              <span className="visually-hidden">Carregando dados da API...</span>
            </div>
            <p className="mt-3 text-secondary">Buscando informações do servidor backend...</p>
          </div>
        )}

        {error && (
          <div className="alert alert-danger shadow-sm p-4" role="alert">
            <h4 className="alert-heading fw-bold">Erro de Conexão com o Backend!</h4>
            <p>Não foi possível obter os dados da API em <code>{API_BASE}/sobre</code>.</p>
            <p className="mb-0">Verifique se o backend está rodando e se os bancos de dados foram inicializados com sucesso.</p>
            <hr />
            <p className="mb-0 small text-muted">Detalhe do erro: {error}</p>
          </div>
        )}

        {!loading && !error && data && (
          <div className="row g-4">
            {/* Sidebar Lateral */}
            <div className="col-md-3">
              <Sidebar />
            </div>

            {/* Conteúdo Principal */}
            <div className="col-md-9" id="tutorial-components">
              <ProfessorProfile professor={data.professor} />
              <DisciplinasList disciplinas={data.disciplinas} />
              <StacksTable stacks={data.stacks} />
              <ImageAndCarousel />
              <VideoComponent />
              <InteractiveExamples />
              <HoteisRaw />
            </div>
          </div>
        )}

        <footer className="mt-5 py-4 border-top text-center text-muted">
          <p className="mb-0">&copy; {new Date().getFullYear()} - Disciplina de Estágio II. Desenvolvido pela Equipe {data?.equipe || 'Alpha'}.</p>
        </footer>
      </div>
      {authMode && (
        <AuthModal
          mode={authMode}
          account={account}
          error={authError}
          message={authMessage}
          onClose={() => setAuthMode(null)}
          onLogout={sair}
          onModeChange={abrirAutenticacao}
          onSubmit={enviarAutenticacao}
        />
      )}
    </div>
  )
}
