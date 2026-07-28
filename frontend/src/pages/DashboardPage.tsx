import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import WorkoutView from "../components/workouts/WorkoutView";
import ExerciseLibrary from "../components/exercises/ExerciseLibrary";
import styles from "./DashboardPage.module.css";

type DashboardTab = "workouts" | "exercises";

function DashboardPage() {

    const { user, logout } = useAuth();
    const navigate = useNavigate();
    const [activeTab, setActiveTab] = useState<DashboardTab>("workouts");

    function handleLogout() {
        logout();
        navigate("/login");
    }

    return (
        <div className={styles.dashboard}>
            <header className={styles.header}>
                <div className={styles.titleSection}>
                    <h1>
                        Workout Planner
                    </h1>
                    <p>
                        Welcome back, {user?.username}!
                    </p>
                </div>
                <button
                    className={styles.logoutButton}
                    onClick={handleLogout}
                >
                    Log out

                </button>
            </header>

            <div className={styles.tabs}>
                <button
                    className={
                        activeTab === "workouts"
                        ? `${styles.tab} ${styles.activeTab}`
                        : styles.tab
                    }
                    onClick={() => setActiveTab("workouts")}

                >
                    Workouts
                </button>
                <button
                    className={
                        activeTab === "exercises"
                        ? `${styles.tab} ${styles.activeTab}`
                        : styles.tab
                    }
                    onClick={() => setActiveTab("exercises")}
                >
                    Exercises
                </button>
            </div>

            <main className={styles.content}>
                {activeTab === "workouts" ? (
                    <WorkoutView />
                ) : (
                    <ExerciseLibrary />
                )}
            </main>
        </div>
    );
}

export default DashboardPage;