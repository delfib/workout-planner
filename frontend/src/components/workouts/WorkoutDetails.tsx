import { useEffect, useState } from "react";
import { AxiosError } from "axios";
import styles from "./WorkoutDetails.module.css";
import editIcon from "../../assets/edit-pen.svg";
import type { WorkoutDay } from "../../types/workoutDay";
import type { Exercise } from "../../types/exercise";
import { getWorkoutColor } from "../../constants/workoutColors";
import { addExerciseToWorkout, deleteWorkout, deleteWorkoutExercise, getWorkout, updateWorkout } from "../../services/workoutService";
import { deleteWorkoutDay } from "../../services/workoutDayService";
import ExerciseCard from "./ExerciseCard";
import AddExerciseForm from "./AddExerciseForm";

interface Props {
    workoutDay: WorkoutDay;
    onWorkoutUpdated: () => void;
    onClose: () => void;
}

function WorkoutDetails({workoutDay, onWorkoutUpdated, onClose}: Props) {

    const [workout, setWorkout] = useState<any>(null);
    const [name, setName] = useState("");
    const [error, setError] = useState("");
    const [isEditingName, setIsEditingName] = useState(false);
    const [showAddExercise, setShowAddExercise] = useState(false);

    async function loadWorkout() {
        try {
            const data = await getWorkout(workoutDay.workout.id);
            setWorkout(data);
            setName(data.name);
        } catch (error) {
            console.error(error);
        }
    }


    async function handleSaveName() {
        if (!workout) return;

        setError("");

        try {
            const updatedWorkout = await updateWorkout(workout.id, name);

            setWorkout({
                ...workout,
                name: updatedWorkout.name
            });

            setIsEditingName(false);
            onWorkoutUpdated();
        } catch (error) {
            if (error instanceof AxiosError) {
                setError(error.response?.data?.error || "Something went wrong");
            } else {
                setError("Something went wrong");
            }
        }
    }


    async function handleDeleteExercise(id: number) {
        try {
            await deleteWorkoutExercise(id);
            await loadWorkout();
        } catch (error) {
            console.error(error);
            setError("Could not delete exercise");
        }
    }


    async function handleAddExercise(exercise: Exercise, description: string) {
        try {
            await addExerciseToWorkout(workout.id, exercise.id, description);
            await loadWorkout();
            setShowAddExercise(false);
        } catch (error) {
            console.error(error);
            setError("Could not add exercise");
        }
    }


    async function handleUnassignWorkout() {
        try {
            await deleteWorkoutDay(workoutDay.id);
            onWorkoutUpdated();
            onClose();
        } catch (error) {
            console.error(error);
        }
    }


    async function handleDeleteWorkout() {
        const confirmed = window.confirm("Are you sure you want to delete this workout?");

        if (!confirmed) return;
        try {
            await deleteWorkout(workout.id);
            onClose();
            onWorkoutUpdated();
        } catch (error) {
            console.error(error);
            setError("Could not delete workout");
        }
    }

    useEffect(() => {
        setShowAddExercise(false);
        setError("");
        loadWorkout();
    }, [workoutDay.workout.id]);


    if (!workout) {
        return null;
    }

    const workoutColor = getWorkoutColor(workout.id);

    return (
        <div className={styles.container} style={{backgroundColor: workoutColor.background}}>
            <div className={styles.workoutBanner} style={{backgroundColor: workoutColor.background}} >
                
                <button className={styles.closeButton} onClick={onClose} >
                    ✕
                </button>

                <div className={styles.workoutHeader}>
                    <div className={styles.titleRow}>
                        {isEditingName ? (
                            <>
                                <input
                                    className={styles.titleInput}
                                    value={name}
                                    onChange={(e) => setName(e.target.value)}
                                    style={{color: workoutColor.text}}
                                    autoFocus
                                />

                                <button className={styles.saveButton} onClick={handleSaveName} >
                                    Save
                                </button>
                            </>
                        ) : (
                            <>
                                <h2 style={{color: workoutColor.text}}>
                                    {workout.name}
                                </h2>

                                <button
                                    className={styles.iconButton}
                                    onClick={() => {
                                        setError("");
                                        setIsEditingName(true);
                                    }}
                                >
                                    <img
                                        src={editIcon}
                                        alt="Edit"
                                        className={styles.iconImage}
                                    />
                                </button>
                            </>
                        )}
                    </div>

                    {error && (
                        <p className={styles.error}>
                            {error}
                        </p>
                    )}

                </div>
            </div>

            <div className={styles.exerciseList}>
                {workout.exercises.map((exercise: any) => (
                    <ExerciseCard
                        key={exercise.id}
                        name={exercise.exercise.name}
                        description={exercise.description}
                        onDelete={() => handleDeleteExercise(exercise.id)}
                    />

                ))}
            </div>

            <button className={styles.addExerciseButton} onClick={() => setShowAddExercise(!showAddExercise)} >
                + Add Exercise
            </button>

            {showAddExercise && (
                <AddExerciseForm
                    onAdd={handleAddExercise}
                    currentExercises={
                        workout.exercises.map(
                            (exercise: any) => exercise.exercise.id
                        )
                    }
                />
            )}

            <div className={styles.bottomButtons}>
                <button className={styles.secondaryButton} onClick={handleUnassignWorkout} >
                    Unassign from {workoutDay.day_of_week}
                </button>

                <button className={styles.deleteButton} onClick={handleDeleteWorkout} >
                    Delete Workout
                </button>
            </div>
        </div>
    );
}

export default WorkoutDetails;