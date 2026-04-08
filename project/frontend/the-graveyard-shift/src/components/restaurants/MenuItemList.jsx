import MenuItem from './MenuItem';
import './styles/MenuItemList.css';

export default function MenuItemList({ items, restaurantId, onAddSuccess }) {
  return (
    <div className="menu-item-list">
      <div className="items-grid">
        {items.map((item) => (
          <MenuItem 
            key={item.id} 
            item={item}
            restaurantId={restaurantId}
            onAddSuccess={onAddSuccess}
          />
        ))}
      </div>
    </div>
  );
}
