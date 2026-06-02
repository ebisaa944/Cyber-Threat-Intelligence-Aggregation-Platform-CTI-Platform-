import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import api from '../api'

export default function CVEs() {
  const [items, setItems] = useState([])

  useEffect(() => {
    api.get('cves/')
      .then((r) => setItems(r.data.results || r.data))
  }, [])

  return (
    <section className="card">
      <h2>CVEs</h2>
      <ul className="list">
        {items.map((c) => (
          <li key={c.id}>
            <Link to={`/cves/${c.id}`}><strong>{c.cve_id}</strong></Link> — {c.severity} ({c.cvss_score ?? 'N/A'}) {' '}
            {c.exploit_available ? <span className="badge">Exploit</span> : null}
          </li>
        ))}
      </ul>
    </section>
  )
}
