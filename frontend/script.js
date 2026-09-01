const camera = document.getElementById("camera");
const canvas = document.getElementById("detectionCanvas");
const startButton = document.getElementById("startButton");
const stopButton = document.getElementById("stopButton");

const cameraPlaceholder = document.getElementById("cameraPlaceholder");
const connectionStatus = document.getElementById("connectionStatus");
const detectionCard = document.getElementById("detectionCard");
const statusIcon = document.getElementById("statusIcon");
const detectionStatus = document.getElementById("detectionStatus");
const detectionMessage = document.getElementById("detectionMessage");
const animalDetails = document.getElementById("animalDetails");
const animalName = document.getElementById("animalName");
const confidence = document.getElementById("confidence");
const severity = document.getElementById("severity");
const alertBox = document.getElementById("alertBox");
const alertTitle = document.getElementById("alertTitle");
const alertMessage = document.getElementById("alertMessage");

const imageUpload = document.getElementById("imageUpload");
const uploadedImage = document.getElementById("uploadedImage");

// Automatically use local backend if running locally, or Render if on cloud
const BACKEND_URL = (
    window.location.hostname === "localhost" ||
    window.location.hostname === "127.0.0.1" ||
    window.location.protocol === "file:" ||
    !window.location.hostname
)
    ? "http://127.0.0.1:5000/detect"
    : "https://crop-suraksha-backend.onrender.com/detect";

let stream = null;
let detectionInterval = null;

if (imageUpload) {
    imageUpload.addEventListener("change", async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        // Stop camera stream if active
        stopMonitoring();

        const reader = new FileReader();
        reader.onload = async (event) => {
            uploadedImage.src = event.target.result;
            uploadedImage.style.display = "block";
            camera.style.display = "none";
            cameraPlaceholder.style.display = "none";

            const img = new Image();
            img.onload = async () => {
                const formData = new FormData();
                formData.append("image", file);

                try {
                    connectionStatus.textContent = "● Analyzing...";
                    connectionStatus.classList.remove("offline");
                    connectionStatus.classList.add("online");

                    const response = await fetch(BACKEND_URL, {
                        method: "POST",
                        body: formData
                    });

                    if (!response.ok) {
                        throw new Error(`Backend returned ${response.status}`);
                    }

                    const result = await response.json();
                    processDetectionResult(result, img.naturalWidth || img.width, img.naturalHeight || img.height);
                    connectionStatus.textContent = "● Detection Complete";

                } catch (err) {
                    console.error("Upload error:", err);
                    alert("Detection error: " + err.message);
                    connectionStatus.textContent = "● Error";
                }
            };
            img.src = event.target.result;
        };
        reader.readAsDataURL(file);
    });
}

startButton.addEventListener("click", async () => {
    if (stream) {
        return;
    }

    uploadedImage.style.display = "none";

    try {
        stream = await navigator.mediaDevices.getUserMedia({
            video: {
                width: 1280,
                height: 720
            },
            audio: false
        });

        camera.srcObject = stream;
        camera.style.display = "block";
        cameraPlaceholder.style.display = "none";

        startButton.disabled = true;
        if (stopButton) {
            stopButton.disabled = false;
        }

        connectionStatus.textContent = "● Monitoring";
        connectionStatus.classList.remove("offline");
        connectionStatus.classList.add("online");

        resetDetection();

        detectionInterval = setInterval(() => {
            sendFrameToBackend();
        }, 1000);

    } catch (error) {
        console.error("Camera error:", error);
        alert("Unable to access the camera. Please allow camera permission or use the UPLOAD IMAGE button.");
    }
});

if (stopButton) {
    stopButton.addEventListener("click", () => {
        stopMonitoring();
    });
}

function stopMonitoring() {
    if (detectionInterval) {
        clearInterval(detectionInterval);
        detectionInterval = null;
    }

    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
    }

    camera.srcObject = null;
    camera.style.display = "none";
    uploadedImage.style.display = "none";
    cameraPlaceholder.style.display = "flex";

    startButton.disabled = false;
    if (stopButton) {
        stopButton.disabled = true;
    }

    connectionStatus.textContent = "● Offline";
    connectionStatus.classList.remove("online");
    connectionStatus.classList.add("offline");

    resetDetection();
    clearCanvas();
}

let isProcessing = false;

async function sendFrameToBackend() {
    if (
        isProcessing ||
        !stream ||
        !camera.videoWidth ||
        !camera.videoHeight
    ) {
        return;
    }

    isProcessing = true;

    const tempCanvas = document.createElement("canvas");
    tempCanvas.width = camera.videoWidth;
    tempCanvas.height = camera.videoHeight;

    const context = tempCanvas.getContext("2d");
    context.drawImage(
        camera,
        0,
        0,
        tempCanvas.width,
        tempCanvas.height
    );

    tempCanvas.toBlob(
        async (blob) => {
            if (!blob) {
                isProcessing = false;
                return;
            }

            const formData = new FormData();
            formData.append(
                "image",
                blob,
                "camera_frame.jpg"
            );

            try {
                const response = await fetch(
                    BACKEND_URL,
                    {
                        method: "POST",
                        body: formData
                    }
                );

                if (!response.ok) {
                    throw new Error(
                        `Backend returned ${response.status}`
                    );
                }

                const result = await response.json();
                processDetectionResult(result, camera.videoWidth, camera.videoHeight);

                connectionStatus.textContent = "● Monitoring";
                connectionStatus.classList.remove("offline");
                connectionStatus.classList.add("online");

            } catch (error) {
                console.log(
                    "Backend connection error:",
                    error.message
                );

                connectionStatus.textContent = "● Camera Active";
                connectionStatus.classList.remove("offline");
                connectionStatus.classList.add("online");
            } finally {
                isProcessing = false;
            }
        },
        "image/jpeg",
        0.7
    );
}

function processDetectionResult(result, frameWidth, frameHeight) {
    if (
        !result ||
        !result.success ||
        !result.detections ||
        result.detections.length === 0
    ) {
        resetDetection();
        clearCanvas();
        return;
    }

    const detections = result.detections;
    const topDetection = detections[0];

    // Collect all unique animal names
    const animalNames = [...new Set(detections.map(d => capitalize(d.animal)))].join(", ");
    animalName.textContent = animalNames;

    // Show confidence of top detection
    confidence.textContent = `${Math.round(topDetection.confidence * 100)}%`;

    const alert =
        result.alerts &&
        result.alerts.length > 0
            ? result.alerts[0]
            : null;

    if (alert) {
        severity.textContent = alert.severity || "ALERT";
        alertTitle.textContent = `${capitalize(alert.animal || topDetection.animal)} Detected`;
        alertMessage.textContent = alert.message || "Animal detected!";
        alertBox.classList.remove("hidden");
    }

    detectionStatus.textContent = detections.length > 1
        ? `${detections.length} Animals Detected (${animalNames})`
        : `${capitalize(topDetection.animal)} Detected`;

    detectionMessage.textContent = "Animal detected by the AI model.";

    detectionCard.classList.remove("normal", "warning");
    detectionCard.classList.add("danger");

    statusIcon.textContent = "⚠";
    animalDetails.classList.remove("hidden");

    drawBoundingBoxes(detections, frameWidth, frameHeight);
}

function resetDetection() {
    detectionCard.classList.remove("danger", "warning");
    detectionCard.classList.add("normal");

    statusIcon.textContent = "✓";
    detectionStatus.textContent = "No Animal Detected";
    detectionMessage.textContent = "The monitoring system is ready.";

    animalDetails.classList.add("hidden");
    alertBox.classList.add("hidden");

    animalName.textContent = "—";
    confidence.textContent = "—";
    severity.textContent = "—";

    clearCanvas();
}

function drawBoundingBoxes(detections, frameWidth, frameHeight) {
    if (!detections || detections.length === 0) {
        clearCanvas();
        return;
    }

    const w = frameWidth || camera.videoWidth || 640;
    const h = frameHeight || camera.videoHeight || 480;

    canvas.width = w;
    canvas.height = h;

    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    detections.forEach((det) => {
        const box = det.bounding_box;
        if (!box || box.length !== 4) return;

        const [x1, y1, x2, y2] = box;
        const label = `${capitalize(det.animal)} ${Math.round(det.confidence * 100)}%`;

        ctx.lineWidth = 4;
        ctx.strokeStyle = "#ff3333";
        ctx.strokeRect(x1, y1, x2 - x1, y2 - y1);

        ctx.font = "bold 20px Arial";
        const textWidth = ctx.measureText(label).width;

        ctx.fillStyle = "#ff3333";
        ctx.fillRect(x1, Math.max(0, y1 - 32), textWidth + 16, 32);

        ctx.fillStyle = "white";
        ctx.fillText(label, x1 + 8, Math.max(22, y1 - 9));
    });
}

function clearCanvas() {
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

function capitalize(text) {
    if (!text) {
        return "";
    }
    return text.charAt(0).toUpperCase() + text.slice(1);
}
