export async function request(url, options = {}) {
  const isFormData = options.body instanceof FormData;

  const headers = {
    ...(isFormData ? {} : { "Content-Type": "application/json" }),
    ...(options.headers || {}),
  };

  const res = await fetch(url, {
    ...options,
    credentials: "include",
    headers,
  });

  const json = await res.json().catch(() => null);

  if (!res.ok) {
    const message = json?.detail || json?.message || "Ошибка запроса";
    return {
      ok: false,
      data: null,
      error: message,
      status: res.status,
    };
  }

  return {
    ok: true,
    data: json?.data ?? json,
    error: null,
    status: res.status,
  };
}
