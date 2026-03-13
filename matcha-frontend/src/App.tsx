import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Login from "./pages/Login"
import Profile from './pages/Profile'
import { AuthProvider } from './context/AuthContext'
import Register from './pages/Register'
import Home from './pages/Home'
import VerifyEmail from './pages/VerifyEmail' 
import ResetPassword from './pages/ResetPassword'
import VerifyResetPassword from './pages/VerifyResetPassword'


export default function App() {
  return (
    <AuthProvider>
        <Router>
        <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/profile" element={<Profile />}></Route>
            <Route path="/register" element={<Register />}></Route>
            <Route path="/verify-email" element={<VerifyEmail/>}></Route>
            <Route path="/reset-password" element={<ResetPassword/>}></Route>
            <Route path="/home" element={<Home/>}></Route>
            <Route path="/verify-reset-password" element={<VerifyResetPassword/>}></Route>
            <Route path="/" element={<Login />} /> 
        </Routes>
        </Router>
    </AuthProvider>
  )
}