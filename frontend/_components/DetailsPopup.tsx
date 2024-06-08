import { PopupDataRecoil } from "@/_recoil/cosmic";
import { useRecoilState } from "recoil";

export default function DetailsPopup() {
    const [popupData, setPopupData] = useRecoilState<any>(PopupDataRecoil);
    console.log(popupData, 'popupData')
    return (
        <>
            <div className='bg-[#00000090] min-h-screen w-screen z-[99999] fixed top-0 left-0 flex justify-center items-center' onClick={() => setPopupData({})}>
                <div className="w-[90vw] mob:max-h-[60vh] pc:max-h-[70vh] bg-[#2b2e36] text-white p-4 overflow-auto rounded-md flex justify-center mob:justify-start">
                    <div className=" ">
                        {popupData?.type === 'Stocks' && <StockTable />}
                        {popupData?.type === 'Crypto' && <CryptoTable />}
                        {popupData?.type === 'Properties' && <PropertyTable />}
                        {popupData?.type === 'Bonds' && <BondTable />}
                        {popupData?.type === 'RD' && <RDTable />}
                    </div>
                </div>
            </div>
        </>
    )
}

function StockTable() {
    const [popupData, setPopupData] = useRecoilState<any>(PopupDataRecoil);

    return (
        <>
            {popupData && (
                <table className="w-[1200px] mob:text-sm mob:w-[1400px] mt-2 ">
                    <thead className=" text-white">
                        <tr>
                            <th className=" py-2">Name</th>
                            <th className=" py-2">Price</th>
                            <th className=" py-2">Target Price</th>
                            <th className=" py-2">Revenue</th>
                            <th className=" py-2">Profit %</th>
                            <th className=" py-2">Risk Level</th>
                            <th className=" py-2">Quantity</th>
                        </tr>
                    </thead>
                    <tbody>
                        {popupData?.data?.High.map((stock: any, index: number) => (
                            <tr key={index}>
                                <td className=" pt-4 py-2">{stock.name}</td>
                                <td className=" pt-4 py-2">{parseFloat(stock.price).toFixed(2)}</td>
                                <td className=" pt-4 py-2">{parseFloat(stock.target_price).toFixed(2)}</td>
                                <td className=" pt-4 py-2">{parseFloat(stock.revenue).toFixed(2)}</td>
                                <td className=" pt-4 py-2">{parseFloat(stock.profit_percent).toFixed(2)}</td>
                                <td className=" pt-4 py-2 capitalize text-red-400">{stock.category}</td>
                                <td className=" pt-4 py-2">{stock.quantity}</td>
                            </tr>
                        ))}
                        {popupData?.data?.Medium.map((stock: any, index: number) => (
                            <tr key={index}>
                                <td className=" pt-4 py-2">{stock.name}</td>
                                <td className=" pt-4 py-2">{parseFloat(stock.price).toFixed(2)}</td>
                                <td className=" pt-4 py-2">{parseFloat(stock.target_price).toFixed(2)}</td>
                                <td className=" pt-4 py-2">{parseFloat(stock.revenue).toFixed(2)}</td>
                                <td className=" pt-4 py-2">{parseFloat(stock.profit_percent).toFixed(2)}</td>
                                <td className=" pt-4 py-2 capitalize text-orange-300">{stock.category}</td>
                                <td className=" pt-4 py-2">{stock.quantity}</td>
                            </tr>
                        ))}
                        {popupData?.data?.Low.map((stock: any, index: number) => (
                            <tr key={index}>
                                <td className=" pt-4 py-2">{stock.name}</td>
                                <td className=" pt-4 py-2">{parseFloat(stock.price).toFixed(2)}</td>
                                <td className=" pt-4 py-2">{parseFloat(stock.target_price).toFixed(2)}</td>
                                <td className=" pt-4 py-2">{parseFloat(stock.revenue).toFixed(2)}</td>
                                <td className=" pt-4 py-2">{parseFloat(stock.profit_percent).toFixed(2)}</td>
                                <td className=" pt-4 py-2 capitalize text-green-300">{stock.category}</td>
                                <td className=" pt-4 py-2">{stock.quantity}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </>
    )
}
function CryptoTable() {
    const [popupData, setPopupData] = useRecoilState<any>(PopupDataRecoil);

    return (
        <>
            {popupData && (
                <table className="w-[1200px] mob:text-sm mob:w-[1400px] mt-2 ">
                    <thead className="text-white">
                        <tr>
                            <th className=" py-2">Category</th>
                            <th className=" py-2">Name</th>
                            <th className=" py-2">Last Price</th>
                            <th className=" py-2">Expected Price</th>
                            <th className=" py-2">Change Rate</th>
                            <th className=" py-2">Profit Amount</th>
                            <th className=" py-2">Profit %</th>
                            <th className=" py-2">Quantity</th>
                            <th className=" py-2">Risk Level</th> {/* Added Risk Level column */}
                        </tr>
                    </thead>
                    <tbody>
                        {Object.keys(popupData.data).map((category: string) => (
                            popupData.data[category].map((crypto: any, index: number) => (
                                <tr key={index}>
                                    <td className="pt-4 py-2">{category}</td>
                                    <td className="pt-4 py-2">{crypto.name}</td>
                                    <td className="pt-4 py-2">{parseFloat(crypto.last_price).toFixed(2)}</td>
                                    <td className="pt-4 py-2">{parseFloat(crypto.expected_price).toFixed(2)}</td>
                                    <td className="pt-4 py-2">{parseFloat(crypto.changePercent).toFixed(2)}</td>
                                    <td className="pt-4 py-2">{parseFloat(crypto.profit_amount).toFixed(2)}</td>
                                    <td className="pt-4 py-2">{parseFloat(crypto.profit_percentage).toFixed(2)}</td>
                                    <td className="pt-4 py-2">{parseFloat(crypto.quantity).toFixed(2)}</td>
                                    {category === "High" && <td className="pt-4 py-2 text-green-300">{category}</td>}
                                    {category === "Medium" && <td className="pt-4 py-2 text-orange-300">{category}</td>}
                                    {category === "Low" && <td className="pt-4 py-2 text-red-400">{category}</td>}
                                </tr>
                            ))
                        ))}
                    </tbody>
                </table>
            )}
        </>
    )
}

const PropertyTable = () => {
    const [popupData, setPopupData] = useRecoilState<any>(PopupDataRecoil);

    return (
        <>
            {popupData && (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 py-5">
                    {popupData.data.map((property: any, index: number) => (
                        <div key={index} className=" shadow-lg p-4 border rounded-md">
                            <h3 className="text-lg font-semibold">{property.title}</h3>
                            <p><span className="font-bold">Price:</span> {property.price.toFixed(2)}</p>
                            <p><span className="font-bold">Rate:</span> {property.rate}</p>
                            <p><span className="font-bold">Address:</span> {property.address}</p>
                            <p><span className="font-bold">Area:</span> {property.area}</p>
                            <p><span className="font-bold">Estimated EMI:</span> {property.estimated_emi}</p>
                            <p><span className="font-bold">Location:</span> {property.location}</p>
                            <p><span className="font-bold">Goal Price:</span> {property.goal_price.toFixed(2)}</p>
                            <p><span className="font-bold">Profit:</span> {property.profit.toFixed(2)}</p>
                            {/* <p><span className="font-bold">Profit %:</span> {property.profit_percentage.toFixed(2)}</p> */}
                        </div>
                    ))}
                </div>
            )}
        </>
    )
};

const BondTable = () => {
    const [popupData, setPopupData] = useRecoilState<any>(PopupDataRecoil);

    return (
        <>
            {popupData && (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 py-5">
                    {popupData.data.map((bond: any, index: number) => (
                        <div key={index} className="shadow-lg p-4 border rounded-md">
                            <h3 className="text-lg font-semibold">{bond.name}</h3>
                            <p><span className="font-bold">Coupon:</span> {bond.coupon}</p>
                            <p><span className="font-bold">Maturity:</span> {bond.maturity}</p>
                            <p><span className="font-bold">Yield:</span> {bond.yield}</p>
                            <p><span className="font-bold">Price:</span> {bond.price}</p>
                            <p><span className="font-bold">Frequency:</span> {bond.frequency}</p>
                            <p><span className="font-bold">Estimated Face Value:</span> {bond.estimated_face_value}</p>
                            <p><span className="font-bold">Bond Profit:</span> {bond.bond_profit}</p>
                        </div>
                    ))}
                </div>
            )}
        </>
    )
};

const RDTable = () => {
    const [popupData, setPopupData] = useRecoilState<any>(PopupDataRecoil);

    return (
        <>
            {popupData && (
                <div className="flex flex-col py-10">
                    <h3 className="text-lg font-bold text-slate-200 ">Recurring Deposits</h3>
                    <div className=" p-4 rounded-md flex flex-col gap-3">
                        <p><span className="font-medium">Investment Amount:</span> {popupData.data.investment_amount.toFixed(2)}</p>
                        <p><span className="font-medium">Maturity Amount:</span> {popupData.data.maturity_amount.toFixed(2)}</p>
                        <p><span className="font-medium">Profit Amount:</span> {popupData.data.profit_amount.toFixed(2)}</p>
                        <p><span className="font-medium">Tenure (months):</span> {popupData.data.tenure_months}</p>
                        <p><span className="font-medium">Interest Rate:</span> {popupData.data.interest_rate}%</p>
                    </div>
                </div>
            )}
        </>
    )
};
