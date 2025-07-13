import React, { useRef, useState } from 'react';

export default function MicRecorder({ onTranscript }) {
  const [isRecording, setIsRecording] = useState(false);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  const startRecording = async () => {
    setIsRecording(true);
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorderRef.current = new MediaRecorder(stream);

    mediaRecorderRef.current.ondataavailable = (e) => {
      audioChunksRef.current.push(e.data);
    };

    mediaRecorderRef.current.onstop = async () => {
      const blob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
      audioChunksRef.current = [];

      const formData = new FormData();
      formData.append("audio", blob, "voice.wav");

      const res = await fetch(`${process.env.REACT_APP_API_URL}/speak`, {
        method: "POST",
        body: formData
      });

      const data = await res.json();
      onTranscript(data.text);
    };

    mediaRecorderRef.current.start();
  };

  const stopRecording = () => {
    setIsRecording(false);
    mediaRecorderRef.current.stop();
  };

  return (
    <div className="mt-4">
      <button onClick={startRecording} disabled={isRecording}
        className="bg-green-500 text-white px-4 py-2 rounded mr-2">
        🎙 Start
      </button>
      <button onClick={stopRecording} disabled={!isRecording}
        className="bg-red-500 text-white px-4 py-2 rounded">
        ⏹ Stop
      </button>
    </div>
  );
}
