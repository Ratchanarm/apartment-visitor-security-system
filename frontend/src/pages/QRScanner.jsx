import { useEffect, useState, useRef } from 'react';
import { Html5QrcodeScanner } from 'html5-qrcode';
import { visitorAPI } from '../services/api';
import { QrCode, CheckCircle, XCircle, User, KeyRound } from 'lucide-react';
import toast from 'react-hot-toast';

const QRScanner = () => {
  const [scanResult, setScanResult] = useState(null);
  const [visitor, setVisitor] = useState(null);
  const [otp, setOtp] = useState('');
  const [loading, setLoading] = useState(false);
  const [showOtpInput, setShowOtpInput] = useState(false);
  const scannerRef = useRef(null);

  useEffect(() => {
    const scanner = new Html5QrcodeScanner('qr-reader', {
      qrbox: { width: 250, height: 250 },
      fps: 5,
    });

    scanner.render(onScanSuccess, onScanError);
    scannerRef.current = scanner;

    return () => {
      scanner.clear().catch(console.error);
    };
  }, []);

  const onScanSuccess = async (decodedText) => {
    setScanResult(decodedText);
    
    // Extract token from QR data
    const parts = decodedText.split('|');
    const token = parts.length > 1 ? parts[1] : decodedText;
    
    try {
      const response = await visitorAPI.checkIn({ qr_token: token });
      setVisitor(response.data);
      toast.success(`${response.data.name} checked in!`);
      
      // Clear scanner
      if (scannerRef.current) {
        scannerRef.current.clear();
      }
    } catch (error) {
      if (error.response?.status === 400) {
        // May need OTP verification
        setShowOtpInput(true);
        toast.error('Please enter OTP for verification');
      } else {
        toast.error('Invalid QR code');
      }
    }
  };

  const onScanError = (error) => {
    // Ignore scan errors (no QR in view)
  };

  const handleOtpVerify = async () => {
    if (!otp || otp.length !== 6) {
      toast.error('Please enter a valid 6-digit OTP');
      return;
    }

    setLoading(true);
    try {
      const parts = scanResult?.split('|') || [];
      const token = parts.length > 1 ? parts[1] : scanResult;
      
      const response = await visitorAPI.checkIn({
        qr_token: token,
        otp: otp,
      });
      setVisitor(response.data);
      toast.success(`${response.data.name} checked in!`);
      setShowOtpInput(false);
    } catch (error) {
      toast.error('Invalid OTP');
    } finally {
      setLoading(false);
    }
  };

  const resetScanner = () => {
    setScanResult(null);
    setVisitor(null);
    setOtp('');
    setShowOtpInput(false);
    
    // Reinitialize scanner
    const scanner = new Html5QrcodeScanner('qr-reader', {
      qrbox: { width: 250, height: 250 },
      fps: 5,
    });
    scanner.render(onScanSuccess, onScanError);
    scannerRef.current = scanner;
  };

  return (
    <div className="max-w-lg mx-auto">
      <h1 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
        <QrCode className="w-7 h-7" />
        QR Scanner
      </h1>

      {visitor ? (
        <div className="bg-white rounded-2xl shadow-sm border p-6 text-center">
          <div className="w-20 h-20 rounded-full bg-green-100 flex items-center justify-center mx-auto mb-4">
            <CheckCircle className="w-10 h-10 text-green-600" />
          </div>
          <h2 className="text-xl font-bold text-gray-900 mb-2">Check-in Successful!</h2>
          <div className="bg-gray-50 rounded-lg p-4 mb-6">
            <div className="flex items-center justify-center gap-3 mb-2">
              <div className="w-12 h-12 rounded-full bg-primary-100 flex items-center justify-center">
                <User className="w-6 h-6 text-primary-600" />
              </div>
              <div className="text-left">
                <p className="font-semibold text-gray-900">{visitor.name}</p>
                <p className="text-sm text-gray-500">{visitor.purpose || 'General visit'}</p>
              </div>
            </div>
          </div>
          <button
            onClick={resetScanner}
            className="w-full py-3 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-700"
          >
            Scan Another
          </button>
        </div>
      ) : showOtpInput ? (
        <div className="bg-white rounded-2xl shadow-sm border p-6">
          <div className="text-center mb-6">
            <div className="w-16 h-16 rounded-full bg-blue-100 flex items-center justify-center mx-auto mb-4">
              <KeyRound className="w-8 h-8 text-blue-600" />
            </div>
            <h2 className="text-xl font-bold text-gray-900">Enter OTP</h2>
            <p className="text-gray-500 mt-1">Ask visitor for the OTP sent to their phone</p>
          </div>
          
          <input
            type="text"
            value={otp}
            onChange={(e) => setOtp(e.target.value.replace(/\D/g, '').slice(0, 6))}
            className="w-full text-center text-2xl tracking-widest py-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent mb-4"
            placeholder="000000"
            maxLength={6}
          />
          
          <div className="flex gap-3">
            <button
              onClick={resetScanner}
              className="flex-1 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              onClick={handleOtpVerify}
              disabled={loading || otp.length !== 6}
              className="flex-1 py-3 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-700 disabled:opacity-50"
            >
              {loading ? 'Verifying...' : 'Verify'}
            </button>
          </div>
        </div>
      ) : (
        <div className="bg-white rounded-2xl shadow-sm border p-6">
          <div id="qr-reader" className="overflow-hidden rounded-lg" />
          <p className="text-center text-sm text-gray-500 mt-4">
            Position the QR code within the frame to scan
          </p>
        </div>
      )}
    </div>
  );
};

export default QRScanner;
