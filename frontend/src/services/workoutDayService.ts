import api from "./api";
import type { WorkoutDay } from "../types/workoutDay";

export async function getWorkoutDays(): Promise<WorkoutDay[]> {
    const response = await api.get<WorkoutDay[]>("/workout-days");
    return response.data;
}