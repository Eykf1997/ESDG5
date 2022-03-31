from flask import Flask, render_template, url_for, request, abort, jsonify
import json

import stripe

app = Flask(__name__)

app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_51KeFRIImsLnkA7wnfZXAD9cYt0FZjFMF89IrHfB42LRqC1oUe4LXuR4DajAOlS7tmJdpFe2bBndwekrsmQ2U9xjO00beVTKajW'
app.config['STRIPE_SECRET_KEY'] = 'sk_test_51KeFRIImsLnkA7wnOnnKaXjxyEmQ6ArFQgdnzwZFv8fKiou5WioQsMffnfyqnnFv5UvILdds4QC6fEf70er848c200fLAoAe5V'

stripe.api_key = app.config['STRIPE_SECRET_KEY']

@app.route('/', methods =["GET", "POST"])
def index():
    return render_template('index.html')

@app.route('/stripe_pay', methods =["GET","POST"]) #******
def stripe_pay():
    data = json.loads(request.data)
    print(type(data))
    print(data)
    quantity = data['quantity']
    product = data['product']
    price = ''
    print(product)
    if product == 'Sunflower':
        price = 'price_1KeMtfImsLnkA7wnVSIuQ8FL'
    elif product == 'Pink':
        price = 'price_1KecioImsLnkA7wnXCp8Co2d'
    elif product == 'Roses':
        price = 'price_1KecjOImsLnkA7wn7kNOcRVI'
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': price,
            'quantity': quantity,
        }],
        mode='payment',
        success_url=url_for('thanks', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('index', _external=True),
    )
    return {
        'checkout_session_id': session['id'], 
        'checkout_public_key': app.config['STRIPE_PUBLIC_KEY']
    }

@app.route('/thanks')
def thanks():
    return render_template('thanks.html')

@app.route('/stripe_webhook', methods=['POST'])
def stripe_webhook():
    print('WEBHOOK CALLED')

    if request.content_length > 1024 * 1024:
        print('REQUEST TOO BIG')
        abort(400)
    payload = request.get_data()
    sig_header = request.environ.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = 'whsec_5fd44bedbf7357b7378942aa3a5e0003742cd505f7aec565a5ee1b616e897f02'
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        print('INVALID PAYLOAD')
        return {}, 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print('INVALID SIGNATURE')
        return {}, 400

    # Handle the checkout.session.completed event
    amount = 0
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(session)
        line_items = stripe.checkout.Session.list_line_items(session['id'], limit=1)
        print(line_items)
        print(line_items['data'][0]['description'])
        amount = line_items['data'][0]['amount_total']/100
        print(f'{amount:.2f}')
    return {}



if __name__ == '__main__':
    app.run()