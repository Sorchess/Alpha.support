// Возможные статусы обращения
export const ticketStatus = {
  new: "new",
  in_progress: "in_progress",
  resolved: "resolved",
};

// Читаемые названия статусов
export const ticketStatusLabels = {
  [ticketStatus.new]: "Новое",
  [ticketStatus.in_progress]: "В работе",
  [ticketStatus.resolved]: "Решено",
};

// Цвета для каждого статуса
export const ticketStatusColors = {
  [ticketStatus.new]: "blue",
  [ticketStatus.in_progress]: "orange",
  [ticketStatus.resolved]: "green",
};
