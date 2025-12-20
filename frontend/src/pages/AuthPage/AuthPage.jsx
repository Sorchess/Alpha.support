import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../app/providers/AuthProvider";
import { LoginForm } from "../../features/auth/ui/LoginForm/LoginForm";
import { RegisterForm } from "../../features/auth/ui/RegisterForm/RegisterForm";
import "./AuthPage.scss";

export const AuthPage = () => {
  const navigate = useNavigate();
  const { isAuthenticated, isLoading } = useAuth();

  // 'login' | 'register'
  const [activeTab, setActiveTab] = useState("login");

  // Проверка: если уже залогинен, то редирект на профиль
  useEffect(() => {
    if (!isLoading && isAuthenticated) {
      navigate("/profile");
    }
  }, [isLoading, isAuthenticated, navigate]);

  return (
    <div className="auth-page">
      <div className="auth-page__card">
        <h1 className="auth-page__title">
          {activeTab === "login" ? "Вход в систему" : "Регистрация"}
        </h1>
        <div className="auth-page__tabs">
          <button
            type="button"
            className={`auth-page__tab ${
              activeTab === "login" ? "auth-page__tab--active" : ""
            }`}
            onClick={() => setActiveTab("login")}
          >
            Вход
          </button>
          <button
            type="button"
            className={`auth-page__tab ${
              activeTab === "register" ? "auth-page__tab--active" : ""
            }`}
            onClick={() => setActiveTab("register")}
          >
            Регистрация
          </button>
        </div>
        <div className="auth-page__content">
          {activeTab === "login" ? (
            <LoginForm
              onSwitchToRegister={() => setActiveTab("register")}
            />
          ) : (
            <RegisterForm
              onSwitchToLogin={() => setActiveTab("login")}
            />
          )}
        </div>
      </div>
    </div>
  );
};
