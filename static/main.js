// Check if API is supported
if (
  "SpeechRecognition" in window ||
  "webkitSpeechRecognition" in window ||
  "mozSpeechRecognition" in window ||
  "msSpeechRecognition" in window
) {
  // speech recognition API supported
  var recognition = new (window.SpeechRecognition ||
    window.webkitSpeechRecognition ||
    window.mozSpeechRecognition ||
    window.msSpeechRecognition)();
} else {
  // speech recognition API not supported
  console.error("Sorry, Speech Recognition is not supported in your browser.");
  document.querySelector(".error").style.display = "block";
  document.querySelector(".start").style.display = "none";
}

// Speech Recognition config
recognition.continuous = true;
let result = '';

// On result event


// On recognize event
recognition.onresult = (event) => {
  // Get the current transcript
  const current = event.resultIndex;
  const transcript = event.results[current][0].transcript;
  result = transcript;
  document.querySelector(".command").innerHTML += transcript;
}	


// Declaring elements
const start = document.querySelector(".start"),
  main = document.querySelector(".container"),
  icon = document.querySelector(".fa-microphone");

start.addEventListener("click", function() {
  // Show bot
  main.style.display = "flex";
  this.style.display = "none";

  // Start recognizing
  recognition.start();
});

const apiCall = async () => {
  const res = await fetch(`/api/chat?q=${result}`);
  const arrayBuffer = await res.arrayBuffer();
  const blob = new Blob([arrayBuffer], { type: "audio/wav" });
  const audio = new Audio(URL.createObjectURL(blob));
  audio.play();
  recognition.start();
};

icon.addEventListener("click", async function() {
	  // Stop recognizing
	  recognition.stop();
	  await apiCall();
	})

// Animating microphone while recording
recognition.onstart = () => {
  icon.classList.add("listening");
};
recognition.onend = () => {
  icon.classList.remove("listening");
};
