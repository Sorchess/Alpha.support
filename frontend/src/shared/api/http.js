const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:5173";

// Общая функция запросов к backend'у
export async function apiRequest(path, options = {}) {
  const url = `${API_BASE_URL}${path}`;

  const { method = "GET", headers = {}, body } = options;

  const fetchOptions = {
    method,
    headers: {
      "Content-Type": "application/json",
      ...headers,
    },
    // Для cookie-сессии
    credentials: "include",
  };

  // Тело запроса только для методов с body
  if (body !== undefined && body != null) {
    fetchOptions.body = body instanceof FormData ? body : JSON.stringify(body);
    // Если отправляем FormData (файлы) - убераем Content-Type
    if (body instanceof FormData) {
      delete fetchOptions.headers("Content-Type");
    }
  }

  const response = await fetch(url, fetchOptions);

  // Парсинг json
  let data;
  try {
    data = await response.json();
  } catch {
    data = null;
  }

  // Обработка ошибки по данным запроса
  if (!response.ok) {
    const error = new Error(
      data?.message || data?.detail || `Request failed with ${response.status}`
    );
    error.status = response.status;
    error.payload = data;
    throw error;
  }

  return data;
}
