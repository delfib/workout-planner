import { useEffect, useState } from "react";
import styles from "./AddExerciseForm.module.css";
import type { Exercise } from "../../types/exercise";
import { getExercises } from "../../services/exerciseService";

interface Props {
    onAdd: (exercise: Exercise, description: string) => void;
    currentExercises: number[];
}

function AddExerciseForm({onAdd, currentExercises}: Props) {

    const [exercises, setExercises] = useState<Exercise[]>([]);
    const [selectedExercise, setSelectedExercise] = useState<Exercise | null>(null);
    const [description, setDescription] = useState("");
    const [error, setError] = useState("");

    useEffect(() => {
        async function loadExercises() {
            try {
                const data = await getExercises();
                setExercises(
                    data.filter(exercise => !currentExercises.includes(exercise.id))
                );
            } catch (error) {
                console.error(error);
            }
        }
        loadExercises();
    }, []);

    function handleAdd() {
        if (!selectedExercise || !description.trim()) {
            setError("Select an exercise and add a description");
            return;
        }
    
        setError("");
        onAdd(selectedExercise, description);

        setSelectedExercise(null);
        setDescription("");
    }

    return (
        <div className={styles.wrapper}>
            <div className={styles.container}>
                <select
                    value={selectedExercise?.id ?? ""}
                    onChange={(e) => {
                        const exercise = exercises.find(exercise => exercise.id === Number(e.target.value));
                        setSelectedExercise(exercise ?? null);
                    }}
                >
                    <option value="">
                        Select exercise
                    </option>
    
                    {exercises.map(exercise => (
                        <option key={exercise.id} value={exercise.id} >
                            {exercise.name}
                        </option>
                    ))}
    
                </select>
    
                <input
                    placeholder="Example: 4 sets x 10 reps"
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                />
    
                <button onClick={handleAdd}>
                    Add
                </button>
    
            </div>
    
            {error && (
                <p className={styles.error}>
                    {error}
                </p>
            )}
    
        </div>
    );
}

export default AddExerciseForm;