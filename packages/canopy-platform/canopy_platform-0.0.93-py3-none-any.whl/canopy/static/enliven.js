import { _, cookies, go, upgradeLink } from '/static/web.js'

let mode = 'site'
const konamiCode = [38, 38, 40, 40, 37, 39, 37, 39, 66, 65, 13]
const konamiCodeJSON = JSON.stringify(konamiCode)
let konamiCodeFIFO = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

// TODO $.load(...)
document.addEventListener('DOMContentLoaded', ev => {
  microphoneStatus('off')
  listen.onmouseup = initDictation
  join.onmouseup = initChat

  _('a:not(.breakout)').each(upgradeLink)
  history.pushState({scroll: 0}, 'title', window.location)
  window.go = go

  const client = new WebTorrent()
  DragDrop('body', (files, pos, fileList, directories) => {
    console.log(files[0])
    client.seed(files, torrent => {
      console.log(`Client is seeding at:\n${torrent.magnetURI}`)
    })
  })

  if (cookies.get('rhythm') == 'on') {
    document.querySelector('body').style.backgroundImage = 'url(/static/measure.png)'
  }
  cookies.set('mediasoup-demo.user', `{"displayName": "${userName}"}`)

  document.addEventListener('keydown', ev => {
    if (mode == 'room') {
      switch (ev.key) {
        case 'w': break                              // w   TODO walk forward
        case 'a': break                              // a   TODO strafe left
        case 's': break                              // s   TODO walk backward
        case 'd': break                              // d   TODO strafe right
        case 'h': break                              // h   TODO pan left
        case 'j': break                              // j   TODO scroll map down
        case 'k': break                              // k   TODO scroll map up
        case 'l': break                              // l   TODO pan right
      }
      return
    }
    if (ev.target.tagName == 'INPUT' || ev.target.tagName == 'TEXTAREA')
      return
    if (konamiCode.indexOf(ev.keyCode) != -1) {
      konamiCodeFIFO = konamiCodeFIFO.slice(1).concat(ev.keyCode)
      if (JSON.stringify(konamiCodeFIFO) == konamiCodeJSON) {
        return
      }
    }
    if (following) {
      if (ev.key == 'Escape') {
        hideFollowLinks()
        return
      }
      if (['Shift', 'Alt', 'Control', 'Tab'].indexOf(ev.key) != -1)
        return
      followQueue += ev.key.toLowerCase()
      if (followList.hasOwnProperty(followQueue)) {
        go(followList[followQueue])
        hideFollowLinks()
      }
      return
    }
    if (ev.altKey && ev.key == '.') {                // A-. toggle rhythm indicator
      if (cookies.get('rhythm') == 'on') {
        document.querySelector('body').style.backgroundImage = 'none'
        cookies.set('rhythm', 'off')
      } else {
        document.querySelector('body').style.backgroundImage = 'url(/static/measure.png)'
        cookies.set('rhythm', 'on')
      }
    } else {
      switch (ev.key) {
        case '?': goGuide(); break                   // ?   show the site guide
        case 'q': focusQuery(ev); break              // q   focus query input
        case 'f': showKeyboardFollowLinks(); break   // f   show "follow links"
        case 'm': goHome(); break                    // m   go home
        case 'd': close(); break                     // d   close page
        case 'r': reload(); break                    // r   reload page
        case 'h': goBack(); break                    // h   go back
        case 'j': scrollDown(); break                // j   scroll down 3 EMs
        case 'k': scrollUp(); break                  // k   scroll up 3 EMs
        case 'l': goForward(); break                 // l   go forward
        case 'u': goUp(); break                      // u   follow rel=up
        case 'p': goPrevious(); break                // p   follow rel=prev
        case 'n': goNext(); break                    // n   follow rel=next
        case '[': pageUp(); break                    // [   scroll page up
        case ']': pageDown(); break                  // ]   scroll page down
        case '{': scrollTop(); break                 // {   scroll to top
        case '}': scrollBottom(); break              // }   scroll to bottom
      }
    }
  }, false)
})

const em = parseFloat(getComputedStyle(document.documentElement).fontSize)

const showGuide = () => { go('/guide') }
const focusQuery = ev => {
  document.querySelector('input[name=q]').focus()
  ev.preventDefault()
}
const goHome = () => { go(document.querySelector("a[rel=home]").href) }
const close = () => { window.close() }
const reload = () => { window.location.reload() }
const goUp = () => { go(document.querySelector("a[rel=up]").href) }
const goPrevious = () => { go(document.querySelector("a[rel=prev]").href) }
const goNext = () => { go(document.querySelector("a[rel=next]").href) }
const goBack = () => { history.back() }
const goForward = () => { history.forward() }
const scrollDown = () => { document.documentElement.scrollTop += 3 * em }
const scrollUp = () => { document.documentElement.scrollTop -= 3 * em }
const pageUp = () => { document.documentElement.scrollTop -= 15 * em }
const pageDown = () => { document.documentElement.scrollTop += 15 * em }
const scrollTop = () => { document.documentElement.scrollTop = 0 }
const scrollBottom = () => { document.documentElement.scrollTop = 99999 }

let following = false
let followList = {}
let followQueue = ''
const showKeyboardFollowLinks = () => {
  following = true
  const links = document.querySelectorAll('a')
  links.forEach((link, n) => {
    const characters = 'asdfghjkl;'
    const combinationLength = Math.log10(links.length)
    let combination = ''
    while (true) {
      combination = ''
      for (let i = 0; i < combinationLength; i++)
        combination += characters.charAt(Math.floor(Math.random() * characters.length))
      if (!followList.hasOwnProperty(combination)) break
    }
    followList[combination] = link.href
    link.innerHTML = link.innerHTML + `<span class=followlink>${combination}</span>`
  })
}
const showVoiceFollowLinks = () => {
  following = true
  document.querySelectorAll('a').forEach((link, n) => {
    followList[numberToWords(n).replace(' ', '')] = link.href
    link.innerHTML = link.innerHTML + `<span class=followlink>${n}</span>`
  })
}
const hideFollowLinks = () => {
  following = false
  followList = {}
  followQueue = ''
  document.querySelectorAll('.followlink').forEach(e => e.remove())
}

const initDictation = async () => {
  microphoneStatus('loading')
  const partialContainer = document.querySelector('#search .partial')

  const channel = new MessageChannel()
  const model = await Vosk.createModel('/static/vosk-model-small-en-us-0.15.tar.gz')
  model.registerPort(channel.port1)

  const sampleRate = 48000

  const recognizer = new model.KaldiRecognizer(sampleRate)
  recognizer.setWords(true)

  let wakeWord = 'ghost'
  let readyWord = 'Say "ghost help"'
  let state = 'asleep'
  microphoneStatus('on')
  partialContainer.innerHTML = readyWord

  recognizer.on('result', message => {
    let input = message.result.text
    if (following && input != '') {
      let number = input.replace(' ', '')
      if (number == 'for') number = 'four'
      go(followList[number])
      hideFollowLinks()
      return
    }
    if (input.slice(0, wakeWord.length) != wakeWord) {
      partialContainer.innerHTML = readyWord
      return
    }
    input = input.slice(wakeWord.length + 1)
    microphoneStatus('on')
    if (input.endsWith('cancel cancel')) {
      partialContainer.innerHTML = ''
      return
    }
    if (input == 'help') goGuide()                   // help
    else if (input.startsWith('query for')) {        // query for
      const query = input.slice(10)
      document.querySelector('input[name=q]').value = query
      go(`/search?q=${query}`)
    } else if (input.startsWith('go')) {             // go
      switch (input.slice(3)) {
        case 'home': goHome(); break                 //    home
        case 'up': goUp(); break                     //    up
        case 'prev': goPrevious(); break             //    prev
        case 'next': goNext(); break                 //    next
        case 'back': goBack(); break                 //    back
        case 'forward': goForward(); break           //    forward
      }
    } else if (input.startsWith('follow')) {         // follow
      showVoiceFollowLinks()
    } else if (input.startsWith('tell me')) {        // tell me
      const request = input.slice(8)
      const response = fetch('/ai/assistant', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({request: request}),
      })
      .then(response => response.blob())
      .then(blob => {
        const audio = new Audio(URL.createObjectURL(blob));
        audio.addEventListener('canplaythrough', () => {
          state = 'asleep'
          microphoneStatus('on')
          audio.play()
          // partialContainer.value = readyWord
        })
      })
    }
    partialContainer.innerHTML = `${input}`
  })
  recognizer.on('partialresult', message => {
    const input = message.result.partial
    if (input.slice(0, wakeWord.length) != wakeWord || !following)
      return
    state = 'awake'
    microphoneStatus('active')
    partialContainer.innerHTML = input.slice(wakeWord.length)
  })

  const mediaStream = await navigator.mediaDevices.getUserMedia({
    video: false,
    audio: {
      echoCancellation: true,
      noiseSuppression: true,
      channelCount: 1,
      sampleRate
    },
  })

  const audioContext = new AudioContext()
  await audioContext.audioWorklet.addModule('/static/recognizer-processor.js')
  const recognizerProcessor = new AudioWorkletNode(
    audioContext,
    'recognizer-processor',
    { channelCount: 1, numberOfInputs: 1, numberOfOutputs: 1 }
  )
  recognizerProcessor.port.postMessage(
    { action: 'init', recognizerId: recognizer.id },
    [ channel.port2 ]
  )
  recognizerProcessor.connect(audioContext.destination)

  const source = audioContext.createMediaStreamSource(mediaStream)
  source.connect(recognizerProcessor)
}

const initChat = () => {
  join.disabled = true
  join.style.display = 'none'

  const tag = document.createElement('script')
  tag.src = '/chats/mediasoup-demo-app.js'
  document.getElementsByTagName('head')[0].appendChild(tag)

  const autoMuter = setInterval(autoMute, 100)
  const autoMute = () => {
    if (typeof window.CLIENT !== 'undefined' && window.CLIENT._micProducer) {
      window.CLIENT.muteMic()
      clearInterval(autoMuter)
    }
  }
}

const numberToWords = num => {
  if (num === 0)
    return 'zero'
  const units = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
  const teens = ['eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen']
  const tens = ['', 'ten', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']
  const convert = n => {
    if (n === 0) {
      return ''
    } else if (n < 10) {
      return units[n - 1] + ' '
    } else if (n == 10) {
      return 'ten'
    } else if (n < 20) {
      return teens[n - 11] + ' '
    } else if (n < 100) {
      return tens[Math.floor(n / 10)] + ' ' + convert(n % 10)
    } else {
      return units[Math.floor(n / 100)-1] + ' hundred ' + convert(n % 100)
    }
  }
  return convert(num).trim()
}

const microphoneStatus = mode => {
  let color
  let icon
  if (mode == 'on' || mode == 'active') {
    if (mode == 'on')
      color = 'dc322f'
    else if (mode == 'active')
      color = '268bd2'
    icon = `<path d="M7 7.40991C7 6.08383 7.52677 4.81207 8.46445 3.87439C9.40213 2.93671 10.6739 2.40991 12 2.40991C13.3261 2.40991 14.5978 2.93671 15.5355 3.87439C16.4732 4.81207 17 6.08383 17 7.40991V13.4099C17 14.736 16.4732 16.0079 15.5355 16.9456C14.5978 17.8832 13.3261 18.4099 12 18.4099C10.6739 18.4099 9.40213 17.8832 8.46445 16.9456C7.52677 16.0079 7 14.736 7 13.4099V7.40991Z" stroke="#${color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/><path d="M21 13.4099C21 15.7969 20.0518 18.0861 18.364 19.7739C16.6761 21.4618 14.3869 22.4099 12 22.4099C9.61305 22.4099 7.32384 21.4618 5.63602 19.7739C3.94819 18.0861 3 15.7969 3 13.4099" stroke="#${color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>`
  } else if (mode == 'off' || mode == 'loading') {
    if (mode == 'off')
      color = '586e75'
    else if (mode == 'loading')
      color = '6c71c4'
    icon = `<path d="M17.0005 11.24V13C17.0005 14.3261 16.4737 15.5978 15.536 16.5355C14.5983 17.4732 13.3266 18 12.0005 18C11.4846 17.9975 10.972 17.9166 10.4805 17.76" stroke="#${color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/><path d="M8 16C7.35089 15.1345 7 14.0819 7 13V7C7 5.67392 7.52677 4.40216 8.46445 3.46448C9.40213 2.5268 10.6739 2 12 2C13.3261 2 14.5978 2.5268 15.5355 3.46448C16.4732 4.40216 17 5.67392 17 7" stroke="#${color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/><path d="M5.21081 18.84C3.81268 17.216 3.04593 15.1429 3.0508 13" stroke="#${color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/><path d="M21.0007 13C20.9995 14.5822 20.5812 16.1361 19.788 17.5051C18.9948 18.8741 17.8547 20.0098 16.4827 20.7977C15.1107 21.5857 13.5551 21.9979 11.973 21.993C10.3908 21.9882 8.83786 21.5664 7.4707 20.77" stroke="#${color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/><path d="M22 2L2 22" stroke="#${color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>`
  }
  listen.innerHTML = icon
}
