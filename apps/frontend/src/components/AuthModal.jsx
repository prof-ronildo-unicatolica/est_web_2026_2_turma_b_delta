import { useEffect, useState } from 'react'

const initialForm = { nome: '', email: '', senha: '' }

export default function AuthModal({
  mode,
  account,
  error,
  message,
  onClose,
  onLogout,
  onModeChange,
  onSubmit,
}) {
  const [form, setForm] = useState(initialForm)
  const [submitting, setSubmitting] = useState(false)
  const isRegister = mode === 'register'
  const isProfile = mode === 'profile'

  useEffect(() => {
    setForm(initialForm)
  }, [mode])

  async function handleSubmit(event) {
    event.preventDefault()
    setSubmitting(true)
    const accepted = await onSubmit(form)
    if (accepted) {
      setForm((previous) => ({ ...previous, senha: '' }))
    }
    setSubmitting(false)
  }

  function update(field, value) {
    setForm((previous) => ({ ...previous, [field]: value }))
  }

  return (
    <div
      className="auth-backdrop"
      onMouseDown={(event) => {
        if (event.target === event.currentTarget) onClose()
      }}
    >
      <section
        className="auth-dialog"
        role="dialog"
        aria-modal="true"
        aria-labelledby="auth-title"
      >
        <button
          className="auth-close"
          type="button"
          onClick={onClose}
          aria-label="Fechar"
        >
          ×
        </button>

        {isProfile ? (
          <>
            <p className="auth-eyebrow">Conta conectada</p>
            <h2 id="auth-title">Seu perfil</h2>
            <p className="auth-profile-name">{account?.nome}</p>
            <p className="text-secondary mb-2">{account?.email}</p>
            <span className="badge text-bg-primary mb-4">
              {account?.is_admin ? 'Administrador' : 'Hóspede'}
            </span>
            <div className="d-flex justify-content-between">
              <button className="btn btn-outline-secondary" type="button" onClick={onClose}>
                Fechar
              </button>
              <button className="btn btn-danger" type="button" onClick={onLogout}>
                Sair da conta
              </button>
            </div>
          </>
        ) : (
          <>
            <p className="auth-eyebrow">Sistema de Reservas</p>
            <h2 id="auth-title">{isRegister ? 'Criar conta' : 'Entrar'}</h2>
            <p className="text-secondary mb-4">
              {isRegister
                ? 'Cadastre-se para acessar sua conta.'
                : 'Acesse sua conta de hóspede ou administrador.'}
            </p>

            {message && <div className="alert alert-success" role="status">{message}</div>}
            {error && <div className="alert alert-danger" role="alert">{error}</div>}

            <form onSubmit={handleSubmit}>
              {isRegister && (
                <div className="mb-3">
                  <label className="form-label" htmlFor="auth-name">Nome</label>
                  <input
                    autoComplete="name"
                    className="form-control"
                    id="auth-name"
                    maxLength={100}
                    minLength={1}
                    onChange={(event) => update('nome', event.target.value)}
                    required
                    value={form.nome}
                  />
                </div>
              )}
              <div className="mb-3">
                <label className="form-label" htmlFor="auth-email">E-mail</label>
                <input
                  autoComplete="email"
                  className="form-control"
                  id="auth-email"
                  maxLength={100}
                  onChange={(event) => update('email', event.target.value)}
                  required
                  type="email"
                  value={form.email}
                />
              </div>
              <div className="mb-4">
                <label className="form-label" htmlFor="auth-password">Senha</label>
                <input
                  autoComplete={isRegister ? 'new-password' : 'current-password'}
                  className="form-control"
                  id="auth-password"
                  minLength={isRegister ? 8 : 1}
                  onChange={(event) => update('senha', event.target.value)}
                  required
                  type="password"
                  value={form.senha}
                />
                {isRegister && (
                  <small className="form-text">
                    Mínimo de 8 caracteres; máximo de 72 bytes em UTF-8.
                  </small>
                )}
              </div>
              <button
                className="btn btn-primary w-100"
                disabled={submitting}
                type="submit"
              >
                {submitting
                  ? 'Aguarde…'
                  : isRegister
                    ? 'Criar conta'
                    : 'Entrar'}
              </button>
            </form>

            <p className="text-center mt-4 mb-0">
              {isRegister ? 'Já tem conta?' : 'Ainda não tem conta?'}{' '}
              <button
                className="auth-link"
                type="button"
                onClick={() => onModeChange(isRegister ? 'login' : 'register')}
              >
                {isRegister ? 'Entrar' : 'Criar conta'}
              </button>
            </p>
          </>
        )}
      </section>
    </div>
  )
}
