import MapComponent from './MapComponent';

export default function ProfessorProfile({ professor }) {
  if (!professor) return null;

  return (
    <section className="mb-5" id="professor-profile">
      <h2 className="text-secondary mb-3 fs-4">1. Relação 1:1 - Detalhes do Professor</h2>
      <div className="card shadow-sm border-0 bg-light">
        <div className="card-body">
          <h5 className="card-title text-primary fw-bold">{professor.nome}</h5>
          <h6 className="card-subtitle mb-3 text-muted">{professor.email}</h6>
          <p className="card-text mb-2">
            <strong>Sala/Gabinete:</strong> <span className="badge bg-primary ms-1">{professor.sala}</span>
          </p>
          <p className="card-text mb-0">
            <strong>Atuação Profissional:</strong> {professor.biografia}
          </p>
          {professor.biografia_mapa && (
            <MapComponent geojson={professor.biografia_mapa} />
          )}
        </div>
      </div>
    </section>
  );
}
