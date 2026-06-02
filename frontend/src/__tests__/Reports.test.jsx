import React from 'react'
import { render, screen } from '@testing-library/react'
import Reports from '../pages/Reports'
import api from '../api'

jest.mock('../api')

test('renders Reports header', async () => {
  api.get.mockResolvedValue({ data: [] })
  render(<Reports />)
  expect(await screen.findByText(/Reports/i)).toBeInTheDocument()
})
