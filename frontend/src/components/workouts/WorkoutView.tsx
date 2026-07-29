import styles from "./WorkoutView.module.css";
import { useEffect, useRef, useState } from "react";
import { getWorkoutDays } from "../../services/workoutDayService";
import { WEEK_DAYS } from "../../constants/weekDays";
import type { WorkoutDay } from "../../types/workoutDay";
import WorkoutDayCard from "./WorkoutDayCard";
import WorkoutEditorPanel from "./WorkoutEditorPanel";

function WorkoutView() {
    const [workoutDays, setWorkoutDays] = useState<WorkoutDay[]>([]);
    const [selectedDay, setSelectedDay] = useState<string | null>(null);
    const [selectedWorkoutDay, setSelectedWorkoutDay] = useState<WorkoutDay | null>(null);
    const [panelMode, setPanelMode] = useState<"create" | "edit" | null>(null);
    const panelRef = useRef<HTMLDivElement | null>(null);

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
        setSelectedWorkoutDay(null);
        setPanelMode("create");
    }

    function handleSelectWorkout(workoutDay: WorkoutDay) {
        setSelectedWorkoutDay(workoutDay);
        setSelectedDay(null);
        setPanelMode("edit");
    }

    useEffect(() => {
        loadWorkoutDays();
    }, []);

    useEffect(() => {
        if (!panelMode) return;
    
        if (window.innerWidth <= 1250) {
            const timer = setTimeout(() => {
                panelRef.current?.scrollIntoView({
                    behavior: "smooth",
                    block: "start"
                });
            }, 400);
    
            return () => clearTimeout(timer);
        }
    }, [panelMode, selectedWorkoutDay, selectedDay]);

    return (
        <div className={styles.workoutView}>
    
            {panelMode && (
                <div ref={panelRef} className={styles.panel}>
                    <WorkoutEditorPanel
                        day={selectedDay}
                        workoutDay={selectedWorkoutDay}
                        mode={panelMode}
                        onClose={() => {
                            setSelectedDay(null);
                            setSelectedWorkoutDay(null);
                            setPanelMode(null);
                        }}
                        onWorkoutCreated={loadWorkoutDays}
                    />
                </div>
            )}
    
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
                            onSelectWorkout={handleSelectWorkout}
                            isSelected={
                                selectedDay === weekDay ||
                                (workoutDay !== undefined &&
                                    selectedWorkoutDay?.id === workoutDay.id)
                            }
                        />
                    );
                })}
            </div>
    
        </div>
    );
}

export default WorkoutView;