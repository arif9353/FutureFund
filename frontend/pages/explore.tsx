"use client";
import Top_Nav from "@/_components/Top_Nav";
import axios from "axios";
import { useEffect, useState } from "react";
import { static_data } from "@/_components/static_stock_data";
import { FaArrowTrendUp } from "react-icons/fa6";
export default function Explore() {

    const [data, setData] = useState(static_data)
    console.log(data)
    useEffect(() => {
        // axios.get('http://localhost:8000/fetchdata/')
        //     .then(res => {
        //         console.log(res.data)
        //         setData(res.data)
        //     }).catch(err => {
        //         console.error(err)
        //     })
    }, [])

    return (
        <>
            <Top_Nav />
            <div className="text-white flex min-h-[calc(100vh-70px)] ">
                <div className="w-screen flex mob:flex-col pc:justify-center gap-2 p-4">
                    <div className="w-[30%] mob:w-full mob:h-[350px] pc:h-[calc(85vh)] border rounded-lg ">
                        <h1 className="text-center text-xl my-4"> Top 25 Stocks</h1>
                        <div className="overflow-x-hidden overflow-y-auto max-h-[90%] mob:max-h-[80%]">
                            {data && data?.stock_data?.map((stock, index) => {
                                console.log(stock)
                                return (
                                    <>
                                        <div key={index} className={"w-full h-[50px] font-medium text-white flex justify-between items-center px-4 py-8 relative"
                                            + (index % 2 === 0 ? " bg-[#3e3e3e27]" : " bg-[#00000000]")
                                        }>
                                            <p className="w-[60%] text-ellipsis ">{stock.name}</p>
                                            <p className="text-xs flex items-center gap-1 w-[20%] text-slate-400">
                                                <><FaArrowTrendUp /></>
                                                {(String(stock.profit_percent)).substring(0, 4)}%
                                            </p>
                                            <p className={`w-[30%] flex flex-row-reverse font-medium ${stock.recommendation.split(" ")[0].toLowerCase() === "buy" ? "text-green-300" : "text-slate-300"}`}>₹ {stock.price}</p>
                                        </div>
                                        {/* <hr /> */}
                                    </>
                                )
                            })}
                        </div>
                    </div>

                    <div className="w-[30%] h-[20px] bg-red-500">

                    </div>

                    <div className="w-[30%] h-[20px] bg-red-500">

                    </div>
                </div>
            </div>
        </>
    );
} 