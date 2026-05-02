const video = document.getElementById("video");
const result = document.getElementById("result");

// Start webcam
navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => {
    video.srcObject = stream;
  });

// Capture frame
function captureFrame() {
  const canvas = document.createElement("canvas");
  canvas.width = 320;
  canvas.height = 240;

  const ctx = canvas.getContext("2d");
  ctx.drawImage(video, 0, 0, 320, 240);

  return canvas.toDataURL("image/jpeg");
}

// Send frame every 700ms
setInterval(async () => {
  const image = captureFrame();

  const res = await fetch("http://localhost:8000/detect", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ image })
  });

  const data = await res.json();
  updateUI(data);

}, 700);

// Update UI
function updateUI(data) {
  if (data.result === "UNKNOWN") {
    result.innerText = "UNKNOWN 🚨";
    result.className = "unknown";
    sparkles();

  } else if (data.result === "KNOWN") {
    result.innerText = `KNOWN: ${data.name} ✅`;
    result.className = "known";

  } else {
    result.innerText = "No Face";
    result.className = "";
  }
}

// Sparkle effect
function sparkles() {
  for (let i = 0; i < 12; i++) {
    let s = document.createElement("div");
    s.className = "sparkle";
    s.style.left = Math.random() * window.innerWidth + "px";
    s.style.top = Math.random() * window.innerHeight + "px";

    document.body.appendChild(s);
    setTimeout(() => s.remove(), 500);
  }
}
