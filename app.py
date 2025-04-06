from flask import Flask, abort, redirect, render_template, request
from liqpay.liqpay3 import LiqPay
from config import config
from mqtt_utils import send_parking_command
import time

app = Flask(__name__)

def get_liqpay() -> LiqPay:
    return LiqPay(config.liqpay_pub_key, config.liqpay_private_key)


@app.route("/pay", methods=["GET", "POST"])
def pay():
    if request.method == "POST":
        car_number = request.form['car_number']
        hours = int(request.form['hours'])
        amount = float(request.form['amount'])
        currency = request.form['currency']

        liqpay = get_liqpay()

        order_id = f"park_{car_number}_{int(time.time())}"
        params = {
            "private_key": config.liqpay_private_key,
            "public_key": config.liqpay_pub_key,
            "action": "pay",
            "amount": amount,
            "currency": currency,
            "description": f"Парковка на {hours} г. для авто {car_number}",
            "order_id": order_id,
            "version": "3",
            "sandbox": config.liqpay_sandbox,
            "result_url": f"{config.base_url}/result",
            "server_url": f"{config.base_url}/callback"
        }
        
        data, signature = liqpay.get_data_end_signature("cnb_form", params)
        liqpay_url = f"https://www.liqpay.ua/api/3/checkout?data={data}&signature={signature}"
        
        return redirect(liqpay_url)
    
    return render_template("pay.html")

@app.route("/callback", methods=["POST"])
def callback():
    data = request.form.get("data")
    signature = request.form.get("signature")

    if not data or not signature:
        abort(400)

    liqpay = get_liqpay()
    
    calculated_sign = liqpay.str_to_sign(liqpay._private_key + data + liqpay._private_key)
    if signature != calculated_sign:
        abort(400)

    dict_data = liqpay.decode_data_from_str(data)

    if dict_data.get("status") == "success":
        try:
            send_parking_command()
        except Exception as e:
            print(f"Помилка: {e}")

    return "OK"


@app.route("/result")
def result():
    return "<h2>Дякуємо за оплату!</h2>"

