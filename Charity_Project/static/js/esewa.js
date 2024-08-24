function generateSignature(secretKey, parameters) {
    const signedFieldNames = ['tAmt', 'amt', 'txAmt', 'psc', 'pdc', 'scd', 'pid', 'sid', 'su', 'fu'];
    let stringToSign = signedFieldNames.map(field => `${field}=${parameters[field]}`).join('&');
    return CryptoJS.HmacSHA256(stringToSign, secretKey).toString(CryptoJS.enc.Hex);
}

function submitPayment() {
    const form = document.getElementById('esewa-form');
    const secretKey = '8gBm/:&EnhH.1/q';  // Replace with your actual secret key
    const parameters = {
        tAmt: document.querySelector('input[name="tAmt"]').value,
        amt: document.querySelector('input[name="amt"]').value,
        txAmt: document.querySelector('input[name="txAmt"]').value,
        psc: document.querySelector('input[name="psc"]').value,
        pdc: document.querySelector('input[name="pdc"]').value,
        scd: document.querySelector('input[name="scd"]').value,
        pid: document.querySelector('input[name="pid"]').value,
        sid: document.querySelector('input[name="sid"]').value,
        su: document.querySelector('input[name="su"]').value,
        fu: document.querySelector('input[name="fu"]').value
    };
    
    const signature = generateSignature(secretKey, parameters);
    document.getElementById('signature').value = signature;
    
    form.submit();
}
