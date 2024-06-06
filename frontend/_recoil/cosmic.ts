import { atom } from "recoil";

export const investmentFormDataRecoil = atom({
    key: "formData",
    default: {},
});

//location, years_to_retire, salary, investment_amount, current_savings, debt, other_expenses, number_of_dependents, current_invested_amount, bank