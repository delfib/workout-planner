import { useEffect, useState } from "react";
import { getWorkoutDays } from "../services/workoutDayService";
import { WEEK_DAYS } from "../constants/weekDays";
import type { WorkoutDay } from "../types/workoutDay";

function WorkoutView() {
    const [workoutDays, setWorkoutDays] = useState<WorkoutDay[]>([]);

    useEffect(() => {
        async function loadWorkoutDays() {
            try {
                const data = await getWorkoutDays();
                setWorkoutDays(data);
            } catch (error) {
                console.error(error);
            }
        }
        loadWorkoutDays();
    }, []);

    return (
        <>
            {WEEK_DAYS.map((weekDay) => {
                const workoutDay = workoutDays.find(
                    (day) => day.day_of_week === weekDay
                );

                return (
                    <div key={weekDay}>
                        <h3>{weekDay}</h3>

                        {workoutDay && (
                            <p>{workoutDay.workout.name}</p>
                        )}
                    </div>
                );
            })}
        </>
    );
}

export default WorkoutView;