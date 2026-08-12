import { BrowserRouter as Router, Navigate, Routes, Route } from 'react-router-dom'
import Login from "./pages/Login"
import Profile from './pages/Profile'
import ProfileEdit from './pages/ProfileEdit'
import { AuthProvider } from './context/AuthContext'
import Register from './pages/Register'
import Home from './pages/Home'
import Search from './pages/Search'
import UserProfile from './pages/UserProfile'
import Chat from './pages/Chat'
import VerifyEmail from './pages/VerifyEmail'
import ResetPassword from './pages/ResetPassword'
import VerifyResetPassword from './pages/VerifyResetPassword'
import Notifications from './pages/Notifications'
import Footer from './components/Footer'


import DevTools from './pages/DevTools'
import { ThemeProvider } from './context/ThemeContext'
import ProtectedRoute from './components/ProtectedRoute'


export default function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <Router>
          <div className="site-shell">
            <main className="site-main">
              <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="/verify-email" element={<VerifyEmail />} />
                <Route path="/reset-password" element={<ResetPassword />} />
                <Route path="/verify-reset-password" element={<VerifyResetPassword />} />
                <Route path="/" element={<Navigate to="/home" replace />} />
                <Route element={<ProtectedRoute />}>
                  <Route path="/profile/edit" element={<ProfileEdit />} />
                  <Route path="/dev" element={<DevTools />} />
                  <Route element={<ProtectedRoute requireComplete />}>
                    <Route path="/profile" element={<Profile />} />
                    <Route path="/home" element={<Home />} />
                    <Route path="/search" element={<Search />} />
                    <Route path="/user/:id" element={<UserProfile />} />
                    <Route path="/chat" element={<Chat />} />
                    <Route path="/chat/:id" element={<Chat />} />
                    <Route path="/notification" element={<Notifications />} />
                  </Route>
                </Route>
                <Route path="*" element={<Navigate to="/home" replace />} />
              </Routes>
            </main>
            <Footer />
          </div>
        </Router>
      </AuthProvider>
    </ThemeProvider>
  )
}
