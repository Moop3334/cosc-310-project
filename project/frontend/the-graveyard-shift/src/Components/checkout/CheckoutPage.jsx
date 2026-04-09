import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { cartAPI, orderAPI, paymentAPI } from '../../services/api';
import './styles/CheckoutPage.css';

export default function CheckoutPage() {
  const [cart, setCart] = useState(null);
  const [cartSummary, setCartSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const [orderId, setOrderId] = useState(null);

  const navigate = useNavigate();
  const userId = localStorage.getItem('userId');

  // Payment form state
  const [paymentData, setPaymentData] = useState({
    cardNumber: '',
    expiryDate: '',
    cvv: '',
    cardholderName: ''
  });

  const [formErrors, setFormErrors] = useState({});

  useEffect(() => {
    const isAuthenticated = Boolean(userId && userId.trim());
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }
    fetchCartData();
  }, [userId, navigate]);

  const fetchCartData = async () => {
    try {
      setLoading(true);
      setError(null);

      const cartData = await cartAPI.getCart(userId);
      if (!cartData || !cartData.items || cartData.items.length === 0) {
        setError('Your cart is empty. Please add items before checkout.');
        return;
      }

      setCart(cartData);
      const summaryData = await cartAPI.getCartSummary(userId);
      setCartSummary(summaryData);
    } catch (err) {
      setError(err.message || 'Failed to load cart data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const validatePaymentForm = () => {
    const errors = {};

    // Card number validation (16 digits)
    const cardNumber = paymentData.cardNumber.replace(/\s/g, '');
    if (!/^\d{16}$/.test(cardNumber)) {
      errors.cardNumber = 'Card number must be 16 digits';
    }

    // Expiry date validation (MM/YY format)
    if (!/^(0[1-9]|1[0-2])\/\d{2}$/.test(paymentData.expiryDate)) {
      errors.expiryDate = 'Expiry date must be in MM/YY format';
    } else {
      const [month, year] = paymentData.expiryDate.split('/');
      const currentDate = new Date();
      const currentYear = currentDate.getFullYear() % 100;
      const currentMonth = currentDate.getMonth() + 1;

      if (parseInt(year) < currentYear || (parseInt(year) === currentYear && parseInt(month) < currentMonth)) {
        errors.expiryDate = 'Card has expired';
      }
    }

    // CVV validation (3-4 digits)
    if (!/^\d{3,4}$/.test(paymentData.cvv)) {
      errors.cvv = 'CVV must be 3 or 4 digits';
    }

    // Cardholder name validation
    if (!paymentData.cardholderName.trim()) {
      errors.cardholderName = 'Cardholder name is required';
    }

    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const formatCardNumber = (value) => {
    const v = value.replace(/\s+/g, '').replace(/[^0-9]/gi, '');
    const matches = v.match(/\d{4,16}/g);
    const match = matches && matches[0] || '';
    const parts = [];
    for (let i = 0, len = match.length; i < len; i += 4) {
      parts.push(match.substring(i, i + 4));
    }
    if (parts.length) {
      return parts.join(' ');
    } else {
      return v;
    }
  };

  const formatExpiryDate = (value) => {
    const v = value.replace(/\D/g, '');
    if (v.length >= 2) {
      return v.substring(0, 2) + '/' + v.substring(2, 4);
    }
    return v;
  };

  const handlePaymentInputChange = (e) => {
    const { name, value } = e.target;
    let formattedValue = value;

    if (name === 'cardNumber') {
      formattedValue = formatCardNumber(value);
    } else if (name === 'expiryDate') {
      formattedValue = formatExpiryDate(value);
    } else if (name === 'cvv') {
      formattedValue = value.replace(/\D/g, '').substring(0, 4);
    }

    setPaymentData(prev => ({
      ...prev,
      [name]: formattedValue
    }));

    // Clear error for this field when user starts typing
    if (formErrors[name]) {
      setFormErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const handleSubmitPayment = async (e) => {
    e.preventDefault();

    if (!validatePaymentForm()) {
      return;
    }

    if (!cart || !cartSummary) {
      setError('Cart data is not available');
      return;
    }

    try {
      setProcessing(true);
      setError(null);

      // Prepare payment data
      const paymentPayload = {
        cardNumber: paymentData.cardNumber.replace(/\s/g, ''),
        expiryDate: paymentData.expiryDate,
        cvv: paymentData.cvv,
        cardholderName: paymentData.cardholderName,
        total: cartSummary.total_with_fees
      };

      // Process payment first
      await paymentAPI.processPayment(paymentPayload);

      // If payment succeeds, create the order
      const order = await orderAPI.checkout(userId);

      setOrderId(order.id);
      setSuccess(true);

    } catch (err) {
      setError(err.message || 'Payment failed. Please try again.');
      console.error('Checkout error:', err);
    } finally {
      setProcessing(false);
    }
  };

  if (loading) {
    return (
      <div className="checkout-container">
        <div className="loading">Loading checkout...</div>
      </div>
    );
  }

  if (error && !cart) {
    return (
      <div className="checkout-container">
        <div className="checkout-header">
          <h1>Checkout</h1>
          <button className="back-btn" onClick={() => navigate('/cart')}>
            ← Back to Cart
          </button>
        </div>
        <div className="error-message">{error}</div>
        <button className="continue-btn" onClick={() => navigate('/restaurants')}>
          Continue Shopping
        </button>
      </div>
    );
  }

  if (success) {
    return (
      <div className="checkout-container">
        <div className="success-screen">
          <div className="success-icon">✓</div>
          <h1>Order Placed Successfully!</h1>
          <p>Your order #{orderId} has been confirmed.</p>
          <p>You will receive a confirmation email shortly.</p>
          <div className="success-actions">
            <button className="orders-btn" onClick={() => navigate('/orders')}>
              View My Orders
            </button>
            <button className="continue-btn" onClick={() => navigate('/restaurants')}>
              Continue Shopping
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="checkout-container">
      <div className="checkout-header">
        <h1>Checkout</h1>
        <button className="back-btn" onClick={() => navigate('/cart')}>
          ← Back to Cart
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="checkout-content">
        <div className="order-summary-section">
          <div className="summary-card">
            <h3>Order Summary</h3>

            <div className="order-items">
              {cart.items.map((item) => (
                <div key={item.item_id} className="order-item">
                  <div className="item-info">
                    <span className="item-name">{item.item_name}</span>
                    <span className="item-quantity">×{item.quantity}</span>
                  </div>
                  <span className="item-price">${(item.price * item.quantity).toFixed(2)}</span>
                </div>
              ))}
            </div>

            <div className="summary-divider"></div>

            <div className="summary-row">
              <span>Subtotal:</span>
              <span>${cartSummary.subtotal?.toFixed(2) || '0.00'}</span>
            </div>

            <div className="summary-row">
              <span>Tax (5%):</span>
              <span>${cartSummary.tax?.toFixed(2) || '0.00'}</span>
            </div>

            <div className="summary-row">
              <span>Delivery Fee:</span>
              <span>${cartSummary.delivery_fee?.toFixed(2) || '0.00'}</span>
            </div>

            <div className="summary-row total">
              <span>Total:</span>
              <span>${cartSummary.total_with_fees?.toFixed(2) || '0.00'}</span>
            </div>
          </div>
        </div>

        <div className="payment-section">
          <div className="payment-card">
            <h3>Payment Information</h3>

            <form onSubmit={handleSubmitPayment} className="payment-form">
              <div className="form-group">
                <label htmlFor="cardholderName">Cardholder Name</label>
                <input
                  type="text"
                  id="cardholderName"
                  name="cardholderName"
                  value={paymentData.cardholderName}
                  onChange={handlePaymentInputChange}
                  placeholder="John Doe"
                  required
                  disabled={processing}
                />
                {formErrors.cardholderName && <span className="field-error">{formErrors.cardholderName}</span>}
              </div>

              <div className="form-group">
                <label htmlFor="cardNumber">Card Number</label>
                <input
                  type="text"
                  id="cardNumber"
                  name="cardNumber"
                  value={paymentData.cardNumber}
                  onChange={handlePaymentInputChange}
                  placeholder="1234 5678 9012 3456"
                  maxLength="19"
                  required
                  disabled={processing}
                />
                {formErrors.cardNumber && <span className="field-error">{formErrors.cardNumber}</span>}
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="expiryDate">Expiry Date</label>
                  <input
                    type="text"
                    id="expiryDate"
                    name="expiryDate"
                    value={paymentData.expiryDate}
                    onChange={handlePaymentInputChange}
                    placeholder="MM/YY"
                    maxLength="5"
                    required
                    disabled={processing}
                  />
                  {formErrors.expiryDate && <span className="field-error">{formErrors.expiryDate}</span>}
                </div>

                <div className="form-group">
                  <label htmlFor="cvv">CVV</label>
                  <input
                    type="text"
                    id="cvv"
                    name="cvv"
                    value={paymentData.cvv}
                    onChange={handlePaymentInputChange}
                    placeholder="123"
                    maxLength="4"
                    required
                    disabled={processing}
                  />
                  {formErrors.cvv && <span className="field-error">{formErrors.cvv}</span>}
                </div>
              </div>

              <button
                type="submit"
                className="pay-btn"
                disabled={processing}
              >
                {processing ? 'Processing...' : `Pay $${cartSummary.total_with_fees?.toFixed(2) || '0.00'}`}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}