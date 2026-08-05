export default function StacksTable({ stacks }) {
  if (!stacks || stacks.length === 0) return null;

  return (
    <section className="mb-5" id="stacks-table">
      <h2 className="text-secondary mb-3 fs-4">3. Relação N:M - Stacks, Tecnologias e Linguagens</h2>
      <p className="text-muted small">Tabela ilustrando quais tecnologias utilizam quais linguagens base (ex: Tailwind usa CSS e JS).</p>
      <div className="table-responsive shadow-sm rounded">
        <table className="table table-bordered table-striped table-hover mb-0 bg-white">
          <thead className="table-dark">
            <tr>
              <th>Stack</th>
              <th>Tecnologia</th>
              <th>Linguagens Utilizadas (N:M)</th>
            </tr>
          </thead>
          <tbody>
            {stacks.flatMap((stack) =>
              stack.tecnologias.map((tech, idx) => (
                <tr key={`${stack.nome}-${tech.nome}`}>
                  {idx === 0 ? (
                    <td rowSpan={stack.tecnologias.length} className="align-middle fw-bold text-primary bg-light">
                      {stack.nome}
                    </td>
                  ) : null}
                  <td className="fw-semibold">{tech.nome}</td>
                  <td>
                    {tech.linguagens.map((lang, lIdx) => (
                      <span key={lIdx} className="badge bg-info text-dark me-1">{lang}</span>
                    ))}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
}
