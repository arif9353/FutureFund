import { useEffect, useRef, useState } from 'react';
import Top_Nav from "@/_components/Top_Nav";
import { IoIosArrowForward, IoIosMenu } from "react-icons/io";
import { AiOutlinePlus } from 'react-icons/ai';
import { static_investment_data } from '@/_components/static_investment_data';
import { useRecoilState } from 'recoil';
import { investmentFormDataRecoil } from '@/_recoil/cosmic';
import InvestmentForm from '@/_components/Invest_Form';

export default function Invest() {
    const [data, setData] = useState(static_investment_data)
    const [formData, setFormData] = useRecoilState<any>(investmentFormDataRecoil);

    const requiredFields = [
        'location',
        'years_to_retire',
        'salary',
        'investment_amount',
        'current_savings',
        'debt',
        'other_expenses',
        'number_of_dependents',
        'current_invested_amount',
        'bank'
    ];

    const isFormDataIncomplete = requiredFields.some(field => !formData || formData[field] === undefined || formData[field] === '');

    console.log(formData)

    const [sidebarOpen, setSidebarOpen] = useState(false);
    const sidebarRef = useRef<HTMLDivElement>(null);
    useEffect(() => {
        function handleClickOutside(event: any) {
            if (sidebarRef.current && !sidebarRef.current.contains(event.target)) {
                setSidebarOpen(false);
            }
        }

        document.addEventListener('mousedown', handleClickOutside);
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, [sidebarRef]);


    if (isFormDataIncomplete)
        return <>
            <Top_Nav />
            <div
                style={{ background: "linear-gradient(135deg, #0e141a90, #131b2490, #1a0e2490)" }}
                className="flex flex-col pc:flex-row pc:min-h-[calc(100vh-70px)] mob:min-h-[calc(100vh-70px)] text-white p-4 gap-4">
                <InvestmentForm />
            </div>
        </>


    if (!isFormDataIncomplete)
        return (
            <>
                <Top_Nav />
                <div
                    style={{ background: "linear-gradient(135deg, #0e141a90, #131b2490, #1a0e2490)" }}
                    className="flex flex-col pc:flex-row pc:h-[calc(100vh-70px)] mob:min-h-[calc(100vh-70px)] text-white p-4 gap-4">
                    <div ref={sidebarRef}
                        className={`fixed inset-0 z-40 w-64 bg-[#1d1f24]  rounded-lg p-4 transition-transform duration-500 ease-in-out transform ${sidebarOpen ? "translate-x-0" : "-translate-x-full"} pc:relative pc:translate-x-0`}>

                        <span className='block text-sm'>Details</span>
                        <hr className='my-3' />

                        {/* {PRINT ALL THE DATA WHICH WE COLLECTED THROUGH FORM HERE} */}
                        {requiredFields.map((field) => (
                            <div key={field} className="mb-4">
                                <span className="block text-[10px] text-slate-400 font-medium">{field.replace(/_/g, ' ').toUpperCase()}</span>
                                <span className="block text-base font-medium">{formData[field]}</span>
                            </div>
                        ))}

                    </div>
                    <button className="mob:block pc:hidden  left-1 z-10 text-white font-bold  rounded" onClick={() => setSidebarOpen(!sidebarOpen)}>
                        {<IoIosMenu size={"26px"} />}
                    </button>
                    <div className="flex-1 pc:p-4 mob:p-2 rounded-lg">
                        <div className=' overflow-y-scroll max-h-full'>
                            <LowRiskDetails data={data} />
                            <MediumRiskDetails data={data} />
                            <HighRiskDetails data={data} />
                        </div>
                    </div>
                </div>
            </>
        );
}


export const LowRiskDetails = ({ data }: any) => {
    return <>
        <div className='w-full flex flex-wrap justify-between mob:justify-center gap-2 mb-5'>
            <h1 className='w-full mb-4 text-green-300 font-semibold'>Low Risk</h1>

            <div className='h-[150px] w-[150px] bg-[#1d1f24] rounded-md text-sm flex flex-col p-4 items-start gap-3'>
                Stocks
                <h2>{data?.low_json?.stock_percent.toFixed(1)} %</h2>
                <h2>{data?.low_json?.stock_amount.toFixed(1)} ₹</h2>
            </div>

            <div className='h-[150px] w-[150px] bg-[#1d1f24] rounded-md text-sm flex flex-col p-4 items-start gap-3'>
                Crypto
                <h2>{data?.low_json?.crypto_percent.toFixed(1)} %</h2>
                <h2>{data?.low_json?.crypto_amount.toFixed(1)} ₹</h2>
            </div>


            <div className='h-[150px] w-[150px] bg-[#1d1f24] rounded-md text-sm flex flex-col p-4 items-start gap-3'>
                Properties
                <h2>{data?.low_json?.property_percent.toFixed(1)} %</h2>
                <h2>{data?.low_json?.property_amount.toFixed(1)} ₹</h2>
            </div>
            <div className='h-[150px] w-[150px] bg-[#1d1f24] rounded-md text-sm flex flex-col p-4 items-start gap-3'>
                GOLD ETF
                <h2>{data?.low_json?.gold_percent.toFixed(1)} %</h2>
                <h2>{data?.low_json?.gold_amount.toFixed(1)} ₹</h2>
            </div>
            <div className='h-[150px] w-[150px] bg-[#1d1f24] rounded-md text-sm flex flex-col p-4 items-start gap-3'>
                Bonds
                <h2>{data?.low_json?.bond_percent.toFixed(1)} %</h2>
                <h2>{data?.low_json?.bond_amount.toFixed(1)} ₹</h2>
            </div>

            <div className='h-[150px] w-[150px] bg-[#1d1f24] rounded-md text-sm flex flex-col p-4 items-start gap-3'>
                RD
                <h2>{data?.low_json?.recurrent_percent.toFixed(1)} %</h2>
                <h2>{data?.low_json?.recurrent_amount.toFixed(1)} ₹</h2>
            </div>

        </div>
    </>
}

export const MediumRiskDetails = ({ data }: any) => {
    return <>
        <div className='w-full flex flex-wrap justify-between gap-2 mb-5'>
            <h1 className='w-full mb-4 text-orange-300 font-semibold'>Medium Risk</h1>

            <div className='h-[150px] w-[150px] bg-[#1d1f24] rounded-md text-sm flex flex-col p-4 items-start gap-3'>
                Stocks
                <h2>{data?.medium_json?.stock_percent.toFixed(1)} %</h2>
                <h2>{data?.medium_json?.stock_amount.toFixed(1)} ₹</h2>
            </div>

            <div className='h-[150px] w-[150px] bg-[#1d1f24] rounded-md text-sm flex flex-col p-4 items-start gap-3'>
                Crypto
                <h2>{data?.medium_json?.crypto_percent.toFixed(1)} %</h2>
                <h2>{data?.medium_json?.crypto_amount.toFixed(1)} ₹</h2>
            </div>


            <div className='h-[150px] w-[150px] bg-[#1d1f24] rounded-md text-sm flex flex-col p-4 items-start gap-3'>
                Properties
                <h2>{data?.medium_json?.property_percent.toFixed(1)} %</h2>
                <h2>{data?.medium_json?.property_amount.toFixed(1)} ₹</h2>
            </div>
            <div className='h-[150px] w-[150px] bg-[#1d1f24] rounded-md text-sm flex flex-col p-4 items-start gap-3'>
                GOLD ETF
                <h2>{data?.medium_json?.gold_percent.toFixed(1)} %</h2>
                <h2>{data?.medium_json?.gold_amount.toFixed(1)} ₹</h2>
            </div>
            <div className='h-[150px] w-[150px] bg-[#1d1f24] rounded-md text-sm flex flex-col p-4 items-start gap-3'>
                Bonds
                <h2>{data?.medium_json?.bond_percent.toFixed(1)} %</h2>
                <h2>{data?.medium_json?.bond_amount.toFixed(1)} ₹</h2>
            </div>

            <div className='h-[150px] w-[150px] bg-[#1d1f24] rounded-md text-sm flex flex-col p-4 items-start gap-3'>
                RD
                <h2>{data?.medium_json?.recurrent_percent.toFixed(1)} %</h2>
                <h2>{data?.medium_json?.recurrent_amount.toFixed(1)} ₹</h2>
            </div>

        </div>
    </>
}
export const HighRiskDetails = ({ data }: any) => {
    return <>
        <div className='w-full flex flex-wrap justify-between gap-2 mb-5'>
            <h1 className='w-full mb-4 text-red-400 font-semibold'>High Risk</h1>

            <div className='h-[150px] w-[150px] bg-[#1d1f24] rounded-md text-sm flex flex-col p-4 items-start gap-3'>
                Stocks
                <h2>{data?.high_json?.stock_percent.toFixed(1)} %</h2>
                <h2>{data?.high_json?.stock_amount.toFixed(1)} ₹</h2>
            </div>

            <div className='h-[150px] w-[150px] bg-[#1d1f24] rounded-md text-sm flex flex-col p-4 items-start gap-3'>
                Crypto
                <h2>{data?.high_json?.crypto_percent.toFixed(1)} %</h2>
                <h2>{data?.high_json?.crypto_amount.toFixed(1)} ₹</h2>
            </div>


            <div className='h-[150px] w-[150px] bg-[#1d1f24] rounded-md text-sm flex flex-col p-4 items-start gap-3'>
                Properties
                <h2>{data?.high_json?.property_percent.toFixed(1)} %</h2>
                <h2>{data?.high_json?.property_amount.toFixed(1)} ₹</h2>
            </div>
            <div className='h-[150px] w-[150px] bg-[#1d1f24] rounded-md text-sm flex flex-col p-4 items-start gap-3'>
                Gold ETF
                <h2>{data?.high_json?.gold_percent.toFixed(1)} %</h2>
                <h2>{data?.high_json?.gold_amount.toFixed(1)} ₹</h2>
            </div>
            <div className='h-[150px] w-[150px] bg-[#1d1f24] rounded-md text-sm flex flex-col p-4 items-start gap-3'>
                Bonds
                <h2>{data?.high_json?.bond_percent.toFixed(1)} %</h2>
                <h2>{data?.high_json?.bond_amount.toFixed(1)} ₹</h2>
            </div>

            <div className='h-[150px] w-[150px] bg-[#1d1f24] rounded-md text-sm flex flex-col p-4 items-start gap-3'>
                RD
                <h2>{data?.high_json?.recurrent_percent.toFixed(1)} %</h2>
                <h2>{data?.high_json?.recurrent_amount.toFixed(1)} ₹</h2>
            </div>

        </div>
    </>
}