import { useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";


function DashboardPage() {

    const { user, logout } = useAuth();
    const navigate = useNavigate();

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
            <p>
                This is your dashboard.
            </p>
            <button onClick={handleLogout}>
                Logout
            </button>
        </div>
    );
}

export default DashboardPage;