
import { useState } from 'react'

const hoteis = [
  {
    id: 1,
    nome: 'Hotel Fazenda Sertão Verde',
    cidade: 'Quixadá',
    estado: 'Ceará',
    avaliacao: 9.2,
    categoria: 'Excelente',
    preco: 280,
    imagem: 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=900',
    descricao: 'Conforto, tranquilidade e uma bela vista da natureza.',
  },
  {
    id: 2,
    nome: 'Pousada Pedra dos Ventos',
    cidade: 'Quixadá',
    estado: 'Ceará',
    avaliacao: 8.8,
    categoria: 'Muito bom',
    preco: 190,
    imagem: 'https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=900',
    descricao: 'Uma experiência aconchegante para descansar.',
  },
  {
    id: 3,
    nome: 'Hotel Central Premium',
    cidade: 'Fortaleza',
    estado: 'Ceará',
    avaliacao: 9.5,
    categoria: 'Excepcional',
    preco: 350,
    imagem: 'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=900',
    descricao: 'Estrutura moderna e localização privilegiada.',
  },
]

export default function App() {
  const [destino, setDestino] = useState('')
  const [entrada, setEntrada] = useState('')
  const [saida, setSaida] = useState('')
  const [hospedes, setHospedes] = useState('2')
  const [precoMaximo, setPrecoMaximo] = useState('')
  const [avaliacaoMinima, setAvaliacaoMinima] = useState('')
  const [ordenacao, setOrdenacao] = useState('relevancia')

  const hoteisFiltrados = hoteis.filter((hotel) => {
    const correspondeDestino =
      `${hotel.nome} ${hotel.cidade} ${hotel.estado}`
        .toLowerCase()
        .includes(destino.toLowerCase())

    const correspondePreco =
      !precoMaximo || hotel.preco <= Number(precoMaximo)

    const correspondeAvaliacao =
      !avaliacaoMinima || hotel.avaliacao >= Number(avaliacaoMinima)

    return correspondeDestino && correspondePreco && correspondeAvaliacao
  })

  const hoteisOrdenados = [...hoteisFiltrados].sort((a, b) => {
    if (ordenacao === 'menor-preco') {
      return a.preco - b.preco
    }

    if (ordenacao === 'melhor-avaliacao') {
      return b.avaliacao - a.avaliacao
    }

    return 0
  })

  return (
    <div className="hotel-app">
      <nav className="hotel-navbar">
        <div className="hotel-container navbar-content">
          <a className="hotel-logo" href="#">
            <span className="logo-icon">H</span>
            hospeda<span>+</span>
          </a>

          <div className="navbar-links">
            <a href="#inicio">Início</a>
            <a href="#hoteis">Hospedagens</a>
            <a href="#sobre">Sobre</a>
          </div>

          <button className="login-button">Entrar</button>
        </div>
      </nav>

      <main>
        <section className="hero-section" id="inicio">
          <div className="hero-overlay"></div>

          <div className="hotel-container hero-content">
            <span className="hero-tag">SUA PRÓXIMA VIAGEM COMEÇA AQUI</span>

            <h1>
              Encontre o lugar
              <br />
              perfeito para <span>ficar.</span>
            </h1>

            <p>
              Compare hospedagens, descubra destinos e encontre
              a melhor opção para sua viagem.
            </p>

            <div className="search-panel">
              <div className="search-field destination-field">
                <label htmlFor="destino">DESTINO</label>
                <input
                  id="destino"
                  type="text"
                  placeholder="Para onde você vai?"
                  value={destino}
                  onChange={(e) => setDestino(e.target.value)}
                />
              </div>

              <div className="search-field">
                <label htmlFor="entrada">CHECK-IN</label>
                <input
                  id="entrada"
                  type="date"
                  lang="pt-BR"
                  value={entrada}
                  onChange={(e) => setEntrada(e.target.value)}
                />
              </div>

              <div className="search-field">
                <label htmlFor="saida">CHECK-OUT</label>
                <input
                  id="saida"
                  type="date"
                  lang="pt-BR"
                  value={saida}
                  onChange={(e) => setSaida(e.target.value)}
                  min={entrada || undefined}
                />
              </div>

              <div className="search-field guests-field">
                <label htmlFor="hospedes">HÓSPEDES</label>
                <select
                  id="hospedes"
                  value={hospedes}
                  onChange={(e) => setHospedes(e.target.value)}
                >
                  <option value="1">1 hóspede</option>
                  <option value="2">2 hóspedes</option>
                  <option value="3">3 hóspedes</option>
                  <option value="4">4 hóspedes</option>
                  <option value="5">5 hóspedes</option>
                </select>
              </div>

              <button
                className="search-button"
                onClick={() =>
                  document.getElementById('hoteis')?.scrollIntoView({
                    behavior: 'smooth',
                  })
                }
              >
                Buscar
              </button>
            </div>
          </div>
        </section>

        <section className="hotel-container results-section" id="hoteis">

        <div className="section-heading">
            <div>
              <span className="section-eyebrow">ENCONTRE SUA HOSPEDAGEM</span>
              <h2>Explore hospedagens</h2>
              <p>Compare opções e escolha a melhor para você.</p>
            </div>

            <div className="results-tools">
              <span className="results-count">
                {hoteisOrdenados.length} hospedagens encontradas
              </span>

              <select
                className="sort-select"
                value={ordenacao}
                onChange={(e) => setOrdenacao(e.target.value)}
                aria-label="Ordenar hospedagens"
              >
                <option value="relevancia">Mais relevantes</option>
                <option value="menor-preco">Menor preço</option>
                <option value="melhor-avaliacao">Melhor avaliação</option>
              </select>
            </div>
          </div>

          <div className="results-layout">
            <aside className="filters-panel">
              <h3>Filtros</h3>

              <label htmlFor="preco">Preço máximo por diária</label>
              <select
                id="preco"
                value={precoMaximo}
                onChange={(e) => setPrecoMaximo(e.target.value)}
              >
                <option value="">Qualquer preço</option>
                <option value="200">Até R$ 200</option>
                <option value="300">Até R$ 300</option>
                <option value="400">Até R$ 400</option>
              </select>

              <div className="filter-group">
                <label htmlFor="avaliacao">Avaliação mínima</label>

                <select
                  id="avaliacao"
                  value={avaliacaoMinima}
                  onChange={(e) => setAvaliacaoMinima(e.target.value)}
                >
                <option value="">Qualquer avaliação</option>
                <option value="7">7 ou mais</option>
                <option value="8">8 ou mais</option>
                <option value="9">9 ou mais</option>
                </select>
              </div>

              <button
                className="clear-filters"
                onClick={() => {
                  setDestino('')
                  setPrecoMaximo('')
                  setAvaliacaoMinima('')
                }}
              >
                Limpar filtros
              </button>
            </aside>

            <div className="hotel-list">
              {hoteisFiltrados.length > 0 ? (
                hoteisOrdenados.map((hotel) => (
                  <article className="hotel-card" key={hotel.id}>
                    <img
                      className="hotel-image"
                      src={hotel.imagem}
                      alt={hotel.nome}
                    />

                    <div className="hotel-information">
                      <span className="hotel-location">
                        {hotel.cidade}, {hotel.estado}
                      </span>

                      <h3>{hotel.nome}</h3>

                      <p>{hotel.descricao}</p>

                      <span className="hotel-rating">
                        ★ {hotel.avaliacao} · {hotel.categoria}
                      </span>
                    </div>

                    <div className="hotel-price">
                      <span>Diária a partir de</span>
                      <strong>
                        R$ {hotel.preco.toLocaleString('pt-BR')}
                      </strong>
                      <small>por noite</small>
                      <button
                        onClick={() =>
                          alert(`Você selecionou ${hotel.nome}`)
                        }
                      >
                        Ver hospedagem
                      </button>
                    </div>
                  </article>
                ))
              ) : (
                <div className="empty-results">
                  <h3>Nenhuma hospedagem encontrada</h3>
                  <p>Tente pesquisar outro destino ou alterar os filtros.</p>
                </div>
              )}
            </div>
          </div>
        </section>
      </main>

      <footer className="hotel-footer" id="sobre">
        <div className="hotel-container">
          <a className="hotel-logo" href="#">
            <span className="logo-icon">H</span>
            hospeda<span>+</span>
          </a>
          <p>Encontre sua próxima hospedagem com mais facilidade.</p>
          <small>Projeto acadêmico · Estágio II · 2026</small>
        </div>
      </footer>
    </div>
  )
}
