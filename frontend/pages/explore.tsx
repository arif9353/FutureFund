"use client";
import Top_Nav from "@/_components/Top_Nav";
import axios from "axios";
import { useEffect, useState } from "react";
import { stock_data_static } from "@/_components/static_stock_data";
import { FaArrowTrendUp } from "react-icons/fa6";
import { SlSizeFullscreen } from "react-icons/sl";
import { API_URL } from "@/_components/utils";
export default function Explore() {

    const [data, setData] = useState(stock_data_static)
    useEffect(() => {
        // axios.get(`${API_URL}/fetchdata/`)
        //     .then(res => {
        //         console.log(res.data)
        //         setData(res.data)
        //     }).catch(err => {
        //         console.error(err)
        //     })

        "use client";
        let x : any = JSON.parse(localStorage.getItem("stock_data") as any);
        setData(x)
    }, [])

    return (
        <>
            <Top_Nav />
            <div className="text-white flex min-h-[calc(100vh-70px)] ">
                <div className="w-[calc(100vw)] flex mob:flex-col pc:justify-center gap-4 p-4 ">
                    <div className="w-[30%] mob:w-full mob:h-[350px] pc:h-[calc(85vh)] border rounded-lg ">
                        <h1 className="text-center text-xl py-4 border-b border-b-[#ffffff55]"> Top Stocks</h1>
                        <div className="overflow-x-hidden overflow-y-auto max-h-[90%] mob:max-h-[80%]">
                            <div className={"w-full h-[50px] font-medium text-white flex justify-between items-center px-4 py-8 relative"
                                + " bg-[#3e3e3e25] border-b border-b-[#ffffff30]"}>
                                <p className="w-[60%] text-ellipsis ">Stock</p>
                                <p className={`w-[30%] flex flex-row-reverse font-medium`}>Price (₹) </p>
                            </div>
                            {data && data?.stock_data?.map((stock, index) => {
                                return (
                                    <>
                                        <div key={index} className={"w-full h-[50px] font-medium text-white flex justify-between items-center px-4 py-8 relative"
                                            + (index % 2 !== 0 ? " bg-[#3e3e3e15]" : " bg-[#00000000]")
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

                    <div className="w-[30%] mob:w-full mob:h-[350px] pc:h-[calc(85vh)] border rounded-lg ">
                        <h1 className="text-center text-xl py-4 border-b border-b-[#ffffff55]"> Top Crypto Currencies</h1>
                        <div className="overflow-x-hidden overflow-y-auto max-h-[90%] mob:max-h-[80%]">
                            <div className={"w-full h-[50px] font-medium text-white flex justify-between items-center px-4 py-8 relative"
                                + " bg-[#3e3e3e25] border-b border-b-[#ffffff30]"}>
                                <p className="w-[60%] text-ellipsis ">Crypto Name</p>
                                <p className={`w-[30%] flex flex-row-reverse font-medium`}>Price (₹) </p>
                            </div>
                            {data && data?.crypto_data?.map((crypto, index) => {
                                // console.log(stock)
                                return (
                                    <>
                                        <div key={index} className={"w-full h-[50px] font-medium text-white flex justify-between items-center px-4 py-8 relative"
                                            + (index % 2 !== 0 ? " bg-[#3e3e3e15]" : " bg-[#00000000]")
                                        }>
                                            <p className="w-[50%] text-ellipsis flex items-center gap-2">
                                                <img src={crypto.logourl} className="h-[20px] w-[20px] brightness-[500] grayscale" alt="" />
                                                <span>{crypto.name}</span>
                                            </p>
                                            {/* <p className="text-xs flex items-center gap-1 w-[20%] text-slate-400">
                                                <><FaArrowTrendUp /></>
                                                {(String(stock.profit_percent)).substring(0, 4)}%
                                            </p> */}
                                            <p className={`w-[50%] flex flex-row-reverse font-medium text-blue-300`}>₹ {crypto.last_price}</p>
                                        </div>
                                        {/* <hr /> */}
                                    </>
                                )
                            })}
                        </div>
                    </div>

                    <div className="w-[30%] mob:w-full mob:h-[350px] pc:h-[calc(85vh)] ">

                        <div className="w-[100%] p-6 border rounded-lg flex justify-between mb-5">
                            <h1 className="text-lg">Gold ETF Price</h1>
                            <div className="text-xl font-semibold text-orange-200"> ₹ {data && data.gold_data?.toFixed(2)}</div>
                        </div>

                        <div className="w-[100%] mob:w-full h-[calc(34.4vh)] border rounded-lg mb-5">
                            <h1 className="text-center text-xl py-2 border-b border-b-[#ffffff55]"> Bonds </h1>
                            <div className="overflow-x-hidden overflow-y-auto max-h-[80%]">
                                {data && data?.bond_data?.map((bond, index) => {
                                    return (
                                        <>
                                            <div key={index} className={"w-full font-medium text-white flex justify-between items-center px-4 py-4 relative"
                                                + (index % 2 !== 0 ? " bg-[#3e3e3e15]" : " bg-[#00000000]")
                                            }>
                                                <p className="w-[50%] text-ellipsis flex items-center gap-2">
                                                    <img src={bond.logo} className="h-[20px] w-[20px] rounded-full aspect-square object-cover bg-white" alt="" />
                                                    <span className="text-xs">{bond.name}</span>
                                                </p>
                                                <p className="text-xs flex items-center gap-1 w-[10%] text-slate-400">
                                                    <><FaArrowTrendUp /></>
                                                    {(String(bond.yield)).substring(0, 3)}%
                                                </p>
                                                <p className={`w-[40%] text-sm flex flex-row-reverse font-medium text-teal-400`}>₹ {bond.price}</p>
                                            </div>
                                            {/* <hr /> */}
                                        </>
                                    )
                                })}
                            </div>
                        </div>
                        <div className="w-[100%] mob:w-full h-[calc(34.4vh)] border rounded-lg mb-5">
                            <h1 className="text-center text-xl py-2 border-b border-b-[#ffffff55]"> Properties </h1>
                            <div className="overflow-x-hidden overflow-y-auto max-h-[80%]">
                                {data && data?.property_data?.map((prop, index) => {
                                    return (
                                        <>
                                            <div key={index} className={"w-full font-medium text-white flex justify-between items-center px-4 py-4 relative"
                                                + (index % 2 !== 0 ? " bg-[#3e3e3e15]" : " bg-[#00000000]")
                                            }>
                                                <p className="w-[50%] text-ellipsis flex items-center gap-2">
                                                    <span className="text-[11px]">{prop.title}</span>
                                                </p>
                                                <p className="text-xs flex items-center gap-1 w-[10%] text-slate-400">
                                                    {/* <><SlSizeFullscreen /></> */}
                                                    {(String(prop.area))} <br />sq.ft
                                                </p>
                                                <p className={`w-[20%] text-xs flex flex-row-reverse font-medium text-cyan-300`}>₹ {prop.price}</p>
                                            </div>
                                            {/* <hr /> */}
                                        </>
                                    )
                                })}
                            </div>
                        </div>


                    </div>


                </div>
            </div>
        </>
    );
} 