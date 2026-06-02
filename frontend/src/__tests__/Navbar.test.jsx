import React from 'react'
import { render, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import Navbar from '../components/Navbar'
import { AuthContext } from '../context/AuthContext'

test('renders Navbar with brand and links for anonymous', () => {
  render(
    <AuthContext.Provider value={{ user: null }}>
      <BrowserRouter>
        <Navbar />
      </BrowserRouter>
    </AuthContext.Provider>
  )
  expect(screen.getByText(/ThreatPulse/i)).toBeInTheDocument()
  expect(screen.getByText(/Login/i)).toBeInTheDocument()
})
