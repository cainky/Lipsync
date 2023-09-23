import { useEffect } from 'react';
import Recorder from './components/Recorder';
import { useState } from 'react';
import axios from 'axios';
import ProgressBar from './components/ProgressBar';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000';

function App() {
    const [activeRecorder, setActiveRecorder] = useState(null);
    const [audioURL, setAudioURL] = useState(null);
    const [videoURL, setVideoURL] = useState(null);
    const [audioBlob, setAudioBlob] = useState(null);
    const [videoBlob, setVideoBlob] = useState(null);
    const [mergedVideoURL, setMergedVideoURL] = useState(null);

    const [audioSuccess, setAudioSuccess] = useState(false);
    const [videoSuccess, setVideoSuccess] = useState(false);
    const [mergeSuccess, setMergeSuccess] = useState(false);
    const [errorMessage, setErrorMessage] = useState(null);
    const [progress, setProgress] = useState(0);
    const [showProgressBar, setShowProgressBar] = useState(false);



    useEffect(() => {
        // Cleanup function
        return () => {
            if (audioURL) URL.revokeObjectURL(audioURL);
            if (videoURL) URL.revokeObjectURL(videoURL);
        };
    }, [audioURL, videoURL]);
    
    const [progressInterval, setProgressInterval] = useState(null);

    const AVERAGE_TIME = 10000; // 10 seconds for example
    const UPDATE_INTERVAL = 100; // update every 100ms
    const MAX_SIMULATED_PROGRESS = 100; // The progress will stop at 100%

    const simulateProgressBar = () => {
        setShowProgressBar(true);
        let elapsed = 0;
        const interval = setInterval(() => {
            elapsed += UPDATE_INTERVAL;
            const currentProgress = parseFloat(((elapsed / AVERAGE_TIME) * 100).toFixed(2));
            
            // Stop updating progress at MAX_SIMULATED_PROGRESS
            if (currentProgress >= MAX_SIMULATED_PROGRESS) {
                clearInterval(interval);
                setProgress(MAX_SIMULATED_PROGRESS);
            } else {
                setProgress(currentProgress);
            }
    
        }, UPDATE_INTERVAL);
        setProgressInterval(interval);
    }
    
    useEffect(() => {
        return () => {
            if(progressInterval) clearInterval(progressInterval);
        };
    }, [progressInterval]);


    const handleMerge = async () => {
        if (!audioBlob || !videoBlob) {
            setErrorMessage("Both audio and video recordings are required for merging.");
            return;
        }
        simulateProgressBar();
        setMergeSuccess(false);
        
        const formData = new FormData();
        formData.append("audio", audioBlob, "audio.webm");
        formData.append("video", videoBlob, "video.webm");
    
        try {
            const response = await axios.post(BACKEND_URL+'/api/merge', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            
            setMergeSuccess(true);
            console.log("Backend Response:", response.data);
            setMergedVideoURL(BACKEND_URL+response.data.videoPath);

            if(progressInterval) clearInterval(progressInterval);  
            setProgress(0);
            setShowProgressBar(false);
    
            // Revoke the blob URLs after successful upload to free up memory
            // URL.revokeObjectURL(audioURL);
            // URL.revokeObjectURL(videoURL);
        } catch (error) {
            console.error("Error during merging:", error);
            if(progressInterval) clearInterval(progressInterval);
            setProgress(0);
            setShowProgressBar(false);
            setErrorMessage("An error occurred during merging. Please try again.");
        }        
    };
    

    const handleStartRecording = (type) => {
        setProgress(0);
        setMergeSuccess(false);
        setActiveRecorder(type);
        setAudioSuccess(false);
        setVideoSuccess(false);
        setMergedVideoURL(null);
    };
    

    const handleStopRecording = (type, blob) => {
        const blobURL = URL.createObjectURL(blob);
        if (type === 'audio') {
            setAudioURL(blobURL);
            setAudioBlob(blob);
            setAudioSuccess(true);
            setVideoSuccess(false);
        } else if (type === 'video') {
            setVideoURL(blobURL);
            setVideoBlob(blob);
            setVideoSuccess(true);
            setAudioSuccess(false);
        }
        setActiveRecorder(null);
    };
    
    
    

    return (
        <div className="min-h-screen bg-darkBg text-darkText flex">
            {/* Side Menu */}
            <div className="w-1/5 min-w-xs bg-darkSidebar p-8 shadow-md">
                <h1 className="text-2xl font-bold mb-6">LipSync App</h1>
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
                                setActiveRecorder('audio');
                                setErrorMessage(null);
                                handleStartRecording('audio');
                            }}
                            className="bg-secondary hover:bg-secondary-hover text-white font-bold py-2 px-4 rounded"
                            disabled={progress > 0 && progress < 100}
                        >
                            Audio Recording
                        </button>


                        <button 
                            onClick={() => {
                                setActiveRecorder('video');
                                setErrorMessage(null);
                                handleStartRecording('video');
                            }}
                            className="bg-secondary hover:bg-secondary-hover text-white font-bold py-2 px-4 rounded"
                            disabled={progress > 0 && progress < 100}
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
                            onRecordingStop={(url) => handleStopRecording(activeRecorder, url)}
                        />
                    }

                    {audioSuccess && <div className="mt-4 p-4 bg-green-600 text-white rounded">Audio Recorded Successfully!</div>}
                    {videoSuccess && <div className="mt-4 p-4 bg-green-600 text-white rounded">Video Recorded Successfully!</div>}
                    {mergeSuccess && 
                        <div className="mt-4 p-4 bg-green-600 text-white rounded">
                            Merging completed successfully!
                        </div>
                    }
                    {errorMessage && 
                        <div className="mt-4 p-4 bg-red-600 text-white rounded">
                            {errorMessage}
                        </div>
                    }

                    {showProgressBar && <ProgressBar progress={progress} />}

                    {mergedVideoURL && 
                        <video src={mergedVideoURL} controls autoPlay className="mt-4 rounded w-full" />
                    }
                </div>
            </div>
        </div>
    );
}

export default App;