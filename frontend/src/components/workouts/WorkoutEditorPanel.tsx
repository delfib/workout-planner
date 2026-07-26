import styles from "./WorkoutEditorPanel.module.css";
import type { WorkoutDay } from "../../types/workoutDay.ts";
import CreateWorkoutForm from "./CreateWorkoutForm";
import EditWorkoutForm from "./EditWorkoutForm";

interface Props {
    mode: "create" | "edit";
    day?: string | null;
    workoutDay?: WorkoutDay | null;
    onClose: () => void;
    onWorkoutCreated: () => void;
}

function WorkoutEditorPanel({mode, day, workoutDay, onClose, onWorkoutCreated, }: Props) {

    return (
        <section className={styles.panel}>
            <div className={styles.header}>
                <div>
                    <h2>
                        {mode === "create"
                            ? `Create Workout for ${day}`
                            : `Edit ${workoutDay?.workout.name}`
                        }
                    </h2>

                    <p>
                        {mode === "create"
                            ? "Create a new workout or assign an existing one."
                            : "Edit your workout and manage its exercises."
                        }
                    </p>
                </div>

                <button
                    className={styles.closeButton}
                    onClick={onClose}
                >
                    ✕
                </button>
            </div>

            {mode === "create" ? (
                <CreateWorkoutForm
                    day={day!}
                    onClose={onClose}
                    onWorkoutCreated={onWorkoutCreated}
                />
            ) : (
                <EditWorkoutForm
                    workoutDay={workoutDay!}
                    onWorkoutUpdated={onWorkoutCreated}
                />
            )}
        </section>
    );
}

export default WorkoutEditorPanel;