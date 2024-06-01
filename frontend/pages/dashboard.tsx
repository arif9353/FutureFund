import Top_Nav from "@/_components/Top_Nav";
import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import { auth } from "../firebase/firebase_store";
import toast from "react-hot-toast";
import Side_Nav_Dashboard from "@/_components/Side_Nav_Dashboard";
import { HiOutlineChartBar, HiOutlineCurrencyDollar, HiOutlineSparkles, HiOutlineUser } from "react-icons/hi2";
import { HiOutlineChat } from "react-icons/hi";

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
            <div className="flex flex-col min-h-screen w-screen text-white"
                style={{ background: "linear-gradient(135deg, #0e141a, #131b24, #1a0e24)" }}
            >
                <Top_Nav />
                <div className="flex flex-row w-screen pc:p-16 pc:px-16 mob:py-5">
                    <div className="pc:w-[100%] p-3 rounded-md">
                        <div className="flex flex-row flex-wrap gap-6 justify-center">

                            <button
                                onClick={() => router.push("/investments")}
                                className="bg-[#2a2c34] text-left text-sm py-4 px-5 rounded-md hover:bg-secondary h-[200px] pc:w-[350px] mob:w-[90%] flex flex-col justify-between">
                                <div>
                                    <span className="text-lg font-semibold">Investments Allocation</span>
                                    <span className="block text-xs mt-1">Manage and allocate your investments.</span>
                                </div>
                                <span className="self-end">
                                    <HiOutlineSparkles size={"20px"} />
                                </span>
                            </button>

                            <button
                                onClick={() => router.push("/chat")}
                                className="bg-[#2a2c34] text-left text-sm py-4 px-5 rounded-md hover:bg-secondary h-[200px] pc:w-[350px] mob:w-[90%] flex flex-col justify-between">
                                <div>
                                    <span className="text-lg font-semibold">Chat with AI</span>
                                    <span className="block text-xs mt-1">Get assistance from our AI.</span>
                                </div>
                                <span className="self-end">
                                    <HiOutlineChat size={"20px"} />
                                </span>
                            </button>

                            {/* <button className="bg-[#2a2c34] text-left text-sm py-4 px-5 rounded-md hover:bg-secondary h-[200px] pc:w-[350px] mob:w-[90%] flex flex-col justify-between">
                                <div>
                                    <span className="text-lg font-semibold">Performance Reports</span>
                                    <span className="block text-xs mt-1">View your investment performance.</span>
                                </div>
                                <span className="self-end">
                                    <HiOutlineChartBar size={"20px"} />
                                </span>
                            </button> */}

                            <button
                                onClick={() => router.push("/explore")}
                                className="bg-[#2a2c34] text-left text-sm py-4 px-5 rounded-md hover:bg-secondary h-[200px] pc:w-[350px] mob:w-[90%] flex flex-col justify-between">
                                <div>
                                    <span className="text-lg font-semibold">Explore Market</span>
                                    <span className="block text-xs mt-1">Check out Real-time stock values.</span>
                                </div>
                                <span className="self-end">
                                    <HiOutlineCurrencyDollar size={"20px"} />
                                </span>
                            </button>

                            <button 
                            onClick={() => router.push("/profile")}
                            className="bg-[#2a2c34] text-left text-sm py-4 px-5 rounded-md hover:bg-secondary h-[200px] pc:w-[350px] mob:w-[90%] flex flex-col justify-between">
                                <div>
                                    <span className="text-lg font-semibold">Profile Management</span>
                                    <span className="block text-xs mt-1">Manage user account and settings.</span>
                                </div>
                                <span className="self-end">
                                    <HiOutlineUser size={"20px"} />
                                </span>
                            </button>

                        </div>
                    </div>
                </div>
            </div>
        </>
    );
}
