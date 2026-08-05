export default function VideoComponent() {
  return (
    <section className="mb-5" id="video-section">
      <h2 className="text-secondary mb-3 fs-4">5. Componente de Vídeo Autônomo</h2>
      <p className="text-muted small">Demonstração de um player de vídeo HTML5 completo, estilizado em um layout moderno.</p>
      
      <div className="card shadow-sm border-0 bg-white">
        <div className="card-header bg-dark text-white fw-bold d-flex align-items-center justify-content-between">
          <span>Vídeo Educacional: Arquitetura de Software</span>
          <span className="badge bg-primary">HTML5 Video</span>
        </div>
        <div className="card-body p-4">
          <div className="row g-4 align-items-center">
            <div className="col-lg-7">
              <div className="ratio ratio-16x9 bg-black rounded shadow-sm overflow-hidden border">
                <video 
                  controls 
                  preload="auto"
                  poster="https://picsum.photos/800/450?random=10"
                >
                  <source src="https://www.w3schools.com/html/mov_bbb.mp4" type="video/mp4" />
                  Seu navegador não suporta a tag de vídeo do HTML5.
                </video>
              </div>
            </div>
            <div className="col-lg-5">
              <h5 className="text-primary fw-bold mb-3">Vídeo de Exemplo (Big Buck Bunny)</h5>
              <p className="text-secondary small">
                Este componente exibe um vídeo hospedado externamente utilizando a tag nativa de HTML5 <code>&lt;video&gt;</code> com a classe auxiliar de proporção do Bootstrap (<code>ratio ratio-16x9</code>) para obter responsividade perfeita em qualquer dispositivo.
              </p>
              <p className="text-secondary small">
                O atributo <code>poster</code> carrega uma imagem aleatória como pré-visualização antes da reprodução ser iniciada.
              </p>
              <div className="d-flex gap-2 mt-4">
                <span className="badge bg-light text-dark border">1080p</span>
                <span className="badge bg-light text-dark border">MP4</span>
                <span className="badge bg-light text-dark border">H.264</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
