export default function ImageAndCarousel() {
  return (
    <section className="mb-5" id="image-carousel">
      <h2 className="text-secondary mb-4 fs-4">4. Componentes Básicos: Carrossel e Imagem</h2>
      <div className="row g-4">
        {/* Image demonstration */}
        <div className="col-md-6">
          <div className="card h-100 shadow-sm border-0">
            <div className="card-header bg-dark text-white fw-bold">Imagem Estática do Projeto</div>
            <div className="card-body d-flex flex-column justify-content-between">
              <p className="text-muted small">Demonstração de renderização de imagem estática aleatória do Picsum Photos.</p>
              <img 
                src="https://picsum.photos/600/300?random=1" 
                alt="Placeholder Aleatório" 
                className="img-fluid rounded border shadow-sm mb-3"
              />
              <div className="small text-muted text-center">Imagem aleatória recarregada dinamicamente</div>
            </div>
          </div>
        </div>

        {/* Carousel demonstration */}
        <div className="col-md-6">
          <div className="card h-100 shadow-sm border-0">
            <div className="card-header bg-dark text-white fw-bold">Componente Carrossel (Slideshow)</div>
            <div className="card-body d-flex flex-column justify-content-between">
              <p className="text-muted small">Componente de carrossel com fotos aleatórias e vídeo nativo do Bootstrap 5.</p>
              
              <div id="tutorialCarousel" className="carousel slide border rounded shadow-sm bg-light" data-bs-ride="carousel">
                <div className="carousel-indicators">
                  <button type="button" data-bs-target="#tutorialCarousel" data-bs-slide-to="0" className="active" aria-current="true" aria-label="Slide 1"></button>
                  <button type="button" data-bs-target="#tutorialCarousel" data-bs-slide-to="1" aria-label="Slide 2"></button>
                  <button type="button" data-bs-target="#tutorialCarousel" data-bs-slide-to="2" aria-label="Slide 3"></button>
                  <button type="button" data-bs-target="#tutorialCarousel" data-bs-slide-to="3" aria-label="Slide 4"></button>
                </div>
                <div className="carousel-inner" style={{ height: '220px' }}>
                  <div className="carousel-item active h-100">
                    <img 
                      src="https://picsum.photos/600/300?random=2" 
                      className="d-block w-100 h-100 rounded" 
                      alt="FastAPI Slide" 
                      style={{ objectFit: 'cover', filter: 'brightness(55%)' }}
                    />
                    <div className="carousel-caption d-block">
                      <h5>FastAPI</h5>
                      <p className="small">APIs modernas e rápidas com Python.</p>
                    </div>
                  </div>
                  <div className="carousel-item h-100">
                    <img 
                      src="https://picsum.photos/600/300?random=3" 
                      className="d-block w-100 h-100 rounded" 
                      alt="React Slide" 
                      style={{ objectFit: 'cover', filter: 'brightness(55%)' }}
                    />
                    <div className="carousel-caption d-block">
                      <h5>React & Vite</h5>
                      <p className="small">Interfaces rápidas e reativas.</p>
                    </div>
                  </div>
                  <div className="carousel-item h-100">
                    <img 
                      src="https://picsum.photos/600/300?random=4" 
                      className="d-block w-100 h-100 rounded" 
                      alt="Database Slide" 
                      style={{ objectFit: 'cover', filter: 'brightness(55%)' }}
                    />
                    <div className="carousel-caption d-block">
                      <h5>PostgreSQL & MongoDB</h5>
                      <p className="small">Persistência relacional e NoSQL robusta.</p>
                    </div>
                  </div>
                  {/* Video slide */}
                  <div className="carousel-item h-100 bg-black">
                    <video 
                      className="d-block w-100 h-100 rounded" 
                      style={{ objectFit: 'contain' }} 
                      controls
                      muted
                      preload="auto"
                    >
                      <source src="https://www.w3schools.com/html/movie.mp4" type="video/mp4" />
                      Seu navegador não suporta a reprodução de vídeos.
                    </video>
                    <div className="carousel-caption d-block bg-dark bg-opacity-75 rounded px-2 py-1" style={{ bottom: '10px' }}>
                      <h5 className="m-0 fs-6">Demonstração de Vídeo</h5>
                      <p className="small m-0" style={{ fontSize: '0.75rem' }}>Mídia integrada no carrossel</p>
                    </div>
                  </div>
                </div>
                <button className="carousel-control-prev" type="button" data-bs-target="#tutorialCarousel" data-bs-slide="prev">
                  <span className="carousel-control-prev-icon" aria-hidden="true"></span>
                  <span className="visually-hidden">Anterior</span>
                </button>
                <button className="carousel-control-next" type="button" data-bs-target="#tutorialCarousel" data-bs-slide="next">
                  <span className="carousel-control-next-icon" aria-hidden="true"></span>
                  <span className="visually-hidden">Próximo</span>
                </button>
              </div>

              <div className="small text-muted text-center mt-3">Carrossel de Slides com controles interativos (incluindo vídeo)</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
