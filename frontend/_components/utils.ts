export const API_URL = 'http://localhost:8000';

export function formatIndianPrice(number: any) {
    // Convert the number to a string
    let numStr = number.toString();
    // Split the number into integer and decimal parts if any
    let [integerPart, decimalPart] = numStr.split('.');

    // Regex to insert commas in the integer part in the Indian format
    let lastThreeDigits = integerPart.slice(-3);
    let otherDigits = integerPart.slice(0, -3);
    if (otherDigits !== '') {
        lastThreeDigits = ',' + lastThreeDigits;
    }
    let indianFormattedNumber = otherDigits.replace(/\B(?=(\d{2})+(?!\d))/g, ",") + lastThreeDigits;

    // Append the decimal part if it exists
    if (decimalPart) {
        indianFormattedNumber += '.' + decimalPart;
    }

    return indianFormattedNumber;
}