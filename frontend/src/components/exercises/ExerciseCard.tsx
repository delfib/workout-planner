import axios from "axios";
import styles from "./ExerciseCard.module.css";
import { deleteExercise } from "../../services/exerciseService";
import type { Exercise } from "../../types/exercise";

interface Props {
    exercise: Exercise;
    onDeleted: () => void;
}

function ExerciseCard({ exercise, onDeleted }: Props) {
    
    const handleDelete = async () => {
        if (!window.confirm(`Delete "${exercise.name}"?`)) {
            return;
        }
        try {
            await deleteExercise(exercise.id);
            onDeleted();
        } catch (error) {
            if (axios.isAxiosError(error)) {
                alert(
                    error.response?.data?.error || "Something went wrong."
                );
            } else {
                alert("Something went wrong.");
            }
        }
    };

    return (
        <div className={styles.exerciseCard}>
            <h3>{exercise.name}</h3>
            <p>{exercise.category}</p>
            <button onClick={handleDelete}>
                Delete
            </button>
        </div>
    );
}

export default ExerciseCard;