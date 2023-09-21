import { useRef, useEffect } from 'react';
import { useReactMediaRecorder } from 'react-media-recorder';
import PropTypes from 'prop-types';

import RecordButton from './RecordButton';
import StatusDisplay from './StatusDisplay';
import StopButton from './StopButton';

function Recorder({ type, onRecordingStop }) {
    const {
        status,
        startRecording,
        stopRecording,
        mediaBlobUrl,
        previewStream
    } = useReactMediaRecorder({ video: type !== 'audio', audio: true });

    const videoRef = useRef(null);
    
    useEffect(() => {
        const currentVideoRef = videoRef.current;
        if (currentVideoRef && previewStream) {
            currentVideoRef.srcObject = previewStream;
        }
        return () => {
            if (currentVideoRef) {
                currentVideoRef.srcObject = null;
            }
        };
    }, [previewStream]);

    const handleStop = () => {
        if (onRecordingStop) {
            onRecordingStop(mediaBlobUrl);
        }
        stopRecording();
    };

    return (
        <div className="bg-darkContent p-5 rounded shadow-lg">
            <StatusDisplay status={status} type={type} />

            <div className="flex space-x-4 mt-4">
                <RecordButton type={type} onClick={startRecording} />
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
