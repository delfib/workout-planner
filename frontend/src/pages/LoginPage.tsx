import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { login as loginRequest } from "../services/authService";
import { useAuth } from "../contexts/AuthContext";
import { AxiosError } from "axios";

type ErrorResponse = {
    error: string;
};

function LoginPage() {

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const { login } = useAuth();
    const navigate = useNavigate();

    async function handleSubmit(event: React.FormEvent) {
        event.preventDefault();
        setError("");

        try {
            const data = await loginRequest({email, password});
            login(data.user, data.token);
            navigate("/");
        
        } catch (error) {
            const axiosError = error as AxiosError<ErrorResponse>;
        
            if (axiosError.response?.data?.error) {
                setError(axiosError.response.data.error);
            } else {
                setError("Something went wrong.");
            }
        }
    }

    return (
        <div>
            <h1>
                Workout Planner
            </h1>

            <form onSubmit={handleSubmit}>
                <div>
                    <label>
                        Email
                    </label>
                    <input
                        type="email"
                        value={email}
                        onChange={(e) =>
                            setEmail(e.target.value)
                        }
                    />
                </div>

                <div>
                    <label>
                        Password
                    </label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) =>
                            setPassword(e.target.value)
                        }
                    />
                </div>

                {error && (
                    <p>{error}</p>
                )}

                <button type="submit">
                    Login
                </button>

                <p>
                    Don't have an account?{" "}
                    <Link to="/register">
                        Create one
                    </Link>
                </p>
            </form>
        </div>
    );
}

export default LoginPage;