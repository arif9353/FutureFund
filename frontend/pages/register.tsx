"use client";
import { useState } from 'react';
import { auth, googleProvider } from '../firebase/firebase_store';
import { signInWithPopup, createUserWithEmailAndPassword } from 'firebase/auth';
import toast from 'react-hot-toast';
import { FirebaseError } from 'firebase/app';
import Link from 'next/link';
import { useRouter } from 'next/router';

const getErrorMessage = (error: { code: string }) => {
    switch (error.code) {
        case 'auth/email-already-in-use':
            return 'This email is already in use. Please use a different email.';
        case 'auth/invalid-email':
            return 'The email address is not valid.';
        case 'auth/weak-password':
            return 'The password is too weak. Please use a stronger password.';
        case 'auth/user-disabled':
            return 'This user has been disabled.';
        case 'auth/user-not-found':
            return 'No user found with this email.';
        case 'auth/wrong-password':
            return 'Incorrect password. Please try again.';
        default:
            return 'An error occurred. Please try again.';
    }
};

export default function Register() {
    const [email, setEmail] = useState<string>('');
    const [password, setPassword] = useState<string>('');
    const [confirmPassword, setConfirmPassword] = useState<string>('');

    const router = useRouter();

    const handleGoogleSignup = async () => {
        try {
            await signInWithPopup(auth, googleProvider);
            toast.success('Successfully signed up with Google!');
            // Redirect or show success message
        } catch (error) {
            console.error('Error during Google signup', error);
            toast.error(getErrorMessage(error as FirebaseError));
        }
    };

    const handleEmailSignup = async () => {
        if (password !== confirmPassword) {
            toast.error('Passwords do not match. Please try again.');
            return;
        }

        try {
            await createUserWithEmailAndPassword(auth, email, password);
            toast.success('Successfully signed up with email!');
            router.push("/login")
            // Redirect or show success message
        } catch (error) {
            console.error('Error during email signup', error);
            toast.error(getErrorMessage(error as FirebaseError));
        }
    };

    return (
        <>
            <div className='min-h-screen w-screen flex flex-row mob:flex-col bg-primary text-white'>
                <div className='pc:w-[40%] pc:h-screen mob:w-screen mob:h-[25vh] mob:min-h-[150px] bg-[url("https://images.unsplash.com/photo-1644843521804-74ec147cb7bf?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")] bg-cover bg-center flex justify-center items-center'>
                    <div className='w-[90%] pc:h-[220px] flex items-center justify-center pc:rounded-xl pc:backdrop-blur-xl backdrop-brightness-105'>
                        <img src="/images/logo.png" alt="" className='pc:w-[65%] mob:w-[80%]' />
                    </div>
                </div>

                <div className="pc:w-[60%] mob:w-full pc:h-screen mob:h-[70%] shadow-md px-5 pt-6 pb-8 mb-4 flex flex-col justify-center items-center mob:border-t mob:border-t-white">
                    <form className='pc:w-[400px]' onSubmit={(e) => { e.preventDefault() }}>
                        <div className="mb-4">
                            <h2 className='mb-6 text-2xl font-bold'>Register</h2>
                            <input
                                type="text"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                placeholder="Email"
                                className="shadow appearance-none bg-transparent font-light text-white border rounded w-full py-2 px-3 leading-tight focus:outline-none focus:shadow-outline"
                            />
                        </div>
                        <div className="mb-4">
                            <input
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                placeholder="Password"
                                className="shadow appearance-none bg-transparent text-white border rounded w-full py-2 px-3 leading-tight focus:outline-none focus:shadow-outline"
                            />
                        </div>
                        <div className="mb-6">
                            <input
                                type="password"
                                value={confirmPassword}
                                onChange={(e) => setConfirmPassword(e.target.value)}
                                placeholder="Confirm Password"
                                className="shadow appearance-none bg-transparent text-white border rounded w-full py-2 px-3 mb-3 leading-tight focus:outline-none focus:shadow-outline"
                            />
                        </div>
                        <div className="flex items-center justify-between">
                            <button
                                onClick={handleEmailSignup}
                                className="bg-[#6923cd] hover:bg-[#6a23cde1] text-white font-medium py-2 px-4 rounded focus:outline-none focus:shadow-outline w-full"
                            >
                                Register
                            </button>
                        </div>

                        <div className='flex flex-row w-full justify-between items-center my-7'>
                            <div className='w-[40%] h-[1px] bg-[#eeeeee]'></div>
                            <div className='text-sm'>or</div>
                            <div className='w-[40%] h-[1px] bg-[#eeeeee]'></div>
                        </div>

                        <button
                            onClick={handleGoogleSignup}
                            className="w-full  bg-[#00000000] border border-white text-white font-base py-2 px-4 rounded mb-4 flex items-center justify-center focus:outline-none focus:shadow-outline gap-4"
                        >
                            <img src="/images/google.png" alt="" className='h-[20px] w-[20px]' />
                            Login with Google
                        </button>
                        <div className="flex justify-between items-center mt-2 mb-5">
                            <Link href="/login" className="text-xs underline underline-offset-[2.5px]">Already have an account? Login</Link>
                        </div>
                    </form>
                </div>
            </div>
        </>
    );
}
