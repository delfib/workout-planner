import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { AxiosError } from "axios";

import { register as registerRequest } from "../services/authService";

type ErrorResponse = {
    error: string;
};

function RegisterPage() {

    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const [error, setError] = useState("");

    const navigate = useNavigate();

    async function handleSubmit(event: React.FormEvent) {
        event.preventDefault();

        setError("");

        try {
            await registerRequest({username, email, password});
            navigate("/login");

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
                        Username
                    </label>
                    <input
                        type="text"
                        value={username}
                        onChange={(e) =>
                            setUsername(e.target.value)
                        }
                    />
                </div>

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
                    Create Account
                </button>

                <p>
                    Already have an account?{" "}
                    <Link to="/login">
                        Login
                    </Link>
                </p>

            </form>
        </div>
    );
}

export default RegisterPage;