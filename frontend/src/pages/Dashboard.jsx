import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { visitorAPI, deliveryAPI, emergencyAPI } from '../services/api';
import {
  Users,
  Package,
  AlertTriangle,
  UserPlus,
  Clock,
  CheckCircle,
  TrendingUp
} from 'lucide-react';
import { format } from 'date-fns';

const StatCard = ({ title, value, icon: Icon, color, link }) => (
  <Link
    to={link}
    className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition-shadow"
  >
    <div className="flex items-center justify-between">
      <div>
        <p className="text-sm text-gray-600">{title}</p>
        <p className="text-3xl font-bold text-gray-900 mt-1">{value}</p>
      </div>
      <div className={`w-12 h-12 rounded-full ${color} flex items-center justify-center`}>
        <Icon className="w-6 h-6 text-white" />
      </div>
    </div>
  </Link>
);

const Dashboard = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState({
    activeVisitors: 0,
    pendingDeliveries: 0,
    activeAlerts: 0,
    todayVisitors: 0,
  });
  const [recentVisitors, setRecentVisitors] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [visitorsRes, deliveriesRes, alertsRes] = await Promise.all([
          visitorAPI.getAll(),
          deliveryAPI.getAll(),
          emergencyAPI.getAll(true),
        ]);

        const activeVisitors = visitorsRes.data.filter(v => v.status === 'checked_in').length;
        const pendingDeliveries = deliveriesRes.data.filter(
          d => ['pending', 'received_at_gate', 'in_transit'].includes(d.status)
        ).length;
        const today = new Date().toDateString();
        const todayVisitors = visitorsRes.data.filter(
          v => new Date(v.created_at).toDateString() === today
        ).length;

        setStats({
          activeVisitors,
          pendingDeliveries,
          activeAlerts: alertsRes.data.length,
          todayVisitors,
        });

        setRecentVisitors(visitorsRes.data.slice(0, 5));
      } catch (error) {
        console.error('Failed to fetch dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            Welcome, {user?.full_name?.split(' ')[0]}!
          </h1>
          <p className="text-gray-600">Here's what's happening today</p>
        </div>
        {(user?.role === 'resident' || user?.role === 'admin') && (
          <Link
            to="/visitors/new"
            className="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
          >
            <UserPlus className="w-5 h-5" />
            Add Visitor
          </Link>
        )}
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Active Visitors"
          value={stats.activeVisitors}
          icon={Users}
          color="bg-blue-500"
          link="/visitors"
        />
        <StatCard
          title="Today's Visitors"
          value={stats.todayVisitors}
          icon={TrendingUp}
          color="bg-green-500"
          link="/visitors/history"
        />
        <StatCard
          title="Pending Deliveries"
          value={stats.pendingDeliveries}
          icon={Package}
          color="bg-orange-500"
          link="/deliveries"
        />
        <StatCard
          title="Active Alerts"
          value={stats.activeAlerts}
          icon={AlertTriangle}
          color="bg-red-500"
          link="/emergency"
        />
      </div>

      {/* Recent Visitors */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-100">
        <div className="px-6 py-4 border-b border-gray-100">
          <h2 className="text-lg font-semibold text-gray-900">Recent Visitors</h2>
        </div>
        <div className="divide-y divide-gray-100">
          {recentVisitors.length === 0 ? (
            <div className="px-6 py-8 text-center text-gray-500">
              No visitors yet
            </div>
          ) : (
            recentVisitors.map((visitor) => (
              <div key={visitor.id} className="px-6 py-4 flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center">
                    <span className="text-gray-600 font-medium">
                      {visitor.name.charAt(0).toUpperCase()}
                    </span>
                  </div>
                  <div>
                    <p className="font-medium text-gray-900">{visitor.name}</p>
                    <p className="text-sm text-gray-500">{visitor.purpose || 'General visit'}</p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <span className={`
                    px-2.5 py-1 rounded-full text-xs font-medium
                    ${visitor.status === 'checked_in' ? 'bg-green-100 text-green-700' : ''}
                    ${visitor.status === 'checked_out' ? 'bg-gray-100 text-gray-700' : ''}
                    ${visitor.status === 'approved' ? 'bg-blue-100 text-blue-700' : ''}
                    ${visitor.status === 'pending' ? 'bg-yellow-100 text-yellow-700' : ''}
                  `}>
                    {visitor.status.replace('_', ' ')}
                  </span>
                  <span className="text-sm text-gray-500 flex items-center gap-1">
                    <Clock className="w-4 h-4" />
                    {format(new Date(visitor.created_at), 'h:mm a')}
                  </span>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
