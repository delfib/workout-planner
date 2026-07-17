import styles from "./ExerciseCard.module.css";
import type { Exercise } from "../../types/exercise";

interface Props {
    exercise: Exercise;
}

function ExerciseCard({ exercise }: Props) {
    return (
        <div className={styles.exerciseCard}>
            <h3>{exercise.name}</h3>
            <p>{exercise.category}</p>
        </div>
    );
}

export default ExerciseCard;