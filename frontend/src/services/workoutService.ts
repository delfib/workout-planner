import api from "./api";

export interface Workout {
    id: number;
    name: string;
}

export async function createWorkout(name: string): Promise<Workout> {
    const response = await api.post<Workout>("/workouts", {
        name,
    });
    return response.data;
}

export async function getWorkouts(): Promise<Workout[]> {
    const response = await api.get<Workout[]>("/workouts");
    return response.data;
}