import { useEffect, useState } from 'react'
import Container from '@mui/material/Container'
import CssBaseline from '@mui/material/CssBaseline'
import Typography from '@mui/material/Typography'
import { DataGrid } from '@mui/x-data-grid'

function JobTable({ token }) {
  const [rows, setRows] = useState([])

  useEffect(() => {
    const fetchJobs = () => {
      fetch('/jobs', { headers: { Authorization: token } })
        .then(res => res.json())
        .then(data => {
          if (Array.isArray(data)) {
            setRows(data.map((row, idx) => ({ id: idx, ...row })))
          }
        })
        .catch(err => console.error(err))
    }
    fetchJobs()
    const id = setInterval(fetchJobs, 10000)
    return () => clearInterval(id)
  }, [token])

  const columns = [
    { field: 'JOBID', headerName: 'Job ID', flex: 1 },
    { field: 'NAME', headerName: 'Name', flex: 1 },
    { field: 'USER', headerName: 'User', flex: 1 },
    { field: 'ST', headerName: 'Status', flex: 1 },
    { field: 'TIME', headerName: 'Time', flex: 1 },
    { field: 'NODES', headerName: 'Nodes', flex: 1 },
    { field: 'NODELIST(REASON)', headerName: 'Node List', flex: 1 }
  ]

  return (
    <Container maxWidth="xl">
      <CssBaseline />
      <Typography variant="h4" gutterBottom>
        Job Monitor
      </Typography>
      <div style={{ height: 600, width: '100%' }}>
        <DataGrid rows={rows} columns={columns} pageSize={25} />
      </div>
    </Container>
  )
}

export default JobTable
