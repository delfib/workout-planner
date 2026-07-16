import { useEffect, useState } from "react";
import { getExercises } from "../services/exerciseService";
import type { Exercise } from "../types/exercise";

function ExerciseView() {
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
        <div>
            <h2>Exercise Library</h2>

            <input
                type="text"
                placeholder="Search exercises..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
            />

            <select value={category} onChange={(e) => setCategory(e.target.value)} >
                    <option value="">All categories</option>
                    <option value="Chest">Chest</option>
                    <option value="Back">Back</option>
                    <option value="Legs">Legs</option>
                    <option value="Shoulders">Shoulders</option>
                    <option value="Arms">Arms</option>
                    <option value="Core">Core</option>
                    <option value="Glutes">Glutes</option>
                    <option value="Cardio">Cardio</option>
            </select>

            <button>
                + New Exercise
            </button>

            {exercises.map((exercise) => (
                <div key={exercise.id}>
                    <h3>{exercise.name}</h3>
                    <p>{exercise.category}</p>
                </div>
            ))}
        </div>
    );
}

export default ExerciseView;