import { useState } from 'react';

export default function InteractiveExamples() {
  // Dropdown states
  const [selectedTopic, setSelectedTopic] = useState('react');
  
  // Rating states
  const [rating, setRating] = useState(0);
  const [hoverRating, setHoverRating] = useState(0);
  const [submittedRating, setSubmittedRating] = useState(false);

  // Date picker states
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');

  // Cities from seed (geojson coordinates: [longitude, latitude])
  const cities = [
    { name: 'Fortaleza - CE', coords: [-38.5267, -3.7319] },
    { name: 'Quixadá - CE', coords: [-39.0152, -4.9715] },
    { name: 'Crateús - CE', coords: [-40.6728, -5.1764] },
    { name: 'Cedro - CE', coords: [-39.0625, -6.6074] },
    { name: 'Belo Horizonte - MG', coords: [-43.9378, -19.9191] },
    { name: 'São Paulo - SP', coords: [-46.6333, -23.5505] },
    { name: 'Rio de Janeiro - RJ', coords: [-43.1729, -22.9068] },
    { name: 'Florianópolis - SC', coords: [-48.5480, -27.5954] },
    { name: 'Lisboa - PT', coords: [-9.1393, 38.7223] }
  ];

  const [cityA, setCityA] = useState('Fortaleza - CE');
  const [cityB, setCityB] = useState('Quixadá - CE');

  const topics = {
    react: {
      title: 'React & Vite',
      desc: 'Biblioteca para construção de interfaces SPA (Single Page Applications) ultra rápidas e com carregamento instantâneo via Vite.',
      badge: 'Frontend',
      color: 'info'
    },
    fastapi: {
      title: 'FastAPI',
      desc: 'Framework Python moderno e assíncrono para construção de APIs eficientes de alta performance baseadas em Pydantic e OpenAPI.',
      badge: 'Backend',
      color: 'success'
    },
    docker: {
      title: 'Docker & Compose',
      desc: 'Tecnologia de conteinerização que isola os serviços de banco, fila, backend e frontend para facilitar o desenvolvimento local homogêneo.',
      badge: 'DevOps',
      color: 'primary'
    }
  };

  const ratingFeedbacks = {
    0: 'Escolha uma nota clicando nas estrelas',
    1: '⭐ - Ruim (Precisa melhorar muito)',
    2: '⭐⭐ - Regular (Apenas aceitável)',
    3: '⭐⭐⭐ - Bom (Atende às expectativas)',
    4: '⭐⭐⭐⭐ - Muito Bom (Superou as expectativas)',
    5: '⭐⭐⭐⭐⭐ - Excelente! (Perfeito, sem ressalvas)'
  };

  const handleRatingSubmit = (e) => {
    e.preventDefault();
    if (rating === 0) return;
    setSubmittedRating(true);
    setTimeout(() => {
      setSubmittedRating(false);
    }, 4000);
  };

  // Calculates difference in days
  const calculateDays = () => {
    if (!startDate || !endDate) return null;
    const start = new Date(startDate);
    const end = new Date(endDate);
    const timeDiff = end.getTime() - start.getTime();
    const daysDiff = Math.ceil(timeDiff / (1000 * 3600 * 24));
    return isNaN(daysDiff) ? null : daysDiff;
  };

  // Calculates distance in km between selected cities (Haversine formula)
  const calculateDistance = () => {
    const fromCity = cities.find(c => c.name === cityA);
    const toCity = cities.find(c => c.name === cityB);
    if (!fromCity || !toCity) return 0;
    if (cityA === cityB) return 0;

    const toRad = (value) => (value * Math.PI) / 180;
    const [lon1, lat1] = fromCity.coords;
    const [lon2, lat2] = toCity.coords;

    const R = 6371; // Earth radius in km
    const dLat = toRad(lat2 - lat1);
    const dLon = toRad(lon2 - lon1);
    const a =
      Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos(toRad(lat1)) *
        Math.cos(toRad(lat2)) *
        Math.sin(dLon / 2) *
        Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return Math.round(R * c);
  };

  return (
    <section className="mb-5" id="interactive-examples">
      <h2 className="text-secondary mb-4 fs-4">6. Componentes Interativos: Dropdown e Avaliação</h2>
      
      {/* Primeiros Exemplos */}
      <div className="row g-4 mb-4">
        {/* Dropdown Example */}
        <div className="col-md-6">
          <div className="card h-100 shadow-sm border-0 bg-white">
            <div className="card-header bg-dark text-white fw-bold d-flex align-items-center justify-content-between">
              <span>Seletor de Tópicos</span>
              <span className="badge bg-primary">State Dropdown</span>
            </div>
            <div className="card-body d-flex flex-column justify-content-between">
              <div>
                <p className="text-muted small">Escolha um tópico no menu interativo para atualizar dinamicamente a seção de informações.</p>
                
                <div className="dropdown mb-4">
                  <button 
                    className="btn btn-primary dropdown-toggle w-100 text-start d-flex justify-content-between align-items-center shadow-sm" 
                    type="button" 
                    id="topicDropdown" 
                    data-bs-toggle="dropdown" 
                    aria-expanded="false"
                  >
                    <span>Selecionado: <strong>{topics[selectedTopic].title}</strong></span>
                  </button>
                  <ul className="dropdown-menu w-100 shadow border-0" aria-labelledby="topicDropdown">
                    <li>
                      <button 
                        className={`dropdown-item py-2 ${selectedTopic === 'react' ? 'active' : ''}`}
                        onClick={() => setSelectedTopic('react')}
                      >
                        React & Vite
                      </button>
                    </li>
                    <li>
                      <button 
                        className={`dropdown-item py-2 ${selectedTopic === 'fastapi' ? 'active' : ''}`}
                        onClick={() => setSelectedTopic('fastapi')}
                      >
                        FastAPI
                      </button>
                    </li>
                    <li>
                      <button 
                        className={`dropdown-item py-2 ${selectedTopic === 'docker' ? 'active' : ''}`}
                        onClick={() => setSelectedTopic('docker')}
                      >
                        Docker & Compose
                      </button>
                    </li>
                  </ul>
                </div>
              </div>

              {/* Dynamic content display card */}
              <div className="p-3 rounded bg-light border border-dashed transition-all">
                <div className="d-flex justify-content-between align-items-center mb-2">
                  <h6 className="fw-bold m-0 text-primary">{topics[selectedTopic].title}</h6>
                  <span className={`badge bg-${topics[selectedTopic].color}`}>{topics[selectedTopic].badge}</span>
                </div>
                <p className="small text-secondary mb-0">{topics[selectedTopic].desc}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Rating 1 - 5 Example */}
        <div className="col-md-6">
          <div className="card h-100 shadow-sm border-0 bg-white">
            <div className="card-header bg-dark text-white fw-bold d-flex align-items-center justify-content-between">
              <span>Avaliação do Sistema (1 - 5)</span>
              <span className="badge bg-primary">Interactive Rating</span>
            </div>
            <div className="card-body">
              <p className="text-muted small">Envie sua avaliação sobre o template de inicialização e a documentação do monorepo.</p>
              
              <form onSubmit={handleRatingSubmit} className="text-center py-2">
                {/* Stars container */}
                <div className="mb-3 d-flex justify-content-center gap-2">
                  {[1, 2, 3, 4, 5].map((starValue) => {
                    const isStarred = hoverRating >= starValue || (!hoverRating && rating >= starValue);
                    return (
                      <span
                        key={starValue}
                        style={{ cursor: 'pointer', fontSize: '2rem', transition: 'transform 0.1s' }}
                        className={`star-icon ${isStarred ? 'text-warning scale-110' : 'text-muted'}`}
                        onClick={() => setRating(starValue)}
                        onMouseEnter={() => setHoverRating(starValue)}
                        onMouseLeave={() => setHoverRating(0)}
                      >
                        ★
                      </span>
                    );
                  })}
                </div>

                {/* Rating feedback text */}
                <div className="mb-3">
                  <span className={`badge py-2 px-3 ${rating > 0 ? 'bg-dark' : 'bg-light text-dark'}`} style={{ fontSize: '0.9rem' }}>
                    {ratingFeedbacks[hoverRating || rating]}
                  </span>
                </div>

                {/* Submit button */}
                <button 
                  type="submit" 
                  disabled={rating === 0 || submittedRating} 
                  className="btn btn-outline-success btn-sm px-4 w-100 shadow-sm"
                >
                  {submittedRating ? 'Enviado com sucesso!' : 'Confirmar Avaliação'}
                </button>
              </form>

              {/* Toast/Notification area */}
              {submittedRating && (
                <div className="alert alert-success py-2 px-3 small text-center mt-3 mb-0 shadow-sm transition-all" role="alert">
                  Obrigado! Sua nota de {rating} estrelas foi registrada localmente.
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Novos Exemplos: Calculadora de Datas e Distância de Cidades */}
      <div className="row g-4">
        {/* Date Picker Days Calculator */}
        <div className="col-md-6">
          <div className="card h-100 shadow-sm border-0 bg-white">
            <div className="card-header bg-dark text-white fw-bold d-flex align-items-center justify-content-between">
              <span>Calculadora de Intervalo de Datas</span>
              <span className="badge bg-primary">Date Pickers</span>
            </div>
            <div className="card-body d-flex flex-column justify-content-between">
              <div>
                <p className="text-muted small">Selecione duas datas para calcular automaticamente o total de dias entre elas.</p>
                <div className="row g-3 mb-3">
                  <div className="col-6">
                    <label htmlFor="startDate" className="form-label small fw-bold text-secondary">Data Inicial</label>
                    <input 
                      type="date" 
                      id="startDate" 
                      className="form-control form-control-sm shadow-sm" 
                      value={startDate} 
                      onChange={(e) => setStartDate(e.target.value)} 
                    />
                  </div>
                  <div className="col-6">
                    <label htmlFor="endDate" className="form-label small fw-bold text-secondary">Data Final</label>
                    <input 
                      type="date" 
                      id="endDate" 
                      className="form-control form-control-sm shadow-sm" 
                      value={endDate} 
                      onChange={(e) => setEndDate(e.target.value)} 
                    />
                  </div>
                </div>
              </div>

              {/* Calculation Result */}
              <div className="p-3 rounded bg-light border border-dashed mt-2">
                <div className="d-flex justify-content-between align-items-center">
                  <span className="small fw-semibold text-secondary">Diferença calculada:</span>
                  {calculateDays() !== null ? (
                    <span className="badge bg-success p-2 fs-6 shadow-sm">
                      {calculateDays()} {Math.abs(calculateDays()) === 1 ? 'dia' : 'dias'}
                    </span>
                  ) : (
                    <span className="text-muted small italic">Escolha as duas datas</span>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* City Distance Calculator */}
        <div className="col-md-6">
          <div className="card h-100 shadow-sm border-0 bg-white">
            <div className="card-header bg-dark text-white fw-bold d-flex align-items-center justify-content-between">
              <span>Calculadora de Distância entre Cidades</span>
              <span className="badge bg-primary">Geo Distance</span>
            </div>
            <div className="card-body d-flex flex-column justify-content-between">
              <div>
                <p className="text-muted small">Selecione duas cidades presentes no banco de dados para calcular a distância geográfica em linha reta.</p>
                <div className="row g-3 mb-3">
                  <div className="col-6">
                    <label htmlFor="cityASelect" className="form-label small fw-bold text-secondary">Cidade Origem</label>
                    <select 
                      id="cityASelect" 
                      className="form-select form-select-sm shadow-sm" 
                      value={cityA} 
                      onChange={(e) => setCityA(e.target.value)}
                    >
                      {cities.map((city) => (
                        <option key={city.name} value={city.name}>{city.name}</option>
                      ))}
                    </select>
                  </div>
                  <div className="col-6">
                    <label htmlFor="cityBSelect" className="form-label small fw-bold text-secondary">Cidade Destino</label>
                    <select 
                      id="cityBSelect" 
                      className="form-select form-select-sm shadow-sm" 
                      value={cityB} 
                      onChange={(e) => setCityB(e.target.value)}
                    >
                      {cities.map((city) => (
                        <option key={city.name} value={city.name}>{city.name}</option>
                      ))}
                    </select>
                  </div>
                </div>
              </div>

              {/* Calculation Result */}
              <div className="p-3 rounded bg-light border border-dashed mt-2">
                <div className="d-flex justify-content-between align-items-center">
                  <span className="small fw-semibold text-secondary">Distância linear aproximada:</span>
                  {cityA === cityB ? (
                    <span className="badge bg-secondary p-2 fs-6 shadow-sm">Mesma localidade</span>
                  ) : (
                    <span className="badge bg-primary p-2 fs-6 shadow-sm">
                      {calculateDistance().toLocaleString('pt-BR')} km
                    </span>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
