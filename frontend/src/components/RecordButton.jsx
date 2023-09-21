import PropTypes from 'prop-types'

function RecordButton({ type, onClick }) {
    return (
        <button onClick={onClick} className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mr-4">
            Start {type.charAt(0).toUpperCase() + type.slice(1)} Recording
        </button>
    )
}

RecordButton.propTypes = {
    type: PropTypes.oneOf(['audio', 'video']).isRequired,
    onClick: PropTypes.func.isRequired
}

export default RecordButton
