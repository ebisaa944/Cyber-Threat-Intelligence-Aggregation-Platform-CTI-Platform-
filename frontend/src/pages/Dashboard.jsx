import { useEffect, useState } from 'react'
import api from '../api'
import { Link } from 'react-router-dom'
import { Pie, Line } from 'react-chartjs-2'
import { Chart, ArcElement, CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend } from 'chart.js'

Chart.register(ArcElement, CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend)

export default function Dashboard() {
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    let mounted = true
    api.get('summary/')
      .then((r) => { if (mounted) setData(r.data) })
      .catch((e) => { if (mounted) setError('Could not load dashboard') })
    return () => { mounted = false }
  }, [])

  if (error) return <div className="error">{error}</div>
  if (!data) return <div>Loading...</div>

  const severityData = {
    labels: ['critical','high','medium','low'],
    datasets: [{ data: [data.severity_count?.critical || 0, data.severity_count?.high || 0, data.severity_count?.medium || 0, data.severity_count?.low || 0], backgroundColor: ['#b91c1c','#f97316','#facc15','#10b981'] }]
  }

  const trendLabels = (data.daily_trend || []).map(d => d.date)
  const trendValues = (data.daily_trend || []).map(d => d.count)
  const trendData = { labels: trendLabels, datasets: [{ label: 'Threats', data: trendValues, borderColor: '#2563eb', tension: 0.3 }] }

  return (
    <section className="dashboard card">
      <h2>Dashboard</h2>
      <div className="summary-grid">
        <div className="summary-card">
          <h3>Total threats</h3>
          <p>{data.totals?.threats ?? 0}</p>
        </div>
        <div className="summary-card">
          <h3>Total IOCs</h3>
          <p>{data.totals?.iocs ?? 0}</p>
        </div>
        <div className="summary-card">
          <h3>Total CVEs</h3>
          <p>{data.totals?.cves ?? 0}</p>
        </div>
        <div className="summary-card">
          <h3>Critical CVEs</h3>
          <p>{data.totals?.critical_cves ?? 0}</p>
        </div>
      </div>

      <div style={{display:'flex',gap:16,marginTop:16}}>
        <div style={{width:280}}>
          <h4>Severity distribution</h4>
          <Pie data={severityData} />
        </div>
        <div style={{flex:1}}>
          <h4>Daily trend</h4>
          <Line data={trendData} />
        </div>
      </div>

      <div style={{marginTop:20}}>
        <h4>Top sources</h4>
        <ul>
          {(data.top_sources || []).map(s => <li key={s.source}>{s.source} — {s.count}</li>)}
        </ul>
      </div>
      
      <div style={{marginTop:20}}>
        <h4>Recent threats</h4>
        <RecentThreats />
      </div>
    </section>
  )
}

function RecentThreats() {
  const [items, setItems] = useState([])
  useEffect(()=>{
    api.get('threats/', { params: { page_size: 6, ordering: '-published_date' } })
      .then(r => setItems(r.data.results || r.data))
      .catch(e=>console.error(e))
  }, [])
  return (
    <ul>
      {items.map(t=> <li key={t.id}><Link to={`/threats/${t.id}`}>{t.title}</Link> — {t.severity}</li>)}
    </ul>
  )
}
