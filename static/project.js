document.addEventListener("DOMContentLoaded", function() {
    const videoElement = document.getElementById("videoElement");
    const startButton = document.getElementById("startButton");
    const stopButton = document.getElementById("stopButton");
    let stream;

    startButton.addEventListener("click", startAttendance);
    stopButton.addEventListener("click", stopAttendance);

    async function startAttendance() {
        try {
            stream = await navigator.mediaDevices.getUserMedia({ video: true });
            videoElement.srcObject = stream;
            startButton.disabled = true;
            stopButton.disabled = false;
        } catch (error) {
            console.error("Error starting webcam:", error);
        }
    }

    function stopAttendance() {
        if (stream) {
            const tracks = stream.getTracks();
            tracks.forEach(track => track.stop());
            videoElement.srcObject = null;
            startButton.disabled = false;
            stopButton.disabled = true;
        }
    }
});
