import Link from "next/link";
import { useRouter } from "next/router";
import { useEffect, useRef, useState } from "react";
import { IoIosArrowDown } from "react-icons/io";

export default function Top_Nav() {
    const router = useRouter();
    const location = router.pathname;
    const [isDropdownOpen, setIsDropdownOpen] = useState<boolean>(false);
    
    
    const dropdownRef = useRef<any>(null);

    useEffect(() => {
        function handleClickOutside(event : any) {
            if (dropdownRef.current && !dropdownRef?.current?.contains(event.target)) {
                setIsDropdownOpen(false);
            }
        }

        document.addEventListener("mousedown", handleClickOutside);
        return () => {
            document.removeEventListener("mousedown", handleClickOutside);
        };
    }, [dropdownRef]);

    return (
        <>
            <nav className="flex items-center justify-between px-4 h-[70px] bg-[#1d1f24] w-full">
                <img src="/images/logo.png" alt="" className="max-h-[65%] mob:hidden" />
                <img src="/images/logo_no_text.png" alt="" className="max-h-[65%] pc:hidden" />

                <div onClick={() => setIsDropdownOpen(!isDropdownOpen)} 
                className={"p-2  flex bg-[#00000000] hover:bg-[#22242a] rounded-md items-center gap-2 cursor-pointer relative " + (isDropdownOpen ? "bg-[#282a31]" : "")}>
                    <div className="h-[25px] rounded-full border-white aspect-square border object-cover object-center overflow-hidden">
                        <img src="./images/logo_no_text.png" alt="" />
                    </div>
                    <IoIosArrowDown color="white" />
                    {isDropdownOpen && (
                        <>
                            <div ref={dropdownRef} className="bg-[#22242a] absolute top-[50px] w-[160px] right-0 text-sm p-3 border border-opacity-40 border-slate-300 rounded-lg flex flex-col">
                                <Link href="/profile" className="p-1 px-3 hover:bg-[#2f3139] rounded-[4px]">Profile</Link>
                                <Link href="/logout" className="p-1 px-3 hover:bg-[#2f3139] rounded-[4px]">Logout</Link>
                            </div>
                        </>
                    )

                    }
                </div>

            </nav>
        </>
    )
}