const $ = (selector) => document.querySelector(selector)

const useSpeechRecognition = () => {
  let speechRecognizer = window.SpeechRecognition || window.webkitSpeechRecognition
  
  if (!speechRecognizer) {
	return {
	  supported: false
	}
  }

  speechRecognizer = new speechRecognizer()
  speechRecognizer.lang = 'es-MX'
  speechRecognizer.continuous = true;
  speechRecognizer.interimResults = false;
	
  return {
	supported: true,
	recognition: speechRecognizer
	  }	

}

const { supported, recognition } = useSpeechRecognition()

if (!supported) {
	  alert('Speech Recognition is not supported in this browser')
}

const start = () => {
	$('#result').innerHTML = ''
	$('#start').disabled = true
	$('#stop').disabled = false
	  recognition.start()
}

const stop = async() => {
	  $('#start').disabled = false	
	  $('#stop').disabled = true
	  let result = $('#result').innerHTML
	  const res = await fetch(`/api/chat?q=${result}`)
	  const arrayBuffer = await res.arrayBuffer()
	  const blob = new Blob([arrayBuffer], { type: 'audio/wav' })
	  const audio = new Audio(URL.createObjectURL(blob))
	  audio.play()
	  $('#result').innerHTML = '...'
	  recognition.stop()
		
	}


const onResult = (event) => {
	    let results = event.results
		let result = results[results.length - 1]
		let text = result[0].transcript
		$('#result').innerHTML += text
}


recognition.addEventListener('result', onResult)

$('#start').addEventListener('click', start)
$('#stop').addEventListener('click', stop)