import api from "./api";
import type { Exercise } from "../types/exercise";

export async function getExercises(search?: string, category?: string): Promise<Exercise[]> {

    const response = await api.get<Exercise[]>("/exercises", {
        params: {
            search,
            category
        }
    });

    return response.data;
}

export async function createExercise(name: string, category: string): Promise<Exercise> {

    const response = await api.post<Exercise>(
        "/exercises",
        {
            name,
            category
        }
    );

    return response.data;
}