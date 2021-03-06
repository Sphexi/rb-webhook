import sys, smtplib, json, html, email, datetime, os
from flask import Flask, request, abort
from email.message import EmailMessage

app = Flask(__name__)

emailBody = """
Webhook Dump
"""

@app.route('/', methods=['POST'])
def webhook():
	print("webhook"); sys.stdout.flush()
	if request.method == 'POST':
		if request.json is not None:
			emailBody = """
				Webhook Dump


				Date: {}
				Time: {}

				Request IP: {}
				Request Method: {}
				Request Headers: {}


				Request Content-Type: {}


				Request Body: {}
				""".format(datetime.date.today(),datetime.datetime.now().time(),request.remote_addr,request.method,json.dumps(dict(request.headers)),request.content_type,json.dumps(request.json))
			print(request.json)
			print(json.dumps(request.json))
		elif request.form is not None:
			emailBody = """
				Webhook Dump


				Date: {}
				Time: {}

				Request IP: {}
				Request Method: {}
				Request Headers: {}


				Request Content-Type: {}


				Request Body: {}
				""".format(datetime.date.today(),datetime.datetime.now().time(),request.remote_addr,request.method,json.dumps(dict(request.headers)),request.content_type,json.dumps(request.form.to_dict()))
			
			print("form data submitted")
			print(emailBody)
		else:
			abort(400)

		message = EmailMessage()
		message['Subject'] = 'Recurring Billing Webhook'
		message['From'] = os.environ.get('FROM-EMAIL')
		message['To'] = os.environ.get('ALERT-EMAIL')
		message.set_content(emailBody)

		server = smtplib.SMTP_SSL(os.environ.get('SMTP-ADDR'), 465)

		try:
			server.login(os.environ.get('SMTP-USER'), os.environ.get('SMTP-PASS'))
			server.send_message(message)
		finally:
			server.quit()
		return '', 200
	else:
		abort(400)


if __name__ == '__main__':
	app.run(host='0.0.0.0')