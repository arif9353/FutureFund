import { useEffect } from 'react';
import { auth } from '../firebase/firebase_store';
import { useRouter } from 'next/router';

export default function Logout() {
    const router = useRouter();
    
    useEffect(() => {
        const logout = async () => {
            try {
                await auth.signOut();
                router.push('/login');
            } catch (error) {
                console.error('Error during logout', error);
            }
        };
        logout();
    }, []);

    return <></>;
}
