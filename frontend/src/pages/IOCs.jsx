import { useEffect, useState } from 'react'
import api from '../api'
import { Link, useSearchParams } from 'react-router-dom'

export default function IOCs() {
  const [items, setItems] = useState([])
  const [types] = useState(['ip','domain','url','hash','email'])
  const [searchParams, setSearchParams] = useSearchParams()
  const q = searchParams.get('q') || ''
  const type = searchParams.get('type') || ''

  useEffect(() => {
    const params = {}
    if (q) params.search = q
    if (type) params.ioc_type = type
    api.get('iocs/', { params })
      .then((r) => setItems(r.data.results || r.data))
      .catch(e => console.error(e))
  }, [q, type])

  function onSearch(e) {
    e.preventDefault()
    const val = e.target.elements.search.value
    if (val) searchParams.set('q', val)
    else searchParams.delete('q')
    setSearchParams(searchParams)
  }

  function onTypeChange(e) {
    const v = e.target.value
    if (v) searchParams.set('type', v)
    else searchParams.delete('type')
    setSearchParams(searchParams)
  }

  return (
    <section className="card">
      <h2>IOCs</h2>
      <form onSubmit={onSearch}>
        <input name="search" defaultValue={q} placeholder="Search IOCs..." />
        <select onChange={onTypeChange} defaultValue={type} style={{marginLeft:8, width:'auto'}}>
          <option value="">All types</option>
          {types.map(t => <option key={t} value={t}>{t}</option>)}
        </select>
        <button type="submit" className="btn" style={{marginLeft:8}}>Search</button>
      </form>

      <ul className="list">
        {items.map((ioc) => (
          <li key={ioc.id}>{ioc.ioc_type}: {ioc.value} — {ioc.source} {ioc.related_threat && (<Link to={`/threats/${ioc.related_threat}`}>[related threat]</Link>)}</li>
        ))}
      </ul>
    </section>
  )
}
