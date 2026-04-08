import './styles/MenuItem.css';

export default function MenuItem({ item }) {
  return (
    <div className="menu-item">
      <div className="item-header">
        <h3>{item.item_name}</h3>
        <span className="price">${item.price.toFixed(2)}</span>
      </div>
      <p className="description">{item.description}</p>
      <button className="add-to-cart-btn">Add to Cart</button>
    </div>
  );
}
