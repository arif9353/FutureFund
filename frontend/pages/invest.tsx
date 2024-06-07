import { useEffect, useRef, useState } from 'react';
import Top_Nav from "@/_components/Top_Nav";
import { IoIosArrowForward, IoIosMenu } from "react-icons/io";
import { AiOutlinePlus } from 'react-icons/ai';
import { static_investment_data } from '@/_components/static_investment_data';
import { useRecoilState } from 'recoil';
import { PopupDataRecoil, allocationDataRecoil, investmentFormDataRecoil } from '@/_recoil/cosmic';
import InvestmentForm from '@/_components/Invest_Form';
import DetailsPopup from '@/_components/DetailsPopup';

export default function Invest() {
    const [data, setData] = useRecoilState(allocationDataRecoil);
    const [formData, setFormData] = useRecoilState<any>(investmentFormDataRecoil);
    const [popupData, setPopupData] = useRecoilState<any>(PopupDataRecoil);


    const requiredFields = [
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

    console.log(formData, "formData :: ", isFormDataIncomplete);

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
        return (
            <>
                <Top_Nav />
                <div
                    style={{ background: "linear-gradient(135deg, #0e141a90, #131b2490, #1a0e2490)" }}
                    className="flex flex-col pc:flex-row pc:min-h-[calc(100vh-70px)] mob:min-h-[calc(100vh-70px)] text-white p-4 gap-4">
                    <InvestmentForm />
                </div>
            </>
        );

    return (
        <>
            <Top_Nav />
            <div
                style={{ background: "linear-gradient(135deg, #0e141a90, #131b2490, #1a0e2490)" }}
                className="flex flex-col pc:flex-row pc:min-h-[calc(100vh-70px)] mob:min-h-[calc(100vh-70px)] text-white p-4 gap-4">
                <div ref={sidebarRef}

                    className={`fixed inset-0 z-40 w-64 bg-[#1d1f24]  rounded-lg p-4 pb-1 transition-transform duration-500 ease-in-out transform ${sidebarOpen ? "translate-x-0" : "-translate-x-full"} pc:relative pc:translate-x-0`}>

                    <span className='block text-sm'>Details</span>
                    <hr className='my-3' />
                    {requiredFields.map((field) => (
                        <div key={field} className="mb-4">
                            <span className="block text-[10px] text-slate-400 font-medium capitalize">{field?.replace(/_/g, ' ').toUpperCase()}</span>
                            <span className="block text-base font-medium capitalize">{formData[field]?.replace(/_/g, ' ')}</span>
                        </div>
                    ))}
                    <button
                        onClick={() => { setFormData({}) }}
                        className='mb-4 text-sm text-center w-full bg-[#ffffff10] rounded-md mt-4 py-2'>Reset Details</button>
                </div>
                <button className="mob:block pc:hidden left-1 z-10 text-white font-bold rounded" onClick={() => setSidebarOpen(!sidebarOpen)}>
                    {<IoIosMenu size={"26px"} />}
                </button>
                <div className="flex-1 pc:p-4 mob:p-2 rounded-lg">
                    <div className='overflow-y-scroll max-h-full'>
                        <RiskDetails title="Low Risk" color="text-green-300" data={data.low_json} />
                        <RiskDetails title="Medium Risk" color="text-orange-300" data={data.medium_json} />
                        <RiskDetails title="High Risk" color="text-red-400" data={data.high_json} />
                    </div>
                </div>
            </div>

            {
                popupData?.type &&
                (
                    <DetailsPopup />
                )
            }
        </>
    );
}

const RiskDetails = ({ title, color, data }: { title: string, color: string, data: any }) => {
    const fields = [
        { name: 'Stocks', percent: 'stock_percent', amount: 'stock_amount' },
        { name: 'Crypto', percent: 'crypto_percent', amount: 'crypto_amount' },
        { name: 'Properties', percent: 'property_percent', amount: 'property_amount' },
        { name: 'Gold ETF', percent: 'gold_percent', amount: 'gold_amount' },
        { name: 'Bonds', percent: 'bond_percent', amount: 'bond_amount' },
        { name: 'RD', percent: 'recurrent_percent', amount: 'recurrent_amount' },
    ];

    const [popupData, setPopupData] = useRecoilState<any>(PopupDataRecoil);

    const handleOnClickofDiv = (name: string, title: string) => {
        if (name === "Stocks" && data?.stock) {
            setPopupData({ type: "Stocks", data: data?.stock })
        } else if (name === "Crypto") {
            setPopupData({ type: "Crypto", data: data?.crypto })
        } else if (name === "Properties" && data?.property) {
            console.log(data?.property)
            setPopupData({ type: "Properties", data: data?.property })
        } else if (name === "Bonds") {
            setPopupData({ type: "Bonds", data: data?.bond })
            console.log(data?.bond)
        } else if (name === "RD") {
            console.log(data?.recurrent)
            setPopupData({ type: "RD", data: data?.recurrent })
        }
    }

    return (
        <div className='w-full flex flex-wrap justify-between mob:justify-center gap-2 mb-5'>
            <h1 className={`w-full mb-4 ${color} font-semibold`}>{title}
                <span className='ml-4 font-normal text-white mob:block mob:ml-0 mob:mt-2'>
                    <span className='text-white opacity-40 font-extrabold'>
                        |
                    </span>
                    &nbsp;&nbsp; Goal Savings : {data?.goal_savings}</span>
            </h1>
            {fields.map(({ name, percent, amount }) => (
                <div onClick={() => {
                    handleOnClickofDiv(name, title)
                }}
                    key={name} className='h-[150px] w-[150px] bg-[#1d1f24] rounded-md text-sm flex flex-col p-4 items-start gap-3'>
                    {name}
                    <h2>{data[percent]?.toFixed(1)} %</h2>
                    <h2>{data[amount]?.toFixed(1)} ₹</h2>
                </div>
            ))}
        </div>
    );
}
