import { useState } from 'react'
import Login from './components/Login'
import Register from './components/Register'
import JobTable from './components/JobTable'

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'))
  const [page, setPage] = useState(token ? 'jobs' : 'login')

  const handleLogin = tok => {
    setToken(tok)
    localStorage.setItem('token', tok)
    setPage('jobs')
  }

  const logout = () => {
    setToken(null)
    localStorage.removeItem('token')
    setPage('login')
  }

  if (page === 'login') {
    return <Login onLogin={handleLogin} switchToRegister={() => setPage('register')} />
  }

  if (page === 'register') {
    return <Register onRegister={() => setPage('login')} switchToLogin={() => setPage('login')} />
  }

  return (
    <div>
      <button onClick={logout}>Logout</button>
      <JobTable token={token} />
    </div>
  )
}

export default App
