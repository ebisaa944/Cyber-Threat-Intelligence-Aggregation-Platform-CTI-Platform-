import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import api from '../api'

export default function CveDetail() {
  const { id } = useParams()
  const [item, setItem] = useState(null)

  useEffect(() => {
    api.get(`cves/${id}/`).then(r => setItem(r.data)).catch(e => console.error(e))
  }, [id])

  if (!item) return <div>Loading...</div>

  return (
    <section>
      <h2>{item.cve_id}</h2>
      <div>CVSS: {item.cvss_score ?? 'N/A'}</div>
      <div>Severity: {item.severity}</div>
      <div>Exploit available: {item.exploit_available ? 'Yes' : 'No'}</div>
      <h3>Description</h3>
      <p>{item.description}</p>
    </section>
  )
}
