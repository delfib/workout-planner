import { createContext, useContext, useState } from "react";


type User = {
    id: number;
    username: string;
    email: string;
};


type AuthContextType = {
    user: User | null;
    token: string | null;
    login: (user: User, token: string) => void;
    logout: () => void;
};


const AuthContext = createContext<AuthContextType | null>(null);


export function AuthProvider({ children }: { children: React.ReactNode }) {

    const [user, setUser] = useState<User | null>(() => {
        const storedUser = localStorage.getItem("user");

        return storedUser
            ? JSON.parse(storedUser)
            : null;
    });


    const [token, setToken] = useState<string | null>(() => {
        return localStorage.getItem("token");
    });


    function login(user: User, token: string) {

        setUser(user);
        setToken(token);

        localStorage.setItem("user", JSON.stringify(user));

        localStorage.setItem("token", token);
    }

    function logout() {

        setUser(null);
        setToken(null);

        localStorage.removeItem("user");
        localStorage.removeItem("token");
    }

    return (
        <AuthContext.Provider
            value={{user, token, login, logout}}
        >
            {children}
        </AuthContext.Provider>
    );
}


export function useAuth() {

    const context = useContext(AuthContext);
    if (!context) {
        throw new Error(
            "useAuth must be used inside AuthProvider"
        );
    }
    return context;
}