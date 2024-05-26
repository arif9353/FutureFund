import Top_Nav from "@/_components/Top_Nav";
import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import { auth } from "./firebase_store";
import toast from "react-hot-toast";

export default function Dashboard() {
    const router = useRouter();

    const [redirected, setRedirected] = useState<boolean>(false);

    useEffect(() => {
        const unsubscribe = auth.onAuthStateChanged(async user => {
            if (!user && !redirected) {
                await auth.signOut();
                toast(' ⓘ  Please Login to access.');
                setRedirected(true);
                router.push('/login');
            }
        });

        return () => unsubscribe();
    }, [redirected]);

    return (
        <>
            <div className="flex flex-col min-h-screen w-screen text-white">
                <Top_Nav />
                
            </div>
        </>
    )
}