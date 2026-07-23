import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { visitorAPI } from '../services/api';
import { UserPlus, QrCode, Phone, Mail, Clock, RefreshCw } from 'lucide-react';
import { format } from 'date-fns';
import toast from 'react-hot-toast';
import QRCode from 'react-qr-code';

const Visitors = () => {
  const { user } = useAuth();
  const [visitors, setVisitors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedVisitor, setSelectedVisitor] = useState(null);

  const fetchVisitors = async () => {
    try {
      const response = await visitorAPI.getAll();
      setVisitors(response.data.filter(v => 
        ['pending', 'approved', 'checked_in'].includes(v.status)
      ));
    } catch (error) {
      toast.error('Failed to fetch visitors');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchVisitors();
  }, []);

  const handleCheckOut = async (visitorId) => {
    try {
      await visitorAPI.checkOut(visitorId);
      toast.success('Visitor checked out');
      fetchVisitors();
    } catch (error) {
      toast.error('Failed to check out visitor');
    }
  };

  const handleResendOTP = async (visitorId) => {
    try {
      await visitorAPI.resendOTP(visitorId);
      toast.success('OTP sent');
    } catch (error) {
      toast.error('Failed to send OTP');
    }
  };

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
        <h1 className="text-2xl font-bold text-gray-900">Active Visitors</h1>
        <div className="flex gap-3">
          <button
            onClick={fetchVisitors}
            className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg"
          >
            <RefreshCw className="w-5 h-5" />
          </button>
          {(user?.role === 'resident' || user?.role === 'admin') && (
            <Link
              to="/visitors/new"
              className="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
            >
              <UserPlus className="w-5 h-5" />
              Add Visitor
            </Link>
          )}
        </div>
      </div>

      {visitors.length === 0 ? (
        <div className="bg-white rounded-xl p-12 text-center">
          <div className="w-16 h-16 rounded-full bg-gray-100 flex items-center justify-center mx-auto mb-4">
            <UserPlus className="w-8 h-8 text-gray-400" />
          </div>
          <h3 className="text-lg font-medium text-gray-900">No active visitors</h3>
          <p className="text-gray-500 mt-1">Create a visitor pass to get started</p>
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {visitors.map((visitor) => (
            <div
              key={visitor.id}
              className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden"
            >
              <div className="p-5">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h3 className="font-semibold text-gray-900">{visitor.name}</h3>
                    <p className="text-sm text-gray-500">{visitor.purpose || 'General visit'}</p>
                  </div>
                  <span className={`
                    px-2.5 py-1 rounded-full text-xs font-medium
                    ${visitor.status === 'checked_in' ? 'bg-green-100 text-green-700' : ''}
                    ${visitor.status === 'approved' ? 'bg-blue-100 text-blue-700' : ''}
                    ${visitor.status === 'pending' ? 'bg-yellow-100 text-yellow-700' : ''}
                  `}>
                    {visitor.status.replace('_', ' ')}
                  </span>
                </div>

                <div className="space-y-2 text-sm">
                  {visitor.phone && (
                    <div className="flex items-center gap-2 text-gray-600">
                      <Phone className="w-4 h-4" />
                      {visitor.phone}
                    </div>
                  )}
                  {visitor.email && (
                    <div className="flex items-center gap-2 text-gray-600">
                      <Mail className="w-4 h-4" />
                      {visitor.email}
                    </div>
                  )}
                  <div className="flex items-center gap-2 text-gray-600">
                    <Clock className="w-4 h-4" />
                    {format(new Date(visitor.created_at), 'MMM d, h:mm a')}
                  </div>
                </div>
              </div>

              <div className="px-5 py-3 bg-gray-50 border-t flex gap-2">
                <button
                  onClick={() => setSelectedVisitor(visitor)}
                  className="flex-1 flex items-center justify-center gap-1 py-2 text-sm font-medium text-primary-600 hover:bg-primary-50 rounded-lg"
                >
                  <QrCode className="w-4 h-4" />
                  Show QR
                </button>
                {visitor.phone && (
                  <button
                    onClick={() => handleResendOTP(visitor.id)}
                    className="flex-1 py-2 text-sm font-medium text-gray-600 hover:bg-gray-100 rounded-lg"
                  >
                    Resend OTP
                  </button>
                )}
                {visitor.status === 'checked_in' && (user?.role === 'security_guard' || user?.role === 'admin') && (
                  <button
                    onClick={() => handleCheckOut(visitor.id)}
                    className="flex-1 py-2 text-sm font-medium text-red-600 hover:bg-red-50 rounded-lg"
                  >
                    Check Out
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* QR Modal */}
      {selectedVisitor && (
        <div
          className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
          onClick={() => setSelectedVisitor(null)}
        >
          <div
            className="bg-white rounded-2xl p-6 max-w-sm w-full"
            onClick={(e) => e.stopPropagation()}
          >
            <h3 className="text-lg font-semibold text-center mb-4">
              Visitor Pass: {selectedVisitor.name}
            </h3>
            <div className="flex justify-center p-4 bg-white rounded-lg">
              {selectedVisitor.qr_code ? (
                <img 
                  src={selectedVisitor.qr_code} 
                  alt="QR Code"
                  className="w-48 h-48"
                />
              ) : (
                <QRCode value={selectedVisitor.qr_token || `visitor:${selectedVisitor.id}`} size={192} />
              )}
            </div>
            <p className="text-center text-sm text-gray-500 mt-4">
              Show this QR code at the security gate
            </p>
            <button
              onClick={() => setSelectedVisitor(null)}
              className="w-full mt-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200"
            >
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Visitors;
