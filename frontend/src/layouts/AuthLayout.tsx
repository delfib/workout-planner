import styles from "./AuthLayout.module.css";
import heroImage from "../assets/gym.svg";

type AuthLayoutProps = {
    children: React.ReactNode;
};

function AuthLayout({ children }: AuthLayoutProps) {

    return (
        <div className={styles.container}>
            <div className={styles.formSection}>
                {children}
            </div>

            <div className={styles.heroSection}>
                <img
                    src={heroImage}
                    alt="Workout illustration"
                    className={styles.heroImage}
                />
            </div>
        </div>
    );
}

export default AuthLayout;