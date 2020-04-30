var submitFunction = async function (event) {
    event.preventDefault();
    var transactionData = {
        email: "test@paystack.com",
        amount: 100,
        key: "pk_test_7ba0aaceedcecce5291d23553c0a53f5b7bc2a87"
    };

    var transaction = await Paystack.Transaction.request(transactionData);

    var card = {
        number: "4084084084084081",
        cvv: "408",
        month: "12",
        year: "20"
    };

    var validation = Paystack.Card.validate(card);

    // validate card 
    if (validation.isValid) {
        await transaction.setCard(card);
        var chargeResponse = await transaction.chargeCard();

        // Handle the charge responses
        if (chargeResponse.status === "success") {
            alert("Payment completed!");
        }

        // Another charge response example
        if (chargeResponse.status === "auth") {
            const token = 123456;
            const authenticationResponse = await transaction.authenticateCard(token);
            if (authenticationResponse.status === "success") {
                alert("Payment completed!");
            }
        }
    }

};

var form = document.getElementById("paystack-card-form");

form.addEventListener("submit", submitFunction, true);