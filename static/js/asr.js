const recordButton = document.getElementById('record_button');
const textButton = document.getElementByID('text_button');

let recorder;
let audio;
let isRecord = true;
let boost_dict = null;

const recordAudio = () =>
    new Promise(async resolve => {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const mediaRecorder = new MediaRecorder(stream);
        let audioChunks = [];

        mediaRecorder.addEventListener('dataavailable', event => {
            audioChunks.push(event.data);
        });

        const start = () => {
            audioChunks = [];
            mediaRecorder.start();
        };

        const stop = () =>
            new Promise(resolve => {
                mediaRecorder.addEventListener('stop', () => {
                    const audioBlob = new Blob(audioChunks);
                    const audioUrl = URL.createObjectURL(audioBlob);
                    const audio = new Audio(audioUrl);
                    const play = () => audio.play();
                    resolve({ audioChunks, audioBlob, audioUrl, play });
                });
                mediaRecorder.stop();
            });

        resolve({ start, stop });
    });

recordButton.addEventListener('click', async () => {
    if (isRecord) {
        // Recording...
        isRecord = !isRecord;
        //recordButton.setAttribute('class', 'pulse pulse-animation');
        //recordIcon.setAttribute('class', 'fa fa-square fa-3x fa_custom');

        if (!recorder) {
            recorder = await recordAudio();
        }
        recorder.start();
    } else {
        // Stop
        isRecord = !isRecord;
        //recordButton.setAttribute('class', 'pulse');
        //recordIcon.setAttribute('class', 'fa fa-microphone fa-4x fa_custom');

        audio = await recorder.stop();

        saveAndInference();
    }
});

const saveAndInference = () => {

  const reader = new FileReader();
  reader.readAsDataURL(audio.audioBlob);
  reader.onload = () => {
      const url = '/record'
      const base64AudioMessage = reader.result.split(',')[1];

      fetch(url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
              record: base64AudioMessage,
          })
      })
          .then(processResponse)
          .then(data => {
              let results = data['result'];
              let result_list = [];
              for (let i = 0, result; i < results.length; i++) {
                  result = results[i];
                  result_list.push(result);
              }
          })
  };
};

const processResponse = (res) => {
    if (res.status !== 201) {
        throw new Error(res.status)
    }
    return res.json()
};

function textButtonFunc() {
    alert ('hihi')
}
