import { Link, useNavigate } from 'react-router-dom'
import { useContext, useEffect, useState } from 'react'
import { AuthContext } from '../context/AuthContext'

export default function Navbar() {
  const navigate = useNavigate()
  const { user, logout } = useContext(AuthContext)
  const [theme, setTheme] = useState(() => localStorage.getItem('theme') || 'light')

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme)
    localStorage.setItem('theme', theme)
  }, [theme])

  function handleLogout() {
    logout()
    navigate('/login')
  }

  const loggedIn = Boolean(user)

  return (
    <nav className="navbar">
      <div className="container" style={{display:'flex',alignItems:'center',justifyContent:'space-between'}}>
        <div className="nav-left">
          <Link to="/dashboard" className="brand">ThreatPulse</Link>
        </div>
        <div className="nav-right">
          <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')} className="linkish">{theme === 'light' ? 'Dark' : 'Light'}</button>
          {loggedIn ? (
            <>
              <Link to="/threats">Threats</Link>
              <Link to="/iocs">IOCs</Link>
              <Link to="/cves">CVEs</Link>
              <Link to="/reports">Reports</Link>
              <button onClick={handleLogout} className="linkish">Logout</button>
            </>
          ) : (
            <>
              <Link to="/login">Login</Link>
              <Link to="/register">Register</Link>
            </>
          )}
        </div>
      </div>
    </nav>
  )
}
