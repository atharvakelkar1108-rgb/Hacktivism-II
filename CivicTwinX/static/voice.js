function startVoice() {
  const recognition = new webkitSpeechRecognition();
  recognition.lang = 'en-US';
  recognition.start();
  recognition.onresult = (event) => {
    const command = event.results[0][0].transcript.toLowerCase();
    if (command.includes("analyze")) predict();
    else speak("Please provide civic parameters first.");
  };
}

function speak(text) {
  const synth = window.speechSynthesis;
  const utter = new SpeechSynthesisUtterance(text);
  utter.pitch = 1;
  utter.rate = 1;
  utter.volume = 1;
  synth.speak(utter);
}
