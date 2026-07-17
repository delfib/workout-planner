import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import WorkoutView from "../components/WorkoutView";
import ExerciseLibrary from "../components/ExerciseLibrary";

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
        <div>
            <h1>
                Workout Planner
            </h1>
            <h2>
                Welcome, {user?.username}!
            </h2>
            <hr />
                <div>
                    <button onClick={() => setActiveTab("workouts")} >
                        Workouts
                    </button>
                    <button onClick={() => setActiveTab("exercises")} >
                        Exercises
                    </button>
                </div>
            <hr />
                {activeTab === "workouts" ? (
                    <WorkoutView />
                ) : (
                    <ExerciseLibrary />
                )}

            <button onClick={handleLogout}>
                Logout
            </button>
        </div>
    );
}

export default DashboardPage;