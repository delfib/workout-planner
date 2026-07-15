import { Navigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";


function ProtectedRoute({ children }: { children: React.ReactNode }) {
    const { token } = useAuth();
    if (!token) {
        return <Navigate to="/login" />;
    }
    return children;
}

export default ProtectedRoute;