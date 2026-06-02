import React from 'react'
import { render, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import Login from '../pages/Login'
import { AuthContext } from '../context/AuthContext'

test('renders Login form', () => {
  render(
    <AuthContext.Provider value={{ login: jest.fn() }}>
      <BrowserRouter>
        <Login />
      </BrowserRouter>
    </AuthContext.Provider>
  )
  expect(screen.getByText(/Login/i)).toBeInTheDocument()
  expect(screen.getByRole('button', { name: /sign in/i })).toBeInTheDocument()
})
