import styles from "./AuthCard.module.css";

type AuthCardProps = {
    children: React.ReactNode;
    subtitle: string;
};

function AuthCard({
    children,
    subtitle
}: AuthCardProps) {
    return (
        <div className={styles.wrapper}>
            <h1 className={styles.logo}>
                WORKOUT PLANNER
            </h1>

            <p className={styles.subtitle}>
                {subtitle}
            </p>

            {children}
        </div>
    );
}

export default AuthCard;