import styles from "./WorkoutDayCard.module.css";
import type { WorkoutDay } from "../../types/workoutDay";
import { getWorkoutColor } from "../../constants/workoutColors";

interface Props {
    weekDay: string;
    workoutDay?: WorkoutDay;
    onAddWorkout: (weekDay: string) => void;
    isSelected: boolean;
}

function WorkoutDayCard({weekDay, workoutDay, onAddWorkout, isSelected}: Props) {
    return (
        <div
            className={
                isSelected
                    ? `${styles.dayCard} ${styles.selected}`
                    : styles.dayCard
            }
        >
            <h3 className={styles.dayTitle}>
                {weekDay}
            </h3>
            {workoutDay ? (
                <div
                    className={styles.workoutCard}
                    style={{
                        backgroundColor: getWorkoutColor(workoutDay.workout.id).background
                    }}
                >
                    <p
                        style={{
                            color: getWorkoutColor(workoutDay.workout.id).text
                        }}
                    >
                        {workoutDay.workout.name}
                    </p>
                </div>
            ) : (
                <div
                    className={
                        isSelected
                            ? `${styles.placeholder} ${styles.activePlaceholder}`
                            : styles.placeholder
                    }
                    onClick={() => onAddWorkout(weekDay)}
                >
                    <p>+ Add Workout</p>
                </div>
            )}
        </div>
    );
}

export default WorkoutDayCard;