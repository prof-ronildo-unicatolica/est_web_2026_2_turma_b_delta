export default function DisciplinasList({ disciplinas }) {
  if (!disciplinas || disciplinas.length === 0) return null;

  return (
    <section className="mb-5" id="disciplinas-list">
      <h2 className="text-secondary mb-3 fs-4">2. Relação 1:N - Disciplinas Ministradas</h2>
      <p className="text-muted small">Lista simples mostrando a disciplina vinculada ao professor e as tecnologias ensinadas (relação N:M).</p>
      <div className="list-group shadow-sm border-0">
        {disciplinas.map((disc, idx) => (
          <div key={idx} className="list-group-item list-group-item-action border-1 rounded mb-2">
            <div className="d-flex w-100 justify-content-between align-items-center">
              <h5 className="mb-1 text-primary fw-bold fs-5">{disc.nome}</h5>
              <span className="badge bg-dark">Ano: {disc.ano} | {disc.semestre}º Semestre</span>
            </div>
            <p className="mb-1 mt-2 text-secondary small">Tecnologias ensinadas nesta disciplina:</p>
            <div className="mt-2">
              {disc.tecnologias.map((tech, tIdx) => (
                <span key={tIdx} className="badge bg-secondary me-1 px-2.5 py-1.5">{tech}</span>
              ))}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
