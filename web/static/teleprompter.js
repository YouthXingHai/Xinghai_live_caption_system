let ws = new WebSocket("ws://" + location.host + "/ws");

ws.onmessage = (e) => {
  let data;
  try {
    data = JSON.parse(e.data);
  } catch (err) {
    return;
  }

  const currentEl = document.getElementById("current");
  const nextEl = document.getElementById("next");

  // 更新当前行（若不存在则跳过）
  if (currentEl) {
    const text = typeof data.current === "string" ? data.current : (data.prompt ?? "");
    currentEl.textContent = text;

    // 如果使用 left:50% 居中，补偿左侧间距（若定义了 CSS 变量）
    try {
      const comp = getComputedStyle(currentEl);
      if (comp.left === "50%") {
        currentEl.style.transform = "translateX(calc(-50% + var(--side-padding)))";
      }
    } catch (err) { /* 忽略 */ }
  }

  // 更新后续行列表（若不存在则跳过）
  if (nextEl) {
    nextEl.innerHTML = "";
    const items = Array.isArray(data.next) ? data.next : (data.next != null ? [data.next] : []);
    items.forEach((it) => {
      const div = document.createElement("div");
      div.textContent = it ?? "";
      nextEl.appendChild(div);
    });
  }
};