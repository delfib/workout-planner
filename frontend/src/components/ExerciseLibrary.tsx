import styles from "./ExerciseLibrary.module.css";
import { useEffect, useState } from "react";
import { getExercises } from "../services/exerciseService";
import type { Exercise } from "../types/exercise";
import { EXERCISE_CATEGORIES } from "../constants/exerciseCategories";
import CreateExerciseForm from "./exercises/CreateExerciseForm";
import ExerciseCard from "./exercises/ExerciseCard";

function ExerciseLibrary() {
    const [exercises, setExercises] = useState<Exercise[]>([]);
    const [search, setSearch] = useState("");
    const [category, setCategory] = useState("");

    async function loadExercises() {
        try {
            const data = await getExercises(search, category);
            setExercises(data);
        } catch (error) {
            console.error(error);
        }
    }
    useEffect(() => {
        loadExercises();
    }, [search, category]);

    return (
        <div className={styles.exerciseLibrary}>
            {/* Header */}
            <h2>Exercise Library</h2>

            {/* Main Content */}
            <div className={styles.exerciseContent}>
                {/* Left Side */}
                <div className={styles.exerciseListSection}>
                    {/* Controls */}
                    <div className={styles.exerciseControls}>
                        <input
                            type="text"
                            placeholder="Search exercises..."
                            value={search}
                            onChange={(e) => setSearch(e.target.value)}
                        />

                        <select
                            value={category}
                            onChange={(e) => setCategory(e.target.value)}
                        >
                            <option value="">
                                All categories
                            </option>

                            {EXERCISE_CATEGORIES.map((category) => (
                                <option
                                    key={category}
                                    value={category}
                                >
                                    {category}
                                </option>
                            ))}
                        </select>

                    </div>

                    {/* Exercise Cards */}
                    <div className={styles.exerciseList}>

                        {exercises.map((exercise) => (
                            <ExerciseCard
                                key={exercise.id}
                                exercise={exercise}
                            />
                        ))}
                    </div>
                </div>

                {/* Right Side */}
                <div className={styles.exerciseSidebar}>
                    <CreateExerciseForm
                        onCreated={loadExercises}
                    />
                </div>
            </div>
        </div>
    );
}

export default ExerciseLibrary;