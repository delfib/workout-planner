import styles from "./WorkoutDayCard.module.css";
import type { WorkoutDay } from "../../types/workoutDay";

interface Props {
    weekDay: string;
    workoutDay?: WorkoutDay;
}

function WorkoutDayCard({ weekDay, workoutDay }: Props) {
    return (
        <div className={styles.dayCard}>
            <h3>{weekDay}</h3>
            {workoutDay ? (
                <div className={styles.workoutCard}>
                    <p>{workoutDay.workout.name}</p>
                </div>
            ) : (
                <div className={styles.placeholder}>
                    <p>+ Add Workout</p>
                </div>
            )}
        </div>
    );
}

export default WorkoutDayCard;