export interface WorkoutDay {
    id: number;
    day_of_week: string;
    workout: {
        id: number;
        name: string;
    };
}