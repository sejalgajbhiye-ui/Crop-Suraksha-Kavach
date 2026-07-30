const camera = document.getElementById("camera");

const canvas = document.getElementById("detectionCanvas");

const startButton = document.getElementById("startButton");

const stopButton = document.getElementById("stopButton");

const cameraPlaceholder =
    document.getElementById("cameraPlaceholder");

const connectionStatus =
    document.getElementById("connectionStatus");

const detectionCard =
    document.getElementById("detectionCard");

const statusIcon =
    document.getElementById("statusIcon");

const detectionStatus =
    document.getElementById("detectionStatus");

const detectionMessage =
    document.getElementById("detectionMessage");

const animalDetails =
    document.getElementById("animalDetails");

const animalName =
    document.getElementById("animalName");

const confidence =
    document.getElementById("confidence");

const severity =
    document.getElementById("severity");

const alertBox =
    document.getElementById("alertBox");

const alertTitle =
    document.getElementById("alertTitle");

const alertMessage =
    document.getElementById("alertMessage");


let stream = null;

let detectionInterval = null;

let isRunning = false;


/* =========================
   START CAMERA
========================= */

startButton.addEventListener("click", async () => {

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

        stopButton.disabled = false;


        connectionStatus.textContent = "● Monitoring";

        connectionStatus.classList.remove("offline");

        connectionStatus.classList.add("online");


        isRunning = true;


        resetDetection();


        /*
         * Send a frame to the backend periodically.
         *
         * For now, this function is prepared for the
         * Flask /detect endpoint.
         */

        detectionInterval = setInterval(() => {

            if (isRunning) {

                sendFrameToBackend();

            }

        }, 1000);


    } catch (error) {

        console.error("Camera error:", error);

        alert(
            "Unable to access the camera. Please allow camera permission."
        );

    }

});


/* =========================
   STOP CAMERA
========================= */

stopButton.addEventListener("click", () => {

    stopMonitoring();

});


function stopMonitoring() {

    isRunning = false;


    if (detectionInterval) {

        clearInterval(detectionInterval);

        detectionInterval = null;

    }


    if (stream) {

        stream.getTracks().forEach(track => {

            track.stop();

        });

        stream = null;

    }


    camera.srcObject = null;

    camera.style.display = "none";

    cameraPlaceholder.style.display = "flex";


    startButton.disabled = false;

    stopButton.disabled = true;


    connectionStatus.textContent = "● Offline";

    connectionStatus.classList.remove("online");

    connectionStatus.classList.add("offline");


    resetDetection();

}


/* =========================
   SEND FRAME TO BACKEND
========================= */

async function sendFrameToBackend() {

    if (!camera.videoWidth || !camera.videoHeight) {

        return;

    }


    /*
     * Draw current camera frame onto canvas.
     */

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


    /*
     * Convert image to JPEG blob.
     */

    tempCanvas.toBlob(async (blob) => {

        if (!blob) {

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
                "http://127.0.0.1:5000/detect",
                {
                    method: "POST",
                    body: formData
                }
            );


            if (!response.ok) {

                throw new Error(
                    "Backend request failed"
                );

            }


            const result = await response.json();


            processDetectionResult(result);


        } catch (error) {

            /*
             * Backend may not be running yet.
             *
             * We don't stop the camera.
             */

            console.log(
                "Backend not available:",
                error.message
            );

        }

    }, "image/jpeg", 0.8);

}


/* =========================
   PROCESS YOLO RESULT
========================= */

function processDetectionResult(result) {

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


    const detection =
        result.detections[0];


    const animal =
        detection.animal;


    const confidenceValue =
        detection.confidence;


    animalName.textContent =
        capitalize(animal);


    confidence.textContent =
        `${Math.round(confidenceValue * 100)}%`;


    /*
     * Display alert information.
     */

    const alert =
        result.alerts &&
        result.alerts.length > 0
            ? result.alerts[0]
            : null;


    if (alert) {

        severity.textContent =
            alert.severity || "ALERT";


        alertTitle.textContent =
            `${capitalize(animal)} Detected`;


        alertMessage.textContent =
            alert.message || "Animal detected!";


        alertBox.classList.remove("hidden");

    }


    detectionStatus.textContent =
        `${capitalize(animal)} Detected`;


    detectionMessage.textContent =
        "Animal detected by the AI model.";


    detectionCard.classList.remove(
        "normal",
        "warning"
    );


    detectionCard.classList.add(
        "danger"
    );


    statusIcon.textContent = "⚠";


    animalDetails.classList.remove(
        "hidden"
    );


    /*
     * Draw bounding box.
     */

    drawBoundingBox(
        detection.bounding_box,
        capitalize(animal),
        confidenceValue
    );

}


/* =========================
   RESET DETECTION
========================= */

function resetDetection() {

    detectionCard.classList.remove(
        "danger",
        "warning"
    );


    detectionCard.classList.add(
        "normal"
    );


    statusIcon.textContent = "✓";


    detectionStatus.textContent =
        "No Animal Detected";


    detectionMessage.textContent =
        "The monitoring system is ready.";


    animalDetails.classList.add(
        "hidden"
    );


    alertBox.classList.add(
        "hidden"
    );


    animalName.textContent = "—";

    confidence.textContent = "—";

    severity.textContent = "—";


    clearCanvas();

}


/* =========================
   DRAW BOUNDING BOX
========================= */

function drawBoundingBox(
    box,
    label,
    confidenceValue
) {

    if (!box || box.length !== 4) {

        return;

    }


    const ctx =
        canvas.getContext("2d");


    /*
     * Match canvas dimensions
     * with the actual video.
     */

    canvas.width =
        camera.videoWidth;

    canvas.height =
        camera.videoHeight;


    ctx.clearRect(
        0,
        0,
        canvas.width,
        canvas.height
    );


    const [
        x1,
        y1,
        x2,
        y2
    ] = box;


    ctx.lineWidth = 4;

    ctx.strokeStyle = "#ff3333";

    ctx.strokeRect(
        x1,
        y1,
        x2 - x1,
        y2 - y1
    );


    /*
     * Label background.
     */

    const text =
        `${label} ${Math.round(
            confidenceValue * 100
        )}%`;


    ctx.font =
        "bold 18px Arial";


    const textWidth =
        ctx.measureText(text).width;


    ctx.fillStyle =
        "#ff3333";


    ctx.fillRect(
        x1,
        Math.max(0, y1 - 30),
        textWidth + 16,
        30
    );


    ctx.fillStyle =
        "white";


    ctx.fillText(
        text,
        x1 + 8,
        Math.max(21, y1 - 9)
    );

}


/* =========================
   CLEAR CANVAS
========================= */

function clearCanvas() {

    const ctx =
        canvas.getContext("2d");


    ctx.clearRect(
        0,
        0,
        canvas.width,
        canvas.height
    );

}


/* =========================
   CAPITALIZE
========================= */

function capitalize(text) {

    if (!text) {

        return "";

    }


    return text.charAt(0).toUpperCase()
        + text.slice(1);

}