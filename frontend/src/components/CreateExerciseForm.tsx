import { useState } from "react";
import axios from "axios";
import { createExercise } from "../services/exerciseService";

interface Props {
    onCreated: () => void;
}

function CreateExerciseForm({ onCreated }: Props) {

    const [name, setName] = useState("");
    const [category, setCategory] = useState("");
    const [error, setError] = useState("");

    async function handleCreate() {
        try {
            setError("");

            await createExercise(name, category);

            onCreated();

            setName("");
            setCategory("");

        } catch (error) {
            if (axios.isAxiosError(error)) {
                setError(
                    error.response?.data?.error || "Something went wrong."
                );
            } else {
                setError("Something went wrong.");
            }
        }
    }

    return (
        <div>
            <h2>Create Exercise</h2>

            <input
                type="text"
                placeholder="Exercise name"
                value={name}
                onChange={(e) => setName(e.target.value)}
            />

            <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
            >
                <option value="">Select category</option>
                <option value="Chest">Chest</option>
                <option value="Back">Back</option>
                <option value="Legs">Legs</option>
                <option value="Shoulders">Shoulders</option>
                <option value="Arms">Arms</option>
                <option value="Core">Core</option>
                <option value="Glutes">Glutes</option>
                <option value="Cardio">Cardio</option>
            </select>

            {error && (
                <p>{error}</p>
            )}

            <button onClick={handleCreate}>
                Create
            </button>

        </div>
    );
}

export default CreateExerciseForm;