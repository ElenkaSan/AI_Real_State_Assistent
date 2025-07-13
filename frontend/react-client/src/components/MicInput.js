import React, { useState, useRef, useEffect } from 'react';

export default function MicInput({ onTranscript }) {
  const [recording, setRecording] = useState(false);
  const [volume, setVolume] = useState(0);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const analyserRef = useRef(null);
  const animationFrameRef = useRef(null);
  const audioContextRef = useRef(null);
  const sourceRef = useRef(null);

  const startRecording = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorderRef.current = new MediaRecorder(stream);
    audioChunksRef.current = [];

    // waveform setup
    audioContextRef.current = new AudioContext();
    sourceRef.current = audioContextRef.current.createMediaStreamSource(stream);
    analyserRef.current = audioContextRef.current.createAnalyser();
    analyserRef.current.fftSize = 256;
    sourceRef.current.connect(analyserRef.current);

    const bufferLength = analyserRef.current.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);

    const animate = () => {
      analyserRef.current.getByteFrequencyData(dataArray);
      const avg = dataArray.reduce((a, b) => a + b, 0) / bufferLength;
      setVolume(avg);
      animationFrameRef.current = requestAnimationFrame(animate);
    };
    animate();

    mediaRecorderRef.current.ondataavailable = (event) => {
      audioChunksRef.current.push(event.data);
    };

    mediaRecorderRef.current.onstop = async () => {
  cancelAnimationFrame(animationFrameRef.current);

  if (audioContextRef.current && audioContextRef.current.state !== 'closed') {
    await audioContextRef.current.close();
  }

  const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
  const formData = new FormData();
  formData.append('audio', audioBlob, 'voice.wav');

  try {
    const res = await fetch(`${process.env.REACT_APP_API_URL}/speak`, {
      method: 'POST',
      body: formData,
    });
    const data = await res.json();
    onTranscript(data.text);
  } catch (error) {
    console.error('Error processing audio:', error);
  }
};


    mediaRecorderRef.current.start();
    setRecording(true);
  };

  const stopRecording = () => {
    mediaRecorderRef.current.stop();
    setRecording(false);
  };

  useEffect(() => {
  return () => {
    cancelAnimationFrame(animationFrameRef.current);
    if (audioContextRef.current && audioContextRef.current.state !== 'closed') {
      audioContextRef.current.close();
    }
  };
}, []);

  return (
    <div className="d-flex flex-column align-items-center mt-3 w-100">
      <div className="w-100 mb-3 px-3">
        <div className="progress" style={{ height: '10px' }}>
          <div
            className="progress-bar bg-secondary"
            role="progressbar"
            style={{ width: `${Math.min(volume, 100)}%`, transition: 'width 0.1s linear' }}
            aria-valuenow={Math.floor(volume)}
            aria-valuemin="0"
            aria-valuemax="100"
          />
        </div>
      </div>
      <div className="d-flex gap-2">
        <button className="btn btn-dark" onClick={startRecording} disabled={recording}>
          <i className="bi bi-mic-fill"></i> Start
        </button>
        <button className="btn btn-danger" onClick={stopRecording} disabled={!recording}>
          <i className="bi bi-stop-fill"></i> Stop
        </button>
      </div>
    </div>
  );
}
