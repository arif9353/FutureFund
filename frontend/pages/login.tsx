"use client";
import { useEffect, useState } from 'react';
import { auth, googleProvider } from '../firebase/firebase_store';
import { signInWithPopup, signInWithEmailAndPassword, createUserWithEmailAndPassword, getRedirectResult, UserCredential, onAuthStateChanged } from 'firebase/auth';
import Link from 'next/link';
import toast, { Toaster } from 'react-hot-toast';
import { FirebaseApp, FirebaseError } from 'firebase/app';
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

export default function Login() {
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [emailLoginFlag, setEmailLoginFlag] = useState<boolean>(false);

  const router = useRouter();

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      if (user && !emailLoginFlag) {
        toast.success("You are logged in!");
        router.push("/dashboard");
      }
    });

    return () => unsubscribe();
  }, [emailLoginFlag]);

  const handleGoogleLogin = async () => {
    try {
      await signInWithPopup(auth, googleProvider);
      setEmailLoginFlag(true); // Set flag when email login is successful
      router.push("/dashboard");
    } catch (error) {
      console.error("Error during Google login", error);
      toast.error(getErrorMessage(error as FirebaseError));
    }
  };

  const handleEmailLogin = async () => {
    if (email === '' || password === '')
      return toast.error('Please fill all the fields!');

    try {
      await signInWithEmailAndPassword(auth, email, password);
      setEmailLoginFlag(true); // Set flag when email login is successful
      router.push("/dashboard");
    } catch (error) {
      console.error("Error during email login", error);
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
          <form className='pc:w-[400px] mob:w-[90%]' onSubmit={(e) => { e.preventDefault() }}>
            <div className="mb-4">
              <h2 className='mb-6 text-2xl font-bold'>Login</h2>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Email"
                className="shadow appearance-none bg-transparent font-light text-white border rounded w-full py-2 px-3 leading-tight focus:outline-none focus:shadow-outline"
              />
            </div>
            <div className="mb-3">
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Password"
                className="shadow appearance-none bg-transparent text-white border rounded w-full py-2 px-3 leading-tight focus:outline-none focus:shadow-outline"
              />
            </div>
            <div className="flex flex-row-reverse justify-between items-center mb-3">
              <Link href="/forgot-password" className="text-xs text-slate-300 hover:text-slate-200 ">Forgot Password ?</Link>
            </div>


            <div className="flex items-center justify-between">
              <button
                onClick={handleEmailLogin}
                className="bg-blue-500 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded focus:outline-none focus:shadow-outline w-full"
              >
                Login
              </button>
            </div>

            <div className='flex flex-row w-full justify-between items-center my-7'>
              <div className='w-[40%] h-[1px] bg-[#eeeeee]'></div>
              <div className='text-sm'>or</div>
              <div className='w-[40%] h-[1px] bg-[#eeeeee]'></div>
            </div>

            <button
              onClick={handleGoogleLogin}
              className="w-full bg-[#00000000] border border-white text-white font-base py-2 px-4 rounded mb-4 flex items-center justify-center focus:outline-none focus:shadow-outline gap-4"
            >
              <img src="/images/google.png" alt="" className='h-[20px] w-[20px]' />
              Login with Google
            </button>
            <div className="flex justify-between items-center mt-2 mb-5">
              <Link href="/register" className="text-xs underline underline-offset-[2.5px]">Don{"'"}t have an account? Register</Link>
            </div>
          </form>
        </div>
      </div>
    </>
  );
}
