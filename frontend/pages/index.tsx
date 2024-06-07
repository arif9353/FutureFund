import { useRouter } from "next/router";
import { useEffect } from "react";
import React from 'react'
import { getAuth, onAuthStateChanged } from "firebase/auth"; // Adjust the import based on your Firebase setup


const App = () => {
  const router = useRouter();
  const auth = getAuth();
  const click_fn = () => {
    const user = auth?.currentUser;
    if (user) {
      router.push('/dashboard');
    } else {
      router.push('/login');
    }
  };
  return (
    <div className='w-full bg-transparent'>
      <div className='w-full h-screen'>
        <div className='w-full text-white pc:text-8xl mob:text-3xl  flex flex-col items-center justify-center absolute top-0 left-0 h-screen z-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-[#31363f] from-0% to-black to-60%'>
          <div className='tracking-tight font-thin uppercase'>Empower Your Wealth</div><div className='uppercase text-zinc-200 -tracking-[1.03px] pc:mt-[-1rem] font-semibold'> Invest Save  Prosper</div>
          <div className="flex justify-center my-4">
            <button
              onClick={() => { click_fn()}}
              className="text-2xl border rounded-full px-8 py-2 font-medium hover:bg-white hover:text-black hover:shadow-[#ffffff50] hover:shadow-2xl">Get Started</button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App