import { useEffect, useState } from 'react';
import PropTypes from 'prop-types';

function StatusDisplay({ status, type }) {
    const [recordingDuration, setRecordingDuration] = useState(0);

    useEffect(() => {
        if (status === 'recording') {
            const timer = setInterval(() => {
                setRecordingDuration(prev => prev + 1);
            }, 1000);

            return () => clearInterval(timer);
        }
    }, [status]);

    return (
        <div>
            <p className="font-semibold mb-4">{status}</p>
            {type === 'audio' && status === 'recording' && (
                <div className="relative">
                    <div className="mb-4 font-medium text-blue-600">
                        Recording Duration: {recordingDuration} seconds
                    </div>
                    <div className="h-2 bg-gray-200 rounded">
                        <div 
                            style={{ width: `${(recordingDuration % 60) * 1.6667}%` }} 
                            className="h-2 bg-blue-600 rounded"
                        ></div>
                    </div>
                </div>
            )}
        </div>
    );
}

StatusDisplay.propTypes = {
    status: PropTypes.string.isRequired,
    type: PropTypes.oneOf(['audio', 'video']).isRequired
};

export default StatusDisplay;
