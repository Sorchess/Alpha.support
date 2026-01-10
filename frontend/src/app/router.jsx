import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { useAuth } from "./providers/AuthProvider";

import { AuthPage } from "../pages/AuthPage/AuthPage";
import { ProfilePage } from "../pages/ProfilePage/ProfilePage";
import { ForgotPasswordPage } from "../pages/ForgotPasswordPage/ForgotPasswordPage";
import { TicketsPage } from "../pages/TicketsPage/TicketsPage";
import { TicketDetailPage } from "../pages/TicketDetailPage/TicketDetailPage";
import { CreateTicketPage } from "../pages/CreateTicketPage/CreateTicketPage";
import { MetricsPage } from "../pages/MetricsPage/MetricsPage";

const RequireAuth = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    // Позже можно заменить на красивый FullPageLoader
    return (
      <div
        style={{ minHeight: "100vh", display: "grid", placeItems: "center" }}
      >
        Загрузка...
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/auth" replace />;
  }

  return children;
};

export const AppRouter = () => (
  <BrowserRouter>
    <Routes>
      {/* Корень редиректит на /auth */}
      <Route path="/" element={<Navigate to="/auth" replace />} />

      {/* Авторизация */}
      <Route path="/auth" element={<AuthPage />} />
      <Route path="/auth/forgot" element={<ForgotPasswordPage />} />

      {/* Защищённые страницы (проверка внутри каждой) */}
      <Route
        path="/profile"
        element={
          <RequireAuth>
            <ProfilePage />
          </RequireAuth>
        }
      />
      <Route
        path="/tickets"
        element={
          <RequireAuth>
            <TicketsPage />
          </RequireAuth>
        }
      />
      <Route
        path="/tickets/:topicOid"
        element={
          <RequireAuth>
            <TicketDetailPage />
          </RequireAuth>
        }
      />
      <Route
        path="/tickets/create"
        element={
          <RequireAuth>
            <CreateTicketPage />
          </RequireAuth>
        }
      />
      <Route
        path="/metrics"
        element={
          <RequireAuth>
            <MetricsPage />
          </RequireAuth>
        }
      />

      {/* Любой другой путь → на авторизацию */}
      <Route path="*" element={<Navigate to="/auth" replace />} />
    </Routes>
  </BrowserRouter>
);
