import { createContext, useContext, useState, useEffect, useMemo } from "react";

// Функкции работы с пользователем и авторизацией
import {
  signIn,
  signUp,
  getMe,
  logout as apiLogout,
} from "../../entities/user/api/userApi";

// Создаём контекст авторизации
const AuthContext = createContext(null);

// Хук для удобного доступа к контексту из любого приложения
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth должен использоваться внутри AuthProvider");
  }
  return context;
};

// Провайдер - оборачивает всё приложение
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  // При первом рендере проверяем, есть ли сохранённая сессия
  useEffect(() => {
    let isMounted = true;

    const loadUser = async () => {
      try {
        const me = await getMe(); // null если не авторизован
        if (isMounted) setUser(me);
      } catch (e) {
        // Если сервер не запущен/500 — просто считаем что сессии нет
        if (isMounted) setUser(null);
      } finally {
        if (isMounted) setIsLoading(false);
      }
    };

    loadUser();

    return () => {
      isMounted = false;
    };
  }, []);

  // Функция входа: POST /api/users/sign-in
  const login = async ({ email, password }) => {
    setIsLoading(true);
    try {
      const loggedUser = await signIn({ email, password });
      setUser(loggedUser);
      return { ok: true, user: loggedUser };
    } catch (error) {
      setUser(null);
      return {
        ok: false,
        error: error?.message || "Не удалось войти",
      };
    } finally {
      setIsLoading(false);
    }
  };

  // Функиция регистрациии: POST /api/users/sign-up
  const register = async ({ email, password }) => {
    setIsLoading(true);
    try {
      // Регистрируем пользователя
      await signUp({ email, password });
      // Сразу логиним с теми же данными
      const loggedUser = await signIn({ email, password });
      setUser(loggedUser);
      return { ok: true, user: loggedUser };
    } catch (error) {
      setUser(null);
      return {
        ok: false,
        error: error?.message || "Не удалось зарегистрироваться",
      };
    } finally {
      setIsLoading(false);
    }
  };

  // Функция выхода: очищает данные пользователя
  const logout = async () => {
    setIsLoading(true);

    try {
      await apiLogout();
    } catch (error) {
      console.error("Ошибка выхода: ", error);
    } finally {
      setUser(null);
      setIsLoading(false);
    }
  };

  // Функция обновления данных пользователя
  const updateUser = (newData) => {
    setUser((prev) => (prev ? { ...prev, ...newData } : prev));
  };

  // То, что будет доступно через useAuth()
  const value = useMemo(
    () => ({
      user,
      isLoading,
      isAuthenticated: !!user,
      login,
      register,
      logout,
      updateUser,
    }),
    [user, isLoading]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
