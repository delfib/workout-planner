import styles from "./WorkoutView.module.css";
import { useEffect, useState } from "react";
import { getWorkoutDays } from "../../services/workoutDayService";
import { WEEK_DAYS } from "../../constants/weekDays";
import type { WorkoutDay } from "../../types/workoutDay";
import WorkoutDayCard from "./WorkoutDayCard";
import WorkoutEditorPanel from "./WorkoutEditorPanel";

function WorkoutView() {
    const [workoutDays, setWorkoutDays] = useState<WorkoutDay[]>([]);
    const [selectedDay, setSelectedDay] = useState<string | null>(null);

    async function loadWorkoutDays() {
        try {
            const data = await getWorkoutDays();
            setWorkoutDays(data);
        } catch (error) {
            console.error(error);
        }
    }

    function handleAddWorkout(day: string) {
        setSelectedDay(day);
    }

    useEffect(() => {
        loadWorkoutDays();
    }, []);

    return (
        <div className={styles.workoutView}>
            <div className={styles.calendar}>
                {WEEK_DAYS.map((weekDay) => {
                    const workoutDay = workoutDays.find(
                        (day) => day.day_of_week === weekDay
                    );

                    return (
                        <WorkoutDayCard
                            key={weekDay}
                            weekDay={weekDay}
                            workoutDay={workoutDay}
                            onAddWorkout={handleAddWorkout}
                            isSelected={selectedDay === weekDay}
                        />
                    );
                })}
            </div>

            {selectedDay && (
                <WorkoutEditorPanel
                    day={selectedDay}
                    onClose={() => setSelectedDay(null)}
                    onWorkoutCreated={loadWorkoutDays}
                />
            )}
        </div>
    );
}

export default WorkoutView;