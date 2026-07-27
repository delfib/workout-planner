import styles from "./WorkoutEditorPanel.module.css";
import type { WorkoutDay } from "../../types/workoutDay";
import CreateWorkoutForm from "./CreateWorkoutForm";
import WorkoutDetails from "./WorkoutDetails";

interface Props {
    mode: "create" | "edit";
    day?: string | null;
    workoutDay?: WorkoutDay | null;
    onClose: () => void;
    onWorkoutCreated: () => void;
}

function WorkoutEditorPanel({mode, day, workoutDay, onClose, onWorkoutCreated}: Props) {

    return (
        <section className={mode === "edit" ? styles.panelEdit : styles.panel} >
            {mode === "create" ? (
                <>
                    <div className={styles.header}>
                        <div>
                            <h2>
                                Create Workout for {day}
                            </h2>

                            <p>
                                Create a new workout or assign an existing one.
                            </p>
                        </div>

                        <button
                            className={styles.closeButton}
                            onClick={onClose}
                        >
                            ✕
                        </button>
                    </div>

                    <CreateWorkoutForm
                        day={day!}
                        onClose={onClose}
                        onWorkoutCreated={onWorkoutCreated}
                    />
                </>
            ) : (
                <WorkoutDetails
                    workoutDay={workoutDay!}
                    onWorkoutUpdated={onWorkoutCreated}
                    onClose={onClose}
                />
            )}
        </section>
    );
}

export default WorkoutEditorPanel;