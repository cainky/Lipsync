import { useEffect } from 'react';
import Recorder from './components/Recorder';
import { useState } from 'react';
import axios from 'axios';

function App() {
    const [activeRecorder, setActiveRecorder] = useState(null);
    const [audioURL, setAudioURL] = useState(null);
    const [videoURL, setVideoURL] = useState(null);
    const [mergedVideoURL, setMergedVideoURL] = useState(null);

    const [errorMessage, setErrorMessage] = useState(null);

    useEffect(() => {
        // Cleanup function
        return () => {
            if (audioURL) URL.revokeObjectURL(audioURL);
            if (videoURL) URL.revokeObjectURL(videoURL);
        };
    }, [audioURL, videoURL]);
    
    const handleMerge = async () => {
        if (!audioURL || !videoURL) {
            setErrorMessage("Both audio and video recordings are required for merging.");
            return;
        }
    
        // Convert blob URLs to actual blobs
        const audioBlob = await fetch(audioURL).then(res => res.blob());
        const videoBlob = await fetch(videoURL).then(res => res.blob());
    
        const formData = new FormData();
        formData.append("audio", audioBlob, "audio.webm");
        formData.append("video", videoBlob, "video.webm");
    
        try {
            const response = await axios.post('/api/merge', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            console.log("Backend Response:", response.data);
    
            setMergedVideoURL(response.data.videoPath);
            // Revoke the blob URLs after successful upload to free up memory
            URL.revokeObjectURL(audioURL);
            URL.revokeObjectURL(videoURL);
        } catch (error) {
            console.error("Error during merging:", error);
            setErrorMessage("An error occurred during merging. Please try again.");
        }
    }

    const handleStartRecording = (type) => {
        setActiveRecorder(type);
    };
    

    const handleRecordingStop = (type, url) => {
        if (type === 'audio') {
            setAudioURL(url);
        } else if (type === 'video') {
            setVideoURL(url);
        }
        setActiveRecorder(null);
    };

    return (
        <div className="min-h-screen bg-darkBg text-darkText flex">
            {/* Side Menu */}
            <div className="w-1/5 min-w-xs bg-darkSidebar p-8 shadow-md">
                <h1 className="text-2xl font-bold mb-6">Lipsync App</h1>
                {/* Placeholder for menu items */}
                <div>
                    <p className="text-gray-300 mb-4"></p>
                    <p className="text-gray-300 mb-4"></p>
                </div>
            </div>

            {/* Main Content */}
            <div className="flex-1 p-8">
                <div className="bg-darkContent rounded-lg shadow-md p-8 w-full">
                    <div className="flex flex-col md:flex-row space-y-4 md:space-y-0 md:space-x-4 mb-6">
                        <button 
                            onClick={() => {
                                setErrorMessage(null);
                                handleStartRecording('audio');
                            }}
                            className="bg-secondary hover:bg-secondary-hover text-white font-bold py-2 px-4 rounded"
                        >
                            Audio Recording
                        </button>

                        <button 
                            onClick={() => {
                                setErrorMessage(null);
                                handleStartRecording('video');
                            }}
                            className="bg-secondary hover:bg-secondary-hover text-white font-bold py-2 px-4 rounded"
                        >
                            Video Recording
                        </button>
                        <button 
                            onClick={handleMerge}
                            className="bg-success hover:bg-success-hover text-white font-bold py-2 px-4 rounded"
                        >
                            Merge Recordings
                        </button>
                    </div>

                    {activeRecorder && 
                        <Recorder 
                            type={activeRecorder} 
                            onRecordingStop={(url) => handleRecordingStop(activeRecorder, url)}
                        />
                    }

                    {errorMessage && 
                        <div className="mt-4 p-4 bg-red-600 text-white rounded">
                            {errorMessage}
                        </div>
                    }

                    {mergedVideoURL && 
                        <video src={mergedVideoURL} controls autoPlay className="mt-4 rounded w-full" />
                    }
                </div>
            </div>
        </div>
    );
}

export default App;