import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './context/AuthContext';
import Layout from './components/Layout';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Visitors from './pages/Visitors';
import CreateVisitor from './pages/CreateVisitor';
import QRScanner from './pages/QRScanner';
import Deliveries from './pages/Deliveries';
import Emergency from './pages/Emergency';
import VisitorHistory from './pages/VisitorHistory';

const ProtectedRoute = ({ children, roles }) => {
  const { user, loading, isAuthenticated } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (roles && !roles.includes(user.role)) {
    return <Navigate to="/dashboard" replace />;
  }

  return children;
};

function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      
      <Route path="/" element={
        <ProtectedRoute>
          <Layout />
        </ProtectedRoute>
      }>
        <Route index element={<Navigate to="/dashboard" replace />} />
        <Route path="dashboard" element={<Dashboard />} />
        <Route path="visitors" element={<Visitors />} />
        <Route path="visitors/new" element={
          <ProtectedRoute roles={['resident', 'admin']}>
            <CreateVisitor />
          </ProtectedRoute>
        } />
        <Route path="visitors/history" element={<VisitorHistory />} />
        <Route path="scan" element={
          <ProtectedRoute roles={['security_guard', 'admin']}>
            <QRScanner />
          </ProtectedRoute>
        } />
        <Route path="deliveries" element={<Deliveries />} />
        <Route path="emergency" element={<Emergency />} />
      </Route>
    </Routes>
  );
}

export default App;
