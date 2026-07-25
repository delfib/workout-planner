import styles from "./WorkoutView.module.css";
import { useEffect, useState } from "react";
import { getWorkoutDays } from "../services/workoutDayService";
import { WEEK_DAYS } from "../constants/weekDays";
import type { WorkoutDay } from "../types/workoutDay";
import WorkoutDayCard from "./workouts/WorkoutDayCard";
import CreateWorkoutModal from "./workouts/CreateWorkoutModal";

function WorkoutView() {
    const [workoutDays, setWorkoutDays] = useState<WorkoutDay[]>([]);
    const [selectedDay, setSelectedDay] = useState<string | null>(null);
    const [showCreateModal, setShowCreateModal] = useState(false);

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
        setShowCreateModal(true);
    }

    useEffect(() => {
        loadWorkoutDays();
    }, []);

    return (
        <div className={styles.workoutView}>
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
                    />
                );
            })}
            {showCreateModal && selectedDay && (
                <CreateWorkoutModal
                    day={selectedDay}
                    onClose={() => setShowCreateModal(false)}
                />
            )}
        </div>
    );
}

export default WorkoutView;