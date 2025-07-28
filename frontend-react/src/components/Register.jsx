import { useState } from 'react'
import Button from '@mui/material/Button'
import TextField from '@mui/material/TextField'
import Box from '@mui/material/Box'

function Register({ onRegister, switchToLogin }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [sshUser, setSshUser] = useState('')
  const [sshPass, setSshPass] = useState('')

  const handleSubmit = e => {
    e.preventDefault()
    fetch('/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password, ssh_user: sshUser, ssh_pass: sshPass })
    })
      .then(res => res.json())
      .then(data => {
        if (data.status === 'registered') {
          onRegister()
        } else {
          alert(data.error || 'Registration failed')
        }
      })
      .catch(err => console.error(err))
  }

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ mt: 4, display: 'flex', flexDirection: 'column', gap: 2 }}>
      <TextField label="Username" value={username} onChange={e => setUsername(e.target.value)} required />
      <TextField label="Password" type="password" value={password} onChange={e => setPassword(e.target.value)} required />
      <TextField label="SSH User" value={sshUser} onChange={e => setSshUser(e.target.value)} required />
      <TextField label="SSH Password" type="password" value={sshPass} onChange={e => setSshPass(e.target.value)} required />
      <Button type="submit" variant="contained">Register</Button>
      <Button onClick={switchToLogin}>Back to Login</Button>
    </Box>
  )
}

export default Register
