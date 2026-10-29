import { useEffect, useState } from 'react'

const API = 'http://localhost:8000/api/v1'

async function buscarJson(endpoint) {
  const resposta = await fetch(4{API}/4{endpoint})
  if (!resposta.ok) {
    throw new Error(60GET /4{endpoint} devolveu 4{resposta.status}60)
  }
  return resposta.json()
}

export default function HoteisRaw() {
  const [hoteis, setHoteis] = useState(null)
  const [cidades, setCidades] = useState(null)
  const [erro, setErro] = useState(null)
  const [carregando, setCarregando] = useState(true)

  useEffect(() => {
    Promise.all([buscarJson('cidades'), buscarJson('hoteis')])
      .then(([jsonCidades, jsonHoteis]) => {
        setCidades(jsonCidades)
        setHoteis(jsonHoteis)
      })
      .catch((e) => setErro(e.message))
      .finally(() => setCarregando(false))
  }, [])

  if (carregando) {
    return <p>Carregando hotéis...</p>
  }

  if (erro) {
    return (
      <div className="alert alert-danger" role="alert">
        <strong>Erro ao falar com a API:</strong> {erro}
        <br />
        O backend está no ar? Teste: <code>{API}/hoteis</code>
      </div>
    )
  }

  return (
    <section className="mt-5">
      <h2>Hotéis e Cidades — JSON bruto</h2>
      <p>
        Saída literal da API, sem tratamento. Isso permite conferir o caminho
        completo do dado até o navegador.
      </p>

      <h3>GET {API}/cidades</h3>
      <pre className="bg-light border rounded p-3 overflow-auto">
        {JSON.stringify(cidades, null, 2)}
      </pre>

      <h3>GET {API}/hoteis</h3>
      <pre className="bg-light border rounded p-3 overflow-auto">
        {JSON.stringify(hoteis, null, 2)}
      </pre>
    </section>
  )
}
