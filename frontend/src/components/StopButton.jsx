import PropTypes from 'prop-types';

function StopButton({ onClick }) {
    return (
        <button onClick={onClick} className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">
            Stop Recording
        </button>
    );
}

StopButton.propTypes = {
    onClick: PropTypes.func.isRequired
};

export default StopButton;
