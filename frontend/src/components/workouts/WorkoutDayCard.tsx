import styles from "./WorkoutDayCard.module.css";
import type { WorkoutDay } from "../../types/workoutDay";

interface Props {
    weekDay: string;
    workoutDay?: WorkoutDay;
    onAddWorkout: (weekDay: string) => void;
}

function WorkoutDayCard({weekDay, workoutDay, onAddWorkout}: Props) {
    return (
        <div className={styles.dayCard}>
            <h3 className={styles.dayTitle}>
                {weekDay}
            </h3>
            {workoutDay ? (
                <div className={styles.workoutCard}>
                    <p>{workoutDay.workout.name}</p>
                </div>
            ) : (
                <div
                    className={styles.placeholder}
                    onClick={() => onAddWorkout(weekDay)}
                >
                    <p>+ Add Workout</p>
                </div>
            )}
        </div>
    );
}

export default WorkoutDayCard;