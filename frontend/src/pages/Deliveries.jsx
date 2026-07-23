import { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { deliveryAPI } from '../services/api';
import { Package, Truck, CheckCircle, Clock, Plus } from 'lucide-react';
import { format } from 'date-fns';
import toast from 'react-hot-toast';

const statusColors = {
  pending: 'bg-yellow-100 text-yellow-700',
  received_at_gate: 'bg-blue-100 text-blue-700',
  in_transit: 'bg-purple-100 text-purple-700',
  delivered: 'bg-green-100 text-green-700',
  returned: 'bg-red-100 text-red-700',
};

const Deliveries = () => {
  const { user } = useAuth();
  const [deliveries, setDeliveries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    resident_id: '',
    courier_name: '',
    courier_company: '',
    tracking_number: '',
    package_description: '',
  });

  const fetchDeliveries = async () => {
    try {
      const response = await deliveryAPI.getAll();
      setDeliveries(response.data);
    } catch (error) {
      toast.error('Failed to fetch deliveries');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDeliveries();
  }, []);

  const handleCreate = async (e) => {
  e.preventDefault();

  try {
    const response = await deliveryAPI.create({
      resident_id: Number(formData.resident_id),
      courier_name: formData.courier_name,
      courier_company: formData.courier_company,
      tracking_number: formData.tracking_number,
      package_description: formData.package_description,
    });

    console.log(response.data);

    toast.success("Delivery registered");

    setShowForm(false);

    setFormData({
      resident_id: "",
      courier_name: "",
      courier_company: "",
      tracking_number: "",
      package_description: "",
    });

    fetchDeliveries();
  } catch (error) {
    console.log(error.response);
    console.log(error.response?.data);

    toast.error(
      error.response?.data?.detail || "Failed to register delivery"
    );
  }
};

  const handleStatusUpdate = async (id, status) => {
    try {
      await deliveryAPI.update(id, { status });
      toast.success('Status updated');
      fetchDeliveries();
    } catch (error) {
      toast.error('Failed to update status');
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
        <h1 className="text-2xl font-bold text-gray-900">Deliveries</h1>
        {(user?.role === 'security_guard' || user?.role === 'admin') && (
          <button
            onClick={() => setShowForm(true)}
            className="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
          >
            <Plus className="w-5 h-5" />
            Register Delivery
          </button>
        )}
      </div>

      {deliveries.length === 0 ? (
        <div className="bg-white rounded-xl p-12 text-center">
          <div className="w-16 h-16 rounded-full bg-gray-100 flex items-center justify-center mx-auto mb-4">
            <Package className="w-8 h-8 text-gray-400" />
          </div>
          <h3 className="text-lg font-medium text-gray-900">No deliveries</h3>
          <p className="text-gray-500 mt-1">Deliveries will appear here</p>
        </div>
      ) : (
        <div className="space-y-4">
          {deliveries.map((delivery) => (
            <div
              key={delivery.id}
              className="bg-white rounded-xl shadow-sm border p-5"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 rounded-lg bg-orange-100 flex items-center justify-center">
                    <Truck className="w-6 h-6 text-orange-600" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900">
                      {delivery.courier_company || 'Unknown Courier'}
                    </h3>
                    <p className="text-sm text-gray-500">
                      {delivery.tracking_number || 'No tracking number'}
                    </p>
                  </div>
                </div>
                <span className={`px-3 py-1 rounded-full text-xs font-medium ${statusColors[delivery.status]}`}>
                  {delivery.status.replace(/_/g, ' ')}
                </span>
              </div>

              {delivery.package_description && (
                <p className="text-sm text-gray-600 mb-4">{delivery.package_description}</p>
              )}

              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-500 flex items-center gap-1">
                  <Clock className="w-4 h-4" />
                  {format(new Date(delivery.created_at), 'MMM d, h:mm a')}
                </span>

                {(user?.role === 'security_guard' || user?.role === 'admin') && (
                  <div className="flex gap-2">
                    {delivery.status === 'received_at_gate' && (
                      <button
                        onClick={() => handleStatusUpdate(delivery.id, 'in_transit')}
                        className="px-3 py-1 text-sm bg-purple-100 text-purple-700 rounded-lg hover:bg-purple-200"
                      >
                        In Transit
                      </button>
                    )}
                    {['received_at_gate', 'in_transit'].includes(delivery.status) && (
                      <button
                        onClick={() => handleStatusUpdate(delivery.id, 'delivered')}
                        className="px-3 py-1 text-sm bg-green-100 text-green-700 rounded-lg hover:bg-green-200"
                      >
                        Mark Delivered
                      </button>
                    )}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Create Delivery Modal */}
      {showForm && (
        <div
          className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
          onClick={() => setShowForm(false)}
        >
          <div
            className="bg-white rounded-2xl p-6 max-w-md w-full"
            onClick={(e) => e.stopPropagation()}
          >
            <h2 className="text-xl font-bold mb-6">Register Delivery</h2>
            <form onSubmit={handleCreate} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Resident ID *
                </label>
                <input
                  type="number"
                  value={formData.resident_id}
                  onChange={(e) => setFormData({ ...formData, resident_id: e.target.value })}
                  className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Courier Name
                </label>
                <input
                  type="text"
                  value={formData.courier_name}
                  onChange={(e) => setFormData({ ...formData, courier_name: e.target.value })}
                  className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Courier Company
                </label>
                <input
                  type="text"
                  value={formData.courier_company}
                  onChange={(e) => setFormData({ ...formData, courier_company: e.target.value })}
                  className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500"
                  placeholder="Amazon, Flipkart, etc."
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Tracking Number
                </label>
                <input
                  type="text"
                  value={formData.tracking_number}
                  onChange={(e) => setFormData({ ...formData, tracking_number: e.target.value })}
                  className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Package Description
                </label>
                <textarea
                  value={formData.package_description}
                  onChange={(e) => setFormData({ ...formData, package_description: e.target.value })}
                  className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500"
                  rows={2}
                />
              </div>
              <div className="flex gap-3 pt-2">
                <button
                  type="button"
                  onClick={() => setShowForm(false)}
                  className="flex-1 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
                >
                  Register
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Deliveries;
