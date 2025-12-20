import { request } from "../../../shared/api/request";

function assertOk(result) {
  if (result.ok) return result;
  const err = new Error(result.error || "Ошибка запроса");
  err.status = result.status;
  throw err;
}

// Регистрация
export async function signUp(payload) {
  const result = await request("/api/users/sign-up", {
    method: "POST",
    body: JSON.stringify(payload),
  });

  assertOk(result);
  return result.data;
}

// Логин
export async function signIn(payload) {
  const result = await request("/api/users/sign-in", {
    method: "POST",
    body: JSON.stringify(payload),
  });

  assertOk(result);
  return result.data;
}

// Получаем текущего пользователя по cookie
export async function getMe() {
  const result = await request("/api/users/me", {
    method: "GET",
  });
  assertOk(result);
  return result.data;
}

// Логаут
export async function logout() {
  const result = await request("/api/users/logout", {
    method: "POST",
  });
  assertOk(result);
  return result;
}

// Обновление профиля (email / password / username)
export async function updateProfile(payload) {
  // payload: {email?, password?, username?}
  const result = await request("/api/users/edit/", {
    method: "POST",
    body: JSON.stringify(payload),
  });
  assertOk(result);
  return result;
}

// Смена аватара
export async function changeAvatar(file) {
  const formData = new FormData();
  formData.append("file", file);

  const result = request("/api/users/change-avatar", {
    method: "PATCH",
    body: formData,
  });
  assertOk(result);
  return result.data;
}
