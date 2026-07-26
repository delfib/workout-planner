import styles from "./ExerciseCard.module.css";

interface Props {
    name: string;
    description: string;
}

function ExerciseCard({name, description, }: Props) {

    return (
        <div className={styles.card}>
            <div className={styles.header}>
                <h4>{name}</h4>

            </div>

            {description && (
                <p className={styles.description}>
                    {description}
                </p>
            )}
        </div>
    );
}

export default ExerciseCard;