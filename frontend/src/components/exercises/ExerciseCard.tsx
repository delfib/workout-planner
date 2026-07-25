import axios from "axios";
import styles from "./ExerciseCard.module.css";
import { deleteExercise } from "../../services/exerciseService";
import type { Exercise } from "../../types/exercise";
import trashCanIcon from "../../assets/trash-can.svg";

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
            <div className={styles.header}>
                <h3>{exercise.name}</h3>
                <button
                    className={styles.deleteButton}
                    onClick={handleDelete}
                    title="Delete exercise"
                >
                    <img src={trashCanIcon} alt="Delete" />
                </button>
            </div>

            <span className={`${styles.category} ${styles[exercise.category.toLowerCase()]}`} >
                {exercise.category}
            </span>
        </div>
    );
}

export default ExerciseCard;