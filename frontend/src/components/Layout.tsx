import { useNavigate, useLocation } from 'react-router-dom';
import type { ReactNode } from 'react';

interface LayoutProps {
  children: ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  return (
    <div className="layout">
      <Sidebar />
      <main className="main-content">
        {children}
      </main>
    </div>
  );
}

interface NavItemData {
  id: string;
  label: string;
  icon: string;
  path: string;
}

const NAV_ITEMS: NavItemData[] = [
  {
    id: 'dashboard',
    label: 'Dashboard',
    icon: 'M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z',
    path: '/'
  },
  {
    id: 'data-view',
    label: 'Data View',
    icon: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z',
    path: '/data-view'
  },
  {
    id: 'data-management',
    label: 'Data Management',
    icon: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z',
    path: '/data-management'
  }
];

function Sidebar() {
  const navigate = useNavigate();
  const location = useLocation();

  const handleNavClick = (path: string) => {
    navigate(path);
  };

  const getActiveItem = () => {
    const currentItem = NAV_ITEMS.find(item => item.path === location.pathname);
    return currentItem?.id || 'dashboard';
  };

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h2 className="sidebar-title">AI TIMETABLE</h2>
        <p className="sidebar-subtitle">RESOURCE ALLOCATOR</p>
      </div>

      <nav className="sidebar-nav">
        {NAV_ITEMS.map((item) => (
          <button
            key={item.id}
            className={`nav-item ${getActiveItem() === item.id ? 'active' : ''}`}
            onClick={() => handleNavClick(item.path)}
            aria-label={item.label}
            title={item.label}
          >
            <svg className="nav-icon" fill="currentColor" viewBox="0 0 20 20">
              <path d={item.icon} fillRule="evenodd" clipRule="evenodd" />
            </svg>
            <span>{item.label}</span>
          </button>
        ))}
      </nav>

      <div className="sidebar-footer">
        <div className="sidebar-info">
          <p className="version">v1.0.0</p>
          <p className="copyright">© 2026 AI TIMETABLE RESOURCE ALLOCATOR</p>
        </div>
      </div>
    </aside>
  );
}