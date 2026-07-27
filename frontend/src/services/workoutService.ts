import api from "./api";

export interface Workout {
    id: number;
    name: string;
}

export async function createWorkout(name: string): Promise<Workout> {
    const response = await api.post<Workout>("/workouts", {name,});
    return response.data;
}

export async function getWorkouts(): Promise<Workout[]> {
    const response = await api.get<Workout[]>("/workouts");
    return response.data;
}

export async function getWorkout(id: number) {
    const response = await api.get(`/workouts/${id}`);
    return response.data;
}

export async function updateWorkout(id: number, name: string,): Promise<Workout> {
    const response = await api.put<Workout>(`/workouts/${id}`, { name });
    return response.data;
}

export async function deleteWorkoutExercise(id: number) {
    const response = await api.delete(`/workout-exercises/${id}`);
    return response.data;
}