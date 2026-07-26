const WORKOUT_COLORS = [
    /* Pink */
    {
        background: "#fff3fc",
        text: "#f17bbe",
    },
    /* Blue */
    {
        background: "#edf4ff",
        text: "#658ff1",
    },
    /* Green */
    {
        background: "#eefcf2",
        text: "#5fbe7f",
    },
    /* Purple */
    {
        background: "#f9f3ff",
        text: "#b87bf1",
    },
    /* Orange */
    {
        background: "#fff6eb",
        text: "#f0844f",
    },
];

export function getWorkoutColor(id: number) {
    return WORKOUT_COLORS[id % WORKOUT_COLORS.length];
}