"use client";
import { useState } from 'react';
import { auth } from '../firebase/firebase_store';
import { sendPasswordResetEmail, fetchSignInMethodsForEmail } from 'firebase/auth';
import toast from 'react-hot-toast';
import Link from 'next/link';
import { IoBackspace } from 'react-icons/io5';
import { IoMdArrowDropleft } from 'react-icons/io';

export default function ForgotPassword() {
    const [email, setEmail] = useState<string>('');
    const [emailSent, setEmailSent] = useState<boolean>(false);

    const handlePasswordReset = async () => {
        try {
            const signInMethods = await fetchSignInMethodsForEmail(auth, email);
            console.log(signInMethods)
            if (signInMethods.length === 0) {
                toast.error('No user found with this email.');
                return;
            }
            await sendPasswordResetEmail(auth, email);
            toast.success('Password reset email sent!');
            setEmailSent(true);
        } catch (error) {
            console.error('Error sending password reset email', error);
            toast.error('Failed to send password reset email. Please try again.');
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

                <div className="pc:w-[60%] mob:w-full pc:h-screen mob:h-[70%] shadow-md px-5 pb-8 flex flex-col justify-center items-center mob:border-t mob:border-t-white">
                    <form className='pc:w-[400px] mob:w-[90%]' onSubmit={(e) => { e.preventDefault() }}>
                        <div className="mb-4  mob:mt-8">
                            <h2 className='mb-6 text-2xl font-bold'>Forgot Password</h2>
                            {emailSent && <p className='my-6 mb-10 text-lg font-base text-slate-300'>
                                An email has been sent to reset your password. Please check your inbox and follow the instructions. <br /><br />
                                Thank you!
                            </p>}
                            {!emailSent && <input
                                type="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                placeholder="Enter your email"
                                className="shadow appearance-none bg-transparent font-light text-white border rounded w-full py-2 px-3 leading-tight focus:outline-none focus:shadow-outline"
                            />}
                        </div>
                        {!emailSent && <div className="flex items-center justify-between">
                            <button
                                onClick={handlePasswordReset}
                                className="bg-blue-500 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded focus:outline-none focus:shadow-outline w-full"
                            >
                                Submit
                            </button>
                        </div>}

                        <div className="flex justify-between items-center mt-4">
                            <Link href="/login" className="text-xs underline flex flex-row items-center gap-2">
                                {emailSent && <IoMdArrowDropleft size={"20px"}/>}  Back to Login</Link>
                        </div>
                    </form>
                </div>
            </div>
        </>
    );
}
