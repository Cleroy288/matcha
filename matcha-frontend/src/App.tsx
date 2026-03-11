import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Login from "./pages/Login"
import Profile from './pages/Profiel'
import { AuthProvider } from './context/AuthContext'
import Register from './pages/Register'

export default function App() {
  return (
    <AuthProvider>
        <Router>
        <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/profile" element={<Profile />}></Route>
            <Route path="/register" element={<Register />}></Route>
            <Route path="/" element={<Login />} /> 
        </Routes>
        </Router>
    </AuthProvider>
  )
}