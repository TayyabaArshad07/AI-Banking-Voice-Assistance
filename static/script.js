// Elements
const form = document.getElementById("audioForm");
const fileInput = document.getElementById("audio");
const fileName = document.getElementById("file-name");

const recordBtn = document.getElementById("recordBtn");
const audioPreview = document.getElementById("audioPreview");

let mediaRecorder = null;
let audioChunks = [];
let recordedBlob = null;

// File Selection

fileInput.addEventListener("change", function () {

    if (this.files.length > 0) {

        fileName.textContent = this.files[0].name;

        recordedBlob = null;

        audioPreview.pause();
        audioPreview.style.display = "none";
    }

});

// Record Audio

recordBtn.addEventListener("click", async () => {

    try {

        if (!mediaRecorder || mediaRecorder.state === "inactive") {

            const stream = await navigator.mediaDevices.getUserMedia({
                audio: true
            });

            mediaRecorder = new MediaRecorder(stream);

            audioChunks = [];

            mediaRecorder.ondataavailable = (event) => {

                if (event.data.size > 0) {

                    audioChunks.push(event.data);

                }

            };

            mediaRecorder.onstop = () => {

                recordedBlob = new Blob(audioChunks, {
                    type: "audio/webm"
                });

                const url = URL.createObjectURL(recordedBlob);

                audioPreview.src = url;
                audioPreview.style.display = "block";

                fileName.textContent = "Recorded Audio";

                recordBtn.textContent = "🎤 Start Recording";
                recordBtn.classList.remove("recording");

            };

            mediaRecorder.start();

            recordBtn.textContent = "⏹ Stop Recording";
            recordBtn.classList.add("recording");

        }

        else {

            mediaRecorder.stop();

        }

    }

    catch (err) {

        alert("Microphone permission denied.");

        console.error(err);

    }

});

// Upload

form.addEventListener("submit", function (e) {

    // If user selected a file,
    // allow normal form submission

    if (fileInput.files.length > 0) {

        audioPreview.pause();
        audioPreview.style.display = "none";

        return;
    }

    // If user recorded audio

    if (recordedBlob) {

        const recordedFile = new File(

            [recordedBlob],

            "recording.webm",

            {

                type: "audio/webm"

            }

        );

        const dataTransfer = new DataTransfer();

        dataTransfer.items.add(recordedFile);

        fileInput.files = dataTransfer.files;

        audioPreview.pause();
        audioPreview.style.display = "none";

        return;
    }

    e.preventDefault();

    alert("Please choose or record an audio.");

});