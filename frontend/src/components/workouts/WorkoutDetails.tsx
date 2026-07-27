import { useEffect, useState } from "react";
import styles from "./WorkoutDetails.module.css";
import type { WorkoutDay } from "../../types/workoutDay";
import { getWorkout, updateWorkout } from "../../services/workoutService";
import ExerciseCard from "./ExerciseCard";
import { AxiosError } from "axios";
import { getWorkoutColor } from "../../constants/workoutColors";
import editIcon from "../../assets/edit-pen.svg";

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

    async function loadWorkout() {
        try {
            setWorkout(null);
            const data = await getWorkout(workoutDay.workout.id);
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
            setIsEditingName(false);
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

    const workoutColor = getWorkoutColor(workout.id);

    return (
        <div className={styles.container} style={{backgroundColor: workoutColor.background, }} >
            <div
                className={styles.workoutBanner}
                style={{backgroundColor: workoutColor.background,}}
            >
                <button className={styles.closeButton} onClick={onClose} >
                    ✕
                </button>

                <div className={styles.workoutHeader}>
                    {isEditingName ? (
                        <input
                            className={styles.titleInput}
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            style={{color: workoutColor.text}}
                            autoFocus
                        />
                    ) : (
                        <h2 style={{color: workoutColor.text,}} >
                            {workout.name}
                        </h2>
                    )}
                    <button className={styles.iconButton} onClick={() => setIsEditingName(true)} >
                        <img src={editIcon} alt="Edit" className={styles.iconImage} />
                    </button>
                </div>
            </div>
    
            <div className={styles.exerciseList}>
                {workout.exercises.map((exercise: any) => (
                    <ExerciseCard
                        key={exercise.id}
                        name={exercise.exercise.name}
                        description={exercise.description}
                    />
                ))}
            </div>
    
            <button className={styles.addExerciseButton}>
                + Add Exercise
            </button>
    
            {error && (
                <p className={styles.error}>
                    {error}
                </p>
            )}
    
            <button className={styles.saveButton} onClick={handleSaveWorkout} >
                Save Changes
            </button>
    
            <div className={styles.bottomButtons}>
                <button className={styles.secondaryButton} >
                    Unassign from {workoutDay.day_of_week}
                </button>
    
                <button className={styles.deleteButton} >
                    Delete Workout
                </button>    
            </div>
        </div>
    );
}

export default WorkoutDetails;