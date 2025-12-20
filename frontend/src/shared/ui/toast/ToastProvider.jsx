import {
  Children,
  createContext,
  useContext,
  useMemo,
  useRef,
  useState,
} from "react";
import "./toast.scss";

const ToastContext = createContext(null);

export const useToast = () => {
  const ctx = useContext(ToastContext);
  if (!ctx)
    throw new error("useToast должен использоваться внутри ToastProvider");
  return ctx;
};

export const ToastProvider = ({ children }) => {
  const [toasts, setToasts] = useState([]);
  const idRef = useRef(0);

  const api = useMemo(() => {
    const show = (type, message, options = {}) => {
      const id = ++idRef.current;
      const toast = {
        id,
        type, // success | error | info
        message,
        ttl: options.ttl ?? 3500,
      };

      setToasts((prev) => [...prev, toast]);

      window.setTimeout(() => {
        setToasts((prev) => prev.filter((t) => t.id !== id));
      }, toast.ttl);

      return id;
    };

    return {
      success: (msg, opt) => show("success", msg, opt),
      error: (msg, opt) => show("error", msg, opt),
      info: (msg, opt) => show("info", msg, opt),
    };
  }, []);

  return (
    <ToastContext.Provider value={api}>
      {children}

      <div className="toast-stack" aria-live="polite" aria-relevant="additions">
        {toasts.map((t) => (
          <div key={t.id} className={`toast toast--${t.type}`}>
            <div className="toast__body">{t.message}</div>
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
};
