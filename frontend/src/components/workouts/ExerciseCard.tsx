import styles from "./ExerciseCard.module.css";
import trashIcon from "../../assets/trash-can.svg";

interface Props {
    name: string;
    description: string;
    onDelete: () => void;
}

function ExerciseCard({name, description, onDelete}: Props) {

    return (
        <div className={styles.card}>

            <div className={styles.info}>
                <div className={styles.name}>
                    <h4>{name}</h4>
                </div>

                {description && (
                    <p className={styles.description}>
                        {description}
                    </p>
                )}
            </div>

            <button className={styles.deleteButton} onClick={onDelete} >
                <img src={trashIcon} alt="Delete exercise" />
            </button>
        </div>
    );
}

export default ExerciseCard;