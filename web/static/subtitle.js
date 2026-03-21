// javascript
const wsUrl = (location.protocol === "https:" ? "wss://" : "ws://") + location.host + "/ws";
let ws_sub = new WebSocket(wsUrl);

ws_sub.onopen = () => {
  console.log("字幕 WebSocket 已连接");
};

ws_sub.onmessage = (e) => {
  let data;
  try {
    data = JSON.parse(e.data);
  } catch (err) {
    console.error("解析 WebSocket 数据失败:", err);
    return;
  }
  if (!data) return;

  const el = document.getElementById("subtitle");
  if (!el) return;

  // 使用 textContent 更安全，确保是字符串回退为空字符串
  el.textContent = typeof data.subtitle === "string" ? data.subtitle : (data.subtitle ?? "");
};

ws_sub.onerror = (e) => {
  console.error("字幕 WebSocket 错误", e);
};

ws_sub.onclose = (e) => {
  console.log("字幕 WebSocket 已关闭", e);
};
