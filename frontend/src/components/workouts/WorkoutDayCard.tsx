import styles from "./WorkoutDayCard.module.css";
import type { WorkoutDay } from "../../types/workoutDay";
import { getWorkoutColor } from "../../constants/workoutColors";

interface Props {
    weekDay: string;
    workoutDay?: WorkoutDay;
    onAddWorkout: (weekDay: string) => void;
    onSelectWorkout: (workoutDay: WorkoutDay) => void;
    isSelected: boolean;
}

function WorkoutDayCard({weekDay, workoutDay, onAddWorkout, onSelectWorkout, isSelected}: Props) {

    const workoutColor = workoutDay ? getWorkoutColor(workoutDay.workout.id) : null;

    return (
        <div className={styles.dayCard}>

            <h3 className={styles.dayTitle}>
                {weekDay}
            </h3>

            {workoutDay ? (
                <div
                    className={
                        isSelected
                            ? `${styles.workoutCard} ${styles.selectedWorkout}`
                            : styles.workoutCard
                    }
                    style={{
                        backgroundColor: workoutColor?.background,
                        borderColor: isSelected
                            ? workoutColor?.text
                            : workoutColor?.background
                    }}
                    onClick={() => onSelectWorkout(workoutDay)}
                >
                    <p
                        style={{color: workoutColor?.text}}
                    >
                        {workoutDay.workout.name}
                    </p>
                </div>

            ) : (
                <div
                    className={`${styles.placeholder} ${isSelected ? styles.activePlaceholder : ""}`}
                    onClick={() => onAddWorkout(weekDay)}
                >
                    <p>
                        + Add Workout
                    </p>
                </div>

            )}
        </div>
    );
}

export default WorkoutDayCard;