import { useState } from 'react'
import Button from '@mui/material/Button'
import TextField from '@mui/material/TextField'
import Box from '@mui/material/Box'

function Login({ onLogin, switchToRegister }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')

  const handleSubmit = e => {
    e.preventDefault()
    fetch('/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    })
      .then(res => res.json())
      .then(data => {
        if (data.token) {
          onLogin(data.token)
        } else {
          alert(data.error || 'Login failed')
        }
      })
      .catch(err => console.error(err))
  }

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ mt: 4, display: 'flex', flexDirection: 'column', gap: 2 }}>
      <TextField label="Username" value={username} onChange={e => setUsername(e.target.value)} required />
      <TextField label="Password" type="password" value={password} onChange={e => setPassword(e.target.value)} required />
      <Button type="submit" variant="contained">Login</Button>
      <Button onClick={switchToRegister}>Register</Button>
    </Box>
  )
}

export default Login
