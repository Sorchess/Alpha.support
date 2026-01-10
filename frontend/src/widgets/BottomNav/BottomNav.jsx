import { useLocation, useNavigate } from "react-router-dom";
import "./BottomNav.scss";

// Конфигурация пунктов меню
const navItems = [
  { path: "/tickets", label: "Обращение", icon: "☰" },
  { path: "/tickets/create", label: "Создать", icon: "＋" },
  { path: "/metrics", label: "Метрики", icon: "📊" },
  { path: "/profile", label: "Профиль", icon: "👤" },
];

export const BottomNav = () => {
  const location = useLocation(); // Текущий url
  const navigate = useNavigate(); // Функция перехода

  return (
    <nav className="bottom-nav">
      {navItems.map((item) => {
        const isActive =
          location.pathname === item.path ||
          location.pathname.startsWith(item.path + "/");

        return (
          <button
            key={item.path}
            type="button"
            className={`bottom-nav__item ${
              isActive ? "bottom-nav__item--active" : ""
            }`}
            onClick={() => navigate(item.path)}
          >
            <span className="bottom-nav__icon">{item.icon}</span>
            <span className="bottom-nav__label">{item.label}</span>
          </button>
        );
      })}
    </nav>
  );
};
