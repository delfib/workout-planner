import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { AxiosError } from "axios";
import { login as loginRequest } from "../services/authService";
import { useAuth } from "../contexts/AuthContext";
import AuthLayout from "../layouts/AuthLayout";
import AuthCard from "../components/auth/AuthCard";
import styles from "../components/auth/AuthForm.module.css";

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
        <AuthLayout>
            <AuthCard
                subtitle="Welcome back! The weights won't lift themselves..."
            >

                <form
                    onSubmit={handleSubmit}
                    className={styles.form}
                >
                    <div className={styles.field}>
                        <label>
                            Email
                        </label>
                        <input
                            className={styles.input}
                            type="email"
                            value={email}
                            onChange={(e) =>
                                setEmail(e.target.value)
                            }
                        />
                    </div>

                    <div className={styles.field}>
                        <label>
                            Password
                        </label>
                        <input
                            className={styles.input}
                            type="password"
                            value={password}
                            onChange={(e) =>
                                setPassword(e.target.value)
                            }
                        />
                    </div>

                    {error && (
                        <p className={styles.error}>
                            {error}
                        </p>
                    )}

                    <button
                        className={styles.button}
                        type="submit"
                    >
                        Login
                    </button>

                </form>
                <p className={styles.footer}>
                    Don't have an account?{" "}
                    <Link to="/register">
                        Create one
                    </Link>
                </p>
            </AuthCard>
        </AuthLayout>
    );
}

export default LoginPage;