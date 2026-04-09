import { useState } from 'react';
import { reviewAPI } from '../../services/api';
import './styles/ReviewForm.css';

export default function ReviewForm({ order, onReviewSubmitted, existingReviews }) {
  const [reviews, setReviews] = useState({});
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const userId = localStorage.getItem('userId');

  const isItemReviewed = (itemId) => {
    return existingReviews?.some(
      (r) => r.order_id === order.id && r.item_id === itemId
    );
  };

  const handleRatingChange = (itemId, rating) => {
    setReviews((prev) => ({
      ...prev,
      [itemId]: { ...prev[itemId], rating },
    }));
  };

  const handleCommentChange = (itemId, comment) => {
    setReviews((prev) => ({
      ...prev,
      [itemId]: { ...prev[itemId], comment },
    }));
  };

  const handleSubmit = async (item) => {
    const reviewData = reviews[item.item_id];
    if (!reviewData?.rating) {
      setError('Please select a rating.');
      return;
    }

    setSubmitting(true);
    setError('');
    setSuccess('');

    try {
      await reviewAPI.createReview(userId, {
        restaurant_id: order.restaurant_id,
        order_id: order.id,
        item_id: item.item_id,
        item_name: item.item_name,
        rating: reviewData.rating,
        comment: reviewData.comment || '',
      });
      setSuccess(`Review for "${item.item_name}" submitted!`);
      if (onReviewSubmitted) onReviewSubmitted();
    } catch (err) {
      setError(err.message || 'Failed to submit review.');
    } finally {
      setSubmitting(false);
    }
  };

  const renderStars = (itemId) => {
    const currentRating = reviews[itemId]?.rating || 0;
    return (
      <div className="star-rating">
        {[1, 2, 3, 4, 5].map((star) => (
          <button
            key={star}
            type="button"
            className={`star ${star <= currentRating ? 'filled' : ''}`}
            onClick={() => handleRatingChange(itemId, star)}
          >
            ★
          </button>
        ))}
      </div>
    );
  };

  if (!order.items || order.items.length === 0) {
    return null;
  }

  return (
    <div className="review-form-container">
      <h3 className="review-form-title">Review Items</h3>
      {error && <div className="review-error">{error}</div>}
      {success && <div className="review-success">{success}</div>}

      {order.items.map((item) => (
        <div key={item.item_id} className="review-item">
          <div className="review-item-header">
            <span className="review-item-name">{item.item_name}</span>
          </div>

          {isItemReviewed(item.item_id) ? (
            <p className="already-reviewed">Reviewed</p>
          ) : (
            <div className="review-item-form">
              {renderStars(item.item_id)}
              <textarea
                className="review-comment"
                placeholder="Write a comment (optional)..."
                value={reviews[item.item_id]?.comment || ''}
                onChange={(e) => handleCommentChange(item.item_id, e.target.value)}
                rows={2}
              />
              <button
                className="submit-review-btn"
                onClick={() => handleSubmit(item)}
                disabled={submitting || !reviews[item.item_id]?.rating}
              >
                {submitting ? 'Submitting...' : 'Submit Review'}
              </button>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
