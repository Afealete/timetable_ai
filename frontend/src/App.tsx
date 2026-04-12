import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import DataManagementPage from "./pages/DataManagementPage";
import DataViewPage from "./pages/DataViewPage";
import ErrorBoundary from "./components/ErrorBoundary";
import Layout from "./components/Layout";

function App() {
  return (
    <ErrorBoundary>
      <Router>
        <Layout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/data-management" element={<DataManagementPage />} />
            <Route path="/data-view" element={<DataViewPage />} />
          </Routes>
        </Layout>
      </Router>
    </ErrorBoundary>
  );
}

export default App;