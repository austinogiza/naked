< script >
    function MakePayment() {
        var handler = paystackPop.setup({
                key = ‘public_key’ //public key from your paystack
                account
                email: {
                    {
                        email
                    }
                },
                amount: {
                    {
                        amount
                    }
                },
                currency: "NGN",
                ref: " " + Math.floor((Math.random() * 100000000) + 1),
                callback: function (response) {
                    alert("congrats transaction successful, your transcation id is" + response.reference);
                },
                onclose: function () {
                    alert('window closed')
                },
            }),
            handler.openIframe();
    }
window.onload = MakePayment(); <
/script>