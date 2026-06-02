import { useState, useContext } from 'react'
import { useNavigate } from 'react-router-dom'
import { AuthContext } from '../context/AuthContext'

export default function Login() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState(null)
  const navigate = useNavigate()
  const { login } = useContext(AuthContext)

  async function submit(e) {
    e.preventDefault()
    try {
      await login({ username, password })
      navigate('/dashboard')
    } catch (err) {
      const detail = err?.response?.data || err.message || 'Invalid credentials'
      setError(JSON.stringify(detail))
    }
  }

  return (
    <section className="card" style={{maxWidth:520, margin:'0 auto'}}>
      <h2>Login</h2>
      <form onSubmit={submit}>
        <label>
          Username
          <input value={username} onChange={(e) => setUsername(e.target.value)} />
        </label>
        <label>
          Password
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        </label>
        <button type="submit" className="btn">Sign in</button>
        {error && <div className="error">{error}</div>}
      </form>
    </section>
  )
}
