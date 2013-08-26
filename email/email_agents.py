import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os


class sendEmail:
   def __init__(self, username, password, name = ""):
		self.user = username
		self.pwd = password
		if name=="":
			name = username
		self.name = name

	def mail(self,to, subject, text, attach = []):
		msg = MIMEMultipart()

		msg['From'] = self.name
		msg['To'] = to
		msg['Subject'] = subject

		msg.attach(MIMEText(text))

		for a in attach:
			part = MIMEBase('application', 'octet-stream')
			part.set_payload(open(a, 'rb').read())
			Encoders.encode_base64(part)
			part.add_header('Content-Disposition',
				 'attachment; filename="%s"' % os.path.basename(a))
			msg.attach(part)

		mailServer = smtplib.SMTP("smtp.gmail.com", 587)
		mailServer.ehlo()
		mailServer.starttls()
		mailServer.ehlo()
		mailServer.login(self.user, self.pwd)
		mailServer.sendmail(self.user, to, msg.as_string())
		# Should be mailServer.quit(), but that crashes...
		mailServer.close()

#example
email = sendEmail("<your gmail id>", "<Your gmail password>","<Your name>")
email.mail("<to>", "Mail from Python", "Hello. blah blah blah")

# mail("some.person@some.address.com",
   # "Hello from python!",
   # "This is a email sent with python",
   # "my_picture.jpg")
   