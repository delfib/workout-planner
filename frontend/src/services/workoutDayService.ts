import api from "./api";
import type { WorkoutDay } from "../types/workoutDay";

export async function getWorkoutDays(): Promise<WorkoutDay[]> {
    const response = await api.get<WorkoutDay[]>("/workout-days");
    return response.data;
}

export async function createWorkoutDay(
    workout_id: number,
    day_of_week: string
) {
    const response = await api.post("/workout-days", {
        workout_id,
        day_of_week,
    });

    return response.data;
}