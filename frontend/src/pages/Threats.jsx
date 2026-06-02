import { useEffect, useState } from 'react'
import api from '../api'
import { Link, useSearchParams } from 'react-router-dom'

export default function Threats() {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [next, setNext] = useState(null)
  const [previous, setPrevious] = useState(null)
  const [count, setCount] = useState(0)
  const [severities, setSeverities] = useState(['critical','high','medium','low'])

  const [searchParams, setSearchParams] = useSearchParams()
  const page = searchParams.get('page') || 1
  const q = searchParams.get('q') || ''
  const severity = searchParams.get('severity') || ''

  useEffect(() => {
    setLoading(true)
    const params = { page }
    if (q) params.search = q
    if (severity) params.severity = severity
    api.get('threats/', { params })
      .then((r) => {
        setItems(r.data.results || r.data)
        setNext(r.data.next)
        setPrevious(r.data.previous)
        setCount(r.data.count || 0)
      })
      .catch((e)=> console.error(e))
      .finally(() => setLoading(false))
  }, [page, q, severity])

  function setPage(newPage) {
    searchParams.set('page', newPage)
    setSearchParams(searchParams)
  }

  function onSearch(ev) {
    ev.preventDefault()
    const val = ev.target.elements.search.value
    if (val) searchParams.set('q', val)
    else searchParams.delete('q')
    searchParams.set('page', 1)
    setSearchParams(searchParams)
  }

  function onSeverityChange(ev) {
    const val = ev.target.value
    if (val) searchParams.set('severity', val)
    else searchParams.delete('severity')
    searchParams.set('page', 1)
    setSearchParams(searchParams)
  }

  if (loading) return <div>Loading threats...</div>

  return (
    <section className="card">
      <h2>Threats</h2>
      <form onSubmit={onSearch} style={{marginBottom:12}}>
        <input name="search" defaultValue={q} placeholder="Search threats..." />
        <select onChange={onSeverityChange} defaultValue={severity} style={{marginLeft:8, width: 'auto'}}>
          <option value="">All severities</option>
          {severities.map(s => <option key={s} value={s}>{s}</option>)}
        </select>
        <button type="submit" className="btn" style={{marginLeft:8}}>Search</button>
      </form>

      <div>Showing {items.length} of {count}</div>
      <ul className="list">
        {items.map((t) => (
          <li key={t.id}>
            <Link to={`/threats/${t.id}`}><strong>{t.title}</strong></Link> — {t.severity} — {t.source}
          </li>
        ))}
      </ul>

      <div style={{marginTop:12}}>
        <button onClick={() => setPage(Math.max(1, Number(page)-1))} disabled={!previous} className="btn">Previous</button>
        <span style={{margin:'0 8px'}}>Page {page}</span>
        <button onClick={() => setPage(Number(page)+1)} disabled={!next} className="btn">Next</button>
      </div>
    </section>
  )
}
