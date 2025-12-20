import { useState } from "react";
import { Button } from "../../../../shared/ui/Button/Button";
import { EmailStep } from "./steps/EmailStep";
import { CodeStep } from "./steps/CodeStep";
import { ResetStep } from "./steps/ResetStep";
import "./ForgotPassword.scss";

const stepEmail = "email";
const stepCode = "code";
const stepReset = "reset";

export const ForgotPassword = () => {
  const [step, setStep] = useState(stepEmail);
  const [email, setEmail] = useState("");
  const [code, setCode] = useState("");
  const [resetToken, setResetToken] = useState(null); // resetSessionToken от Backend'а
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Шаг 1 - отправка кода
  const handleSendCode = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const res = await fetch("/api/auth/password/forgot", {
        method: "POST",
        headers: { "Content-type": "application/json" },
        body: JSON.stringify({ email: email.trim() }),
      });
      if (!res.ok) {
        throw new Error("Не удалось отправить код. Проверьте Email.");
      }
      // Чтение message с backend и показ пользователю
      setStep(stepCode);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Шаг 2: проверка кода
  const handleVerifyCode = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const res = await fetch("/api/auth/password/verify-code", {
        method: "POST",
        headers: { "Content-type": "application/json" },
        body: JSON.stringify({ email: email.trim, code: code.trim }),
      });
      if (!res.ok) {
        throw new Error("Неверный или просроченный код");
      }

      const data = await res.json();
      // Backend должен вернуть что-то вроде { resetSessionToken: ...}
      setResetToken(data.resetSessionToken);
      setStep(stepReset);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Шаг 3 - установка нового пароля
  const handleResetPassword = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const res = await fetch("/api/auth/password/reset", {
        method: "POST",
        headers: { "Content-type": "application/json" },
        body: JSON.stringify({
          resetSessionToken: resetToken,
          password: newPassword,
        }),
      });
      if (!res.ok) {
        throw new Error("Не удалось обновить пароль");
      }
      //После успешной смены пароля переход на "/auth"
      window.location.href = "/auth";
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  return (
    <div className="forgot">
      {error && <div className="forgot__error">{error}</div>}

      {step === stepEmail && (
        <EmailStep
          email={email}
          setEmail={setEmail}
          loading={loading}
          onSubmit={handleSendCode}
        />
      )}

      {step === stepCode && (
        <CodeStep
          email={email}
          code={Code}
          setCode={setCode}
          loading={loading}
          onSubmit={handleVerifyCode}
          onBack={() => setStep(setEmail)}
        />
      )}

      {step === stepReset && (
        <ResetStep loading={loading} onSubmit={handleResetPassword} />
      )}
    </div>
  );
};
