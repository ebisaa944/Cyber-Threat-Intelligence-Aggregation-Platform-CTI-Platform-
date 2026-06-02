import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Navbar from './components/Navbar'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import Threats from './pages/Threats'
import ThreatDetail from './pages/ThreatDetail'
import IOCs from './pages/IOCs'
import CVEs from './pages/CVEs'
import CveDetail from './pages/CveDetail'
import Reports from './pages/Reports'
import PrivateRoute from './components/PrivateRoute'
import './App.css'

function App() {
  const isAuthenticated = () => Boolean(localStorage.getItem('access_token'))

  return (
    <BrowserRouter>
      <Navbar />
      <main className="container">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          <Route path="/dashboard" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
          <Route path="/threats" element={<PrivateRoute><Threats /></PrivateRoute>} />
          <Route path="/threats/:id" element={<PrivateRoute><ThreatDetail /></PrivateRoute>} />
          <Route path="/iocs" element={<PrivateRoute><IOCs /></PrivateRoute>} />
          <Route path="/cves" element={<PrivateRoute><CVEs /></PrivateRoute>} />
          <Route path="/cves/:id" element={<PrivateRoute><CveDetail /></PrivateRoute>} />
          <Route path="/reports" element={<PrivateRoute><Reports /></PrivateRoute>} />

          <Route path="/" element={<Navigate to="/dashboard" />} />
        </Routes>
      </main>
    </BrowserRouter>
  )
}

export default App
