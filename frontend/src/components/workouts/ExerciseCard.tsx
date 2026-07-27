import styles from "./ExerciseCard.module.css";
import trashIcon from "../../assets/trash-can.svg";

interface Props {
    name: string;
    description: string;
}

function ExerciseCard({name, description}: Props) {

    return (
        <div className={styles.card}>

            <div className={styles.name}>
                <h4>
                    {name}
                </h4>
            </div>

            {description && (
                <p className={styles.description}>
                    {description}
                </p>
            )}

            <button className={styles.deleteButton}>
                <img src={trashIcon} alt="Delete exercise" />
            </button>
        </div>
    );
}

export default ExerciseCard;