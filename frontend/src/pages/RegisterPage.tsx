import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { AxiosError } from "axios";
import { register as registerRequest } from "../services/authService";
import AuthLayout from "../layouts/AuthLayout";
import AuthCard from "../components/auth/AuthCard";
import styles from "../components/auth/AuthForm.module.css";


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
        <AuthLayout>
            <AuthCard
                subtitle="Start building your perfect workout routine."
            >

                <form
                    onSubmit={handleSubmit}
                    className={styles.form}
                >
                    <div className={styles.field}>
                        <label>
                            Username
                        </label>
                        <input
                            className={styles.input}
                            type="text"
                            value={username}
                            onChange={(e) =>
                                setUsername(e.target.value)
                            }
                        />
                    </div>

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
                        Create Account
                    </button>

                </form>
                <p className={styles.footer}>
                    Already have an account?{" "}
                    <Link to="/login">
                        Login
                    </Link>
                </p>
            </AuthCard>
        </AuthLayout>
    );
}

export default RegisterPage;