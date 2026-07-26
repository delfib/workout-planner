import { useEffect, useState } from "react";
import styles from "./WorkoutEditorPanel.module.css";
import { createWorkout, getWorkouts, type Workout } from "../../services/workoutService.ts";
import { createWorkoutDay } from "../../services/workoutDayService.ts";
import { AxiosError } from "axios";

interface Props {
    day: string;
    onClose: () => void;
    onWorkoutCreated: () => void;
}

function WorkoutEditorPanel({
    day,
    onClose,
    onWorkoutCreated,
}: Props) {

    const [name, setName] = useState("");
    const [workouts, setWorkouts] = useState<Workout[]>([]);
    const [selectedWorkout, setSelectedWorkout] = useState<number | "">("");
    const [error, setError] = useState("");

    async function loadWorkouts() {
        try {
            const data = await getWorkouts();
            setWorkouts(data);
        } catch (error) {
            console.error(error);
        }
    }

    async function handleCreateWorkout() {
        setError("");
    
        try {
            if (!name.trim()) {
                setError("Workout name cannot be empty");
                return;
            }
            const workout = await createWorkout(name);
    
            await createWorkoutDay(
                workout.id,
                day
            );
            onWorkoutCreated();
            onClose();
    
        } catch (error) {
            if (error instanceof AxiosError) {
                setError(
                    error.response?.data?.error ||
                    "Something went wrong"
                );
            } else {
                setError("Something went wrong");
            }
        }
    }


    async function handleAssignWorkout() {
        if (!selectedWorkout) return;
    
        setError("");
    
        try {
            await createWorkoutDay(
                selectedWorkout,
                day
            );
            onWorkoutCreated();
            onClose();
    
        } catch (error) {
            if (error instanceof AxiosError) {
                setError(
                    error.response?.data?.error ||
                    "Something went wrong"
                );
            } else {
                setError("Something went wrong");
            }
        }
    }

    useEffect(() => {
        loadWorkouts();
    }, []);


    return (
        <section className={styles.panel}>
            <div className={styles.header}>
                <div>
                    <h2>Create Workout for {day}</h2>
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

            <div className={styles.content}>

                <div className={styles.section}>
                    <h3>Create New Workout</h3>

                    <input
                        placeholder="Workout name"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                    />
                    {error && (
                        <p className={styles.error}>
                            {error}
                        </p>
                    )}
                    <button onClick={handleCreateWorkout}>
                        Create
                    </button>
                </div>


                <div className={styles.divider} />

                <div className={styles.section}>
                    <h3>Assign Existing Workout</h3>

                    <select
                        value={selectedWorkout}
                        onChange={(e) =>
                            setSelectedWorkout(Number(e.target.value))
                        }
                    >
                        <option value="">
                            Select workout...
                        </option>

                        {workouts.map((workout) => (
                            <option
                                key={workout.id}
                                value={workout.id}
                            >
                                {workout.name}
                            </option>
                        ))}
                    </select>

                    <button onClick={handleAssignWorkout}>
                        Assign
                    </button>
                </div>
            </div>
        </section>
    );
}

export default WorkoutEditorPanel;