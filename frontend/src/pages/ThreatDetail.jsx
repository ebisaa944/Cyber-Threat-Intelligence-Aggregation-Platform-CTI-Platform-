import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import api from '../api'

export default function ThreatDetail() {
  const { id } = useParams()
  const [item, setItem] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get(`threats/${id}/`)
      .then(r => setItem(r.data))
      .catch(e => console.error(e))
      .finally(() => setLoading(false))
  }, [id])

  if (loading) return <div>Loading...</div>
  if (!item) return <div>Not found</div>

  return (
    <section className="card">
      <h2>{item.title}</h2>
      <div>Severity: {item.severity}</div>
      <div>Source: {item.source}</div>
      <div>Published: {item.published_date}</div>
      <h3>Description</h3>
      <p>{item.description}</p>
    </section>
  )
}
