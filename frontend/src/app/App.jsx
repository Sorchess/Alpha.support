import { AppRouter } from "./router.jsx";
import { AuthProvider } from "./providers/AuthProvider";
import { ToastProvider } from "../shared/ui/toast/ToastProvider";

export const App = () => {
  return (
    <ToastProvider>
      <AuthProvider>
        <AppRouter />
      </AuthProvider>
    </ToastProvider>
  );
};
