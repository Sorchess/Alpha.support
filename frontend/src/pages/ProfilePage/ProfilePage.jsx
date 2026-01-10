import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../app/providers/AuthProvider";
import { BottomNav } from "../../widgets/BottomNav/BottomNav";
import "./ProfilePage.scss";

export const ProfilePage = () => {
  const navigate = useNavigate();
  const { user, isLoading, isAuthenticated, logout } = useAuth();

  // Если не авторизован, то редирект на "/auth"
  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      navigate("/auth");
    }
  }, [isLoading, isAuthenticated, navigate]);

  // Пока проверяем сессию - показываем загрузку
  if (isLoading) {
    return (
      <div className="profile-page profile-page--loading">
        <p>Загрузка...</p>
      </div>
    );
  }

  if (!user) {
    return null;
  }

  // Обработчик выхода
  const handleLogout = () => {
    logout();
    navigate("/auth");
  };

  return (
    <div className="profile-page">
      {/* Шапка с аватаром и именем */}
      <header className="profile-page__header">
        <div className="profile-page__avatar">
          <span className="profile-page__avatar-text">{user.initials}</span>
        </div>
        <h1 className="profile-page__name">{user.fullName}</h1>
        <p className="profile-page__role">{user.role}</p>
      </header>

      {/* Основной контент */}
      <main className="profile-page__content">
        {/* Карточка контактной информации */}
        <section className="profile-card">
          <h2 className="profile-card__title">Контактная информация</h2>

          <div className="profile-card__row">
            <span className="profile-card__label">Email</span>
            <span className="profile-card__value">{user.email}</span>
          </div>

          <div className="profile-card__row">
            <span className="profile-card__label">Телефон</span>
            <span className="profile-card__value">{user.phone || "-"}</span>
          </div>

          <div className="profile-card__row">
            <span className="profile-card__label">Отдел</span>
            <span className="profile-card__value">{user.department}</span>
          </div>
        </section>

        {/* Карточка настроек */}
        <section className="profile-card">
          <h2 className="profile-card__title">Настройки</h2>

          <ToggleRow label="Статус доступности" />
          <ToggleRow label="Push-уведомления" />
          <ToggleRow label="Email-уведомления" />
        </section>

        {/* Кнопка выхода */}
        <button
          className="profile-page__logout-button"
          type="button"
          onClick={handleLogout}
        >
          Выйти из системы
        </button>
      </main>

      <BottomNav />
    </div>
  );
};

// Компонент переключателя (пока без реального стейта)
const ToggleRow = ({ label }) => {
  return (
    <div className="profile-toggle">
      <span className="profile-toggle__label">{label}</span>
      <label className="profile-toggle__switch">
        <input className="profile-toggle__checkbox" type="checkbox" />
        <span className="profile-toggle__slider" />
      </label>
    </div>
  );
};
