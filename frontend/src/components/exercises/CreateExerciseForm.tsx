import { useState } from "react";
import axios from "axios";
import { createExercise } from "../../services/exerciseService";
import { EXERCISE_CATEGORIES } from "../../constants/exerciseCategories";

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
                {EXERCISE_CATEGORIES.map((category) => (
                    <option
                        key={category}
                        value={category}
                    >
                        {category}
                    </option>
                ))}
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