import { NotificationProvider } from './context/NotificationContext';
import { NotificationBell } from '../../../project/frontend/the-graveyard-shift/src/components/notifications/NotificationBell';
import { ToastContainer } from '../../../project/frontend/the-graveyard-shift/src/components/notifications/ToastContainer';

function App() {
  return (
    <NotificationProvider>
      <div className="app">
        <NotificationBell />
        <ToastContainer />
        {/* ...existing code... */}
      </div>
    </NotificationProvider>
  );
}

export default App;