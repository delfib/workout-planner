interface Props {
    day: string;
    onClose: () => void;
}

function CreateWorkoutModal({day, onClose,}: Props) {
    return (
        <div>
            <h2>{day}</h2>

            <h3>Create New Workout</h3>

            <input
                placeholder="Workout name"
            />

            <button>
                Create
            </button>

            <hr />

            <h3>Already have one?</h3>

            <select>
                <option>
                    Select workout...
                </option>
            </select>

            <button>
                Assign
            </button>

            <button onClick={onClose}>
                Close
            </button>
        </div>
    );
}

export default CreateWorkoutModal;