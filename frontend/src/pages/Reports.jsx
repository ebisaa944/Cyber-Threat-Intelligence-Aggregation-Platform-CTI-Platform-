import { useEffect, useState } from 'react'
import api from '../api'

export default function Reports() {
  const [items, setItems] = useState([])

  const [title, setTitle] = useState('')
  const [summary, setSummary] = useState('')

  async function createReport(e) {
    e.preventDefault()
    try {
      const resp = await api.post('reports/', { title, summary })
      setItems([resp.data, ...items])
      setTitle('')
      setSummary('')
    } catch (err) {
      console.error(err)
      alert('Could not create report')
    }
  }

  async function download(id, filename) {
    try {
      const resp = await api.get(`reports/${id}/download_pdf/`, { responseType: 'blob' })
      const url = window.URL.createObjectURL(new Blob([resp.data], { type: 'application/pdf' }))
      // open PDF in new tab for preview
      window.open(url, '_blank')
    } catch (err) {
      console.error(err)
      alert('Failed to download')
    }
  }

  useEffect(() => {
    api.get('reports/')
      .then((r) => setItems(r.data.results || r.data))
  }, [])

  return (
    <section className="card">
      <h2>Reports</h2>
      <form onSubmit={createReport} style={{marginBottom:16}}>
        <input placeholder="Title" value={title} onChange={(e)=>setTitle(e.target.value)} />
        <br />
        <textarea placeholder="Summary" value={summary} onChange={(e)=>setSummary(e.target.value)} />
        <br />
        <button type="submit" className="btn">Create Report</button>
      </form>
      <ul className="list">
        {items.map((r) => (
          <li key={r.id}>{r.title} — {r.created_by_username} <button onClick={()=>download(r.id)} style={{marginLeft:8}}>Preview</button></li>
        ))}
      </ul>
    </section>
  )
}
