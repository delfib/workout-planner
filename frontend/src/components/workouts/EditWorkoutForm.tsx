import { useEffect, useState } from "react";
import styles from "./WorkoutEditorPanel.module.css";
import type { WorkoutDay } from "../../types/workoutDay";
import { getWorkout, updateWorkout } from "../../services/workoutService";
import { AxiosError } from "axios";

interface Props {
    workoutDay: WorkoutDay;
    onWorkoutUpdated: () => void;
}

function EditWorkoutForm({workoutDay, onWorkoutUpdated}: Props) {

    const [workout, setWorkout] = useState<any>(null);
    const [name, setName] = useState("");
    const [error, setError] = useState("");

    async function loadWorkout() {
        try {
            setWorkout(null);
            const data = await getWorkout(
                workoutDay.workout.id
            );
            setWorkout(data);    
            setName(data.name);
        } catch (error) {
            console.error(error);
        }
    }

    async function handleSaveWorkout() {
        if (!workout) return;
    
        setError("");
    
        try {
            const updatedWorkout = await updateWorkout(workout.id, name,);
            setWorkout({...workout, name: updatedWorkout.name,});
            onWorkoutUpdated();
        } catch (error) {
            if (error instanceof AxiosError) {
                setError(error.response?.data?.error || "Something went wrong" );
            } else {
                setError("Something went wrong");
            }
        }
    }

    useEffect(() => {
        loadWorkout();
    }, [workoutDay.workout.id]);


    if (!workout) {
        return (
            <div className={styles.content}>
                <p>
                    Loading workout...
                </p>
            </div>
        );
    }

    return (
        <div className={styles.content}>
            <div className={styles.section}>

                <h3>Edit Workout</h3>
                <input
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                />
                {error && (
                    <p className={styles.error}>
                        {error}
                    </p>
                )}
                <button onClick={handleSaveWorkout}>
                    Save Changes
                </button>
            </div>

            <div className={styles.divider} />
            <div className={styles.section}>
                <h3>Exercises</h3>

                {workout.exercises.length === 0 ? (
                    <p>
                        No exercises added yet.
                    </p>
                ) : (
                    workout.exercises.map((exercise: any) => (
                        <p key={exercise.id}>
                            {exercise.exercise.name}
                        </p>
                    ))
                )}
            </div>
        </div>
    );
}

export default EditWorkoutForm;