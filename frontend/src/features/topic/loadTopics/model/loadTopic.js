import { topicApi } from "../../../../entities/topic";
import { topicStatusStorage } from "../../../../entities/topic/model/topicStatusStorage";

export async function loadTopics() {
  const res = await topicApi.getTopics();

  if (!res.ok) {
    return res; // { ok: false, error, status}
  }

  const list = Array.isArray(res.data) ? res.data : [];

  // Гарантируем дефолтный статус
  list.forEach((t) => topicStatusStorage.ensure(t.oid));

  return {
    ...res,
    data: list,
  };
}
