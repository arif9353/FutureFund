import { static_investment_data } from "@/_components/static_investment_data";
import { atom } from "recoil";

export const investmentFormDataRecoil = atom({
    key: "formData",
    default: {},
});

export const PopupDataRecoil = atom({
    key: "popupData",
    default: {},
});

export const allocationDataRecoil = atom({
    key: "allocationData",
    default: static_investment_data,
});
//location, years_to_retire, salary, investment_amount, current_savings, debt, other_expenses, number_of_dependents, current_invested_amount, bank