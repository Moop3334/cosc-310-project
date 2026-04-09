import './styles/ReviewList.css';

export default function ReviewList({ reviews }) {
  if (!reviews || reviews.length === 0) {
    return <p className="no-reviews">No reviews yet.</p>;
  }

  const renderStars = (rating) => {
    return (
      <span className="review-stars">
        {[1, 2, 3, 4, 5].map((star) => (
          <span key={star} className={`star-display ${star <= rating ? 'filled' : ''}`}>
            ★
          </span>
        ))}
      </span>
    );
  };

  return (
    <div className="review-list">
      {reviews.map((review) => (
        <div key={review.id} className="review-card">
          <div className="review-card-header">
            <span className="review-item-label">{review.item_name}</span>
            {renderStars(review.rating)}
          </div>
          {review.comment && (
            <p className="review-comment-text">{review.comment}</p>
          )}
          <span className="review-date">
            {new Date(review.created_at).toLocaleDateString()}
          </span>
        </div>
      ))}
    </div>
  );
}
