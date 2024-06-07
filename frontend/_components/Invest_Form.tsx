import { allocationDataRecoil, investmentFormDataRecoil } from '@/_recoil/cosmic';
import React, { useEffect, useState } from 'react';
import { useRecoilState } from 'recoil';
import { FaMapMarkerAlt, FaRupeeSign, FaBuilding, FaUser } from 'react-icons/fa';
import { HiOutlineSparkles } from 'react-icons/hi2';
import toast from 'react-hot-toast';
import axios from 'axios';
import { API_URL } from './utils';
import { PuffLoader } from 'react-spinners';

const InvestmentForm = () => {
    const [formData, setFormData] = useRecoilState<any>(investmentFormDataRecoil);
    const [localFormData, setLocalFormData] = useState(formData);
    const [_, setData] = useRecoilState(allocationDataRecoil);
    const [loading, setLoading] = useState(false);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        const { name, value } = e.target;
        setLocalFormData((prevData: any) => ({
            ...prevData,
            [name]: value,
        }));
    };

    const [detailsObj, setDetailsObj] = useState({})
    useEffect(() => {
        "use client";
        let x: any = localStorage.getItem("details")

        setDetailsObj(JSON.parse(x))
    }, [])

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();

        const requiredFields = ['salary', 'investment_amount', 'current_savings', 'debt', 'other_expenses', 'number_of_dependents', 'current_invested_amount', 'bank', 'years_to_retire'];
        const isAnyFieldEmpty = requiredFields.some(field => !localFormData[field]);

        if (isAnyFieldEmpty) {
            toast.error('Please fill in all fields');
            console.log("Hello NAN")

            return;
        }

        // Validate that numbers are numbers
        const numberFields = ['salary', 'investment_amount', 'current_savings', 'debt', 'other_expenses', 'number_of_dependents', 'current_invested_amount'];
        const isAnyFieldNotNumber = numberFields.some(field => isNaN(localFormData[field]));


        if (isAnyFieldNotNumber) {
            toast.error('Please enter valid numbers for salary, investment amount, current savings, debt, other expenses, number of dependents, and current invested amount');
            console.log("Hello NAN")
            return;
        }
        console.log("Hello NAN")

        // All validations passed, call api and finally  set the form data

        console.log("making api call")

        if (localFormData) {
            setLoading(true)
            axios.post(`${API_URL}/model/`, {
                ...localFormData,
                details: detailsObj
            }).then(res => {
                console.log(":::result", res.data)
                setData(res?.data)
                setFormData(localFormData);
            }).catch(err => {
                console.error(err)
            }).finally(() => {
                setLoading(false)
            })
        }

    };

    const bankOptions = {
        "State Bank of India": "sbi_bank",
        "ICICI Bank": "icici_bank",
        "HDFC Bank": "hdfc_bank",
        "Kotak Mahindra Bank": "kotak_mahindra_bank",
        "Axis Bank": "axis_bank",
        "Bank of Baroda": "bank_of_baroda",
        "Punjab National Bank": "punjab_national_bank",
        "IDBI Bank": "idbi_bank",
        "Canara Bank": "canara_bank",
        "Union Bank of India": "union_bank_of_india",
        "Yes Bank": "yes_bank",
        "Bandhan Bank": "bandhan_bank",
        "Bank of Maharashtra": "bank_of_maharashtra",
        "IndusInd Bank": "indusind_bank",
        "Jammu and Kashmir Bank": "jammu_and_kashmir_bank",
        "Karnataka Bank": "karnataka_bank",
        "Saraswat Bank": "saraswat_bank",
        "Federal Bank": "federal_bank",
        "DBS Bank": "dbs_bank",
        "RBL Bank": "rbl_bank",
        "Indian Bank": "indian_bank",
        "Indian Overseas Bank": "indian_overseas_bank",
        "TMB Bank": "tmb_bank"
    };

    const inputFields = [
        { label: 'Salary', name: 'salary', icon: <FaRupeeSign /> },
        { label: 'Investment Amount', name: 'investment_amount', icon: <FaRupeeSign /> },
        { label: 'Current Savings', name: 'current_savings', icon: <FaRupeeSign /> },
        { label: 'Debt', name: 'debt', icon: <FaRupeeSign /> },
        { label: 'Other Expenses', name: 'other_expenses', icon: <FaRupeeSign /> },
        { label: 'Number of Dependents', name: 'number_of_dependents', icon: <FaUser /> },
        { label: 'Current Invested Amount', name: 'current_invested_amount', icon: <FaRupeeSign /> },
    ];

    const locationOptions = [
        { value: '', label: 'Select location' },
        { value: 'pune', label: 'Pune' },
        { value: 'mumbai', label: 'Mumbai' },
        { value: 'bangalore', label: 'Bangalore' },
        { value: 'chennai', label: 'Chennai' },
        { value: 'delhi', label: 'Delhi' },
        { value: 'gurgaon', label: 'Gurgaon' },
        { value: 'hyderabad', label: 'Hyderabad' },
        { value: 'noida', label: 'Noida' },
        { value: 'greater_noida', label: 'Greater Noida' },
        { value: 'ghaziabad', label: 'Ghaziabad' },
        { value: 'faridabad', label: 'Faridabad' },
    ];

    if (loading) {
        return (
            <>
                <div className='h-[calc(100vh-80px)] w-[100vw] flex justify-center items-center'>
                    <PuffLoader color="#ffffff" />
                </div>
            </>
        )
    }

    return (
        <form className="w-full max-w-lg mx-auto space-y-6 p-6 bg-[#1d1f24] rounded-lg shadow-md" onSubmit={handleSubmit}>
            <h2 className="text-2xl font-bold text-center mb-6 flex justify-center">
                <span className='gradient-text-ai'><HiOutlineSparkles className='inline' color='#9583d0' /> AI  INVESTMENT ALLOCATION </span>
            </h2>
            {/* <div className="flex items-center space-x-2 mb-4">
                <div className="text-gray-400"><FaMapMarkerAlt /></div>
                <div className="flex-1">
                    <label className="block text-gray-300 font-bold mb-1">
                        Location
                    </label>
                    <select
                        className="appearance-none block w-full bg-[#ffffff10] text-gray-300 border border-gray-700 rounded py-2 px-3 leading-tight focus:outline-none focus:bg-[#ffffff10] focus:border-blue-500"
                        name="location"
                        value={localFormData.location || ''}
                        onChange={handleChange}
                    >
                        {locationOptions.map(option => (
                            <option className='bg-[#2b2d32]' key={option.value} value={option.value}>{option.label}</option>
                        ))}
                    </select>
                </div>
            </div> */}

            <div className="flex items-center space-x-2 mb-4">
                <div className="text-gray-400"><FaBuilding /></div>
                <div className="flex-1">
                    <label className="block text-gray-300 font-bold mb-1">
                        Name of Bank
                    </label>
                    <select
                        className="appearance-none block w-full bg-[#ffffff10] text-gray-300 border border-gray-700 rounded py-2 px-3 leading-tight focus:outline-none focus:bg-[#ffffff10] focus:border-blue-500"
                        name="bank"
                        value={localFormData.bank || ''}
                        onChange={handleChange}
                    >
                        <option className='bg-[#2b2d32] ' value="" disabled>Select Bank</option>
                        {Object.entries(bankOptions).map(([label, value]) => (
                            <option className='bg-[#2b2d32]' key={value} value={value}>{label}</option>
                        ))}
                    </select>
                </div>
            </div>

            <div className="flex items-start space-x-2 mb-6">
                <div className="text-gray-400 mt-2"><FaUser /></div>
                <div className="flex-1">
                    <label className="block text-gray-300 font-medium mb-1">
                        Years to Retire : <span className='text-blue-300 underline-offset-8 underline font-bold'>{localFormData.years_to_retire}</span>
                    </label>
                    <input
                        className="appearance-auto block w-full border border-red-700 rounded leading-tight focus:outline-none focus:bg-[#ffffff10] focus:border-blue-500 mb-3 h-1 mt-3"
                        type="range"
                        min="0"
                        max="50"
                        name="years_to_retire"
                        value={localFormData.years_to_retire || 0}
                        onChange={handleChange}
                        required
                    />
                    <p className='text-slate-400 text-xs'>*Slide to select years to retire</p>
                </div>
            </div>
            {inputFields.map(({ label, name, icon }) => (
                <div className="flex items-start space-x-2 justify-start mb-4" key={name}>
                    <div className="text-gray-400 mt-2">{icon}</div>
                    <div className="flex-1">
                        <label className="block text-gray-300 font-bold mb-1">
                            {label}
                        </label>
                        <input
                            className="appearance-none block w-full bg-[#ffffff10] text-gray-300 border border-gray-700 rounded py-2 px-3 leading-tight focus:outline-none focus:bg-[#ffffff10] focus:border-blue-500"
                            type="text"
                            name={name}
                            value={localFormData[name] || ''}
                            onChange={handleChange}
                            placeholder={`Enter ${label.toLowerCase()}`}
                            autoComplete='off'
                        />
                    </div>
                </div>
            ))}

            <div className="flex justify-center">
                <button
                    type="submit"
                    className="appearance-none bg-blue-600 text-white font-bold py-2 px-4 rounded hover:bg-blue-700 focus:outline-none focus:bg-blue-700"
                >
                    Submit
                </button>
            </div>
        </form>
    );
};

export default InvestmentForm;
