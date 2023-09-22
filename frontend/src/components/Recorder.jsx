import { useRef, useEffect, useState } from 'react';
import PropTypes from 'prop-types';

import RecordButton from './RecordButton';
import StatusDisplay from './StatusDisplay';
import StopButton from './StopButton';

function Recorder({ type, onRecordingStop }) {
    const [status, setStatus] = useState("idle");
    const videoRef = useRef(null);
    const [mediaRecorder, setMediaRecorder] = useState(null);
    const [chunks, setChunks] = useState([]);
    const [recordedBlob, setRecordedBlob] = useState(null);
    
    useEffect(() => {
        if (recordedBlob) {
            onRecordingStop(recordedBlob);
        }
    }, [recordedBlob, onRecordingStop]);
    useEffect(() => {
        const constraints = (type === 'video') 
            ? { video: true, audio: true } 
            : { audio: true };
    
        navigator.mediaDevices.getUserMedia(constraints)
            .then(stream => {
                const mimeType = type === 'video' ? 'video/webm' : 'audio/webm';
                const recorder = new MediaRecorder(stream, { mimeType: mimeType });
    
                recorder.ondataavailable = event => {
                    console.log("Data available with size:", event.data.size);
                    setChunks(prev => [...prev, event.data]);
                };
    
                recorder.onstop = () => {
                    // Use functional update to get the latest chunks
                    setChunks(prevChunks => {
                        const blob = new Blob(prevChunks, { type: mimeType });
                        setRecordedBlob(blob);
                        return [];
                    });
                    setStatus("stopped");
                };
    
                recorder.onerror = event => {
                    console.error("MediaRecorder error:", event.error);
                };
    
                setMediaRecorder(recorder);
    
                if (type === 'video') {
                    videoRef.current.srcObject = stream;
                }
            })
            .catch(error => {
                console.error("Error accessing media devices:", error);
            });
    }, [type, onRecordingStop]);
    

    const handleStart = () => {
        if (mediaRecorder) {
            mediaRecorder.start();
            setStatus("recording");
        }
    };

    const handleStop = () => {
        console.log("Stop function called. MediaRecorder state:", mediaRecorder?.state);
        if (mediaRecorder && mediaRecorder.state !== "inactive") {
            mediaRecorder.stop();
            if (type === 'video' && videoRef.current && videoRef.current.srcObject) {
                let stream = videoRef.current.srcObject;
                let tracks = stream.getTracks();
    
                tracks.forEach(function(track) {
                    track.stop();
                });
    
                videoRef.current.srcObject = null;
            }
        }
    };
    

    return (
        <div className="bg-darkContent p-5 rounded shadow-lg">
            <StatusDisplay status={status} type={type} />

            <div className="flex space-x-4 mt-4">
                <RecordButton type={type} onClick={handleStart} />
                <StopButton onClick={handleStop} />
            </div>

            {type === 'video' &&
                <video
                    ref={videoRef}
                    autoPlay muted
                    className="mt-4 rounded w-full"
                />
            }
        </div>
    );
}

Recorder.propTypes = {
    type: PropTypes.oneOf(['audio', 'video']).isRequired,
    onRecordingStop: PropTypes.func.isRequired
};

export default Recorder;
