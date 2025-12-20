import { ForgotPassword } from "../../features/auth/ui/ForgotPassword/ForgotPassword";

export const ForgotPasswordPage = () => {
  return (
    <div className="auth-page">
      <div className="auth-page__card">
        <h1 className="auth-page__title">Восстановление пароля</h1>
        <ForgotPassword />
      </div>
    </div>
  );
};
