import { useRouter } from "next/router";
import { useEffect } from "react";
import React from 'react'
// import exploremarket from '../public/market.jpeg'
// export default function Home() {

//   const router = useRouter();

//   return (
//     //home
//     <>
//       home
//     </>

//   );
// }

const App = () => {
  const router = useRouter();
  useEffect(() => {
    router.push('/login')
  }, [])
  return (
    <div className='w-full bg-transparent'>
      <div className='w-full h-screen'>
        <div className='w-full text-white text-8xl  flex flex-col items-center justify-center absolute top-0 left-0 h-screen z-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-[#31363f] from-0% to-black to-60%'>
          <div className='tracking-tight font-thin uppercase'>Empower Your Wealth</div><div className='uppercase text-zinc-200 -tracking-[1.03px] mt-[-1rem] font-semibold'> Invest Save  Prosper</div>
        </div>
      </div>

      <div className='w-full text-white flex justify-center mt-0  h-auto bg-black '>

        <div className=' w-[75rem] h-[35rem] px-28  border-2 rounded-2xl border-[#31363f] flex justify-around items-center'>

          <img src="/images/logo.png" className='w-[20rem] ' alt="logo" />
          <div className='w-100% h-100%'>
            <h3 className='text-5xl text-center uppercase font-semibold'>investments allocation</h3>
            <p className='w-2/3 text-xl text-center ml-[80px] mt-10 text-zinc-300 font-light tracking-wide'>{'"'}Strategically diversify your investment portfolio across a spectrum of assets, maximizing returns and minimizing risks for long-term financial growth and stability.{'"'}</p>
            <button className='w-[10rem] h-auto text-xl text-center ml-[200px] duration-300 ease-in text-white hover:bg-zinc-50 hover:text-zinc-950  font-extralight tracking-wider capitalize mt-10 border-zinc-400 hover:border-zinc-50 rounded-xl border-solid border-2 py-2 '>visit now!</button>
          </div>

        </div>

      </div>

      <div className='w-full text-white flex justify-center py-10  h-auto bg-black '>

        <div className=' w-[85rem] h-[35rem] px-28  border-2 rounded-2xl border-[#16181d] flex justify-around items-center'>
          <div className='w-100% h-100%'>
            <h3 className='text-5xl text-center mr-[180px] uppercase font-semibold'>explore market</h3>
            <p className='w-2/3 text-xl text-right mt-10 text-zinc-300 font-light tracking-wide'>{'"'}Discover, analyze, and invest smartly with our intuitive market app. Explore trends, track stocks, and make informed decisions effortlessly.{'"'}</p>
            <button className='w-[10rem] h-auto text-xl text-center ml-[130px] duration-300 ease-in text-white hover:bg-zinc-50 hover:text-zinc-950  font-extralight tracking-wider capitalize mt-10 border-zinc-400 hover:border-zinc-50 rounded-xl border-solid border-2 py-2 '>visit now!</button>
          </div>
          {/* <img src={exploremarket} className='w-[30rem] rounded-lg '/> */}
        </div>

      </div>

    </div>
  )
}

export default App