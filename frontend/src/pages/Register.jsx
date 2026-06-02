import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api'

export default function Register() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [email, setEmail] = useState('')
  const [error, setError] = useState(null)
  const navigate = useNavigate()

  async function submit(e) {
    e.preventDefault()
    try {
      await api.post('auth/register/', { username, password, email })
      navigate('/login')
    } catch (err) {
      setError('Registration failed')
    }
  }

  return (
    <section className="card" style={{maxWidth:520, margin:'0 auto'}}>
      <h2>Register</h2>
      <form onSubmit={submit}>
        <label>
          Username
          <input value={username} onChange={(e) => setUsername(e.target.value)} />
        </label>
        <label>
          Email
          <input value={email} onChange={(e) => setEmail(e.target.value)} />
        </label>
        <label>
          Password
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        </label>
        <button type="submit" className="btn">Create account</button>
        {error && <div className="error">{error}</div>}
      </form>
    </section>
  )
}
