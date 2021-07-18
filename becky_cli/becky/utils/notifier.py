import smtplib, ssl

class Notifier:

    def __init__(self, backup):
        self.backup = backup

    def set_parameters(self, args):
        """
        Adds notifier specific parameters from args into the backup model
        """
        if args['type'] == 'smtp':
            self._add_smtp_parameters(args)
        else:
            raise NotImplementedError(f"Notifier -{args['type']} not supported.")

    def _add_smtp_parameters(self, args):
        """
        Adds SMTP params from args to the backup model.
        """
        params = self.backup.notifier_params
        params['type'] =  args['type']
        params['smtp_server'] =  args['smtp_server']
        params['sender_email'] =  args['sender_email']
        params['receiver_email'] =  args['receiver_email']
        params['smtp_password'] = args['smtp_password']
        self.backup.email_params = params

    def send_notification(self, title, text):
        """
        Sends a notification with the given title and text.
        """
        notifier_type = self.backup.notifier_params.get('type', None)
        if notifier_type == 'smtp':
            self._send_smtp_notification(title, text)
        else:
            print(f"Notification type {notifier_type} is not valid!")


    def _send_smtp_notification(self, title, text):
        """
        Sends an email using smtp.
        """
        params = self.backup.notifier_params
        context = ssl.create_default_context()
        message = f'Subject: {title} \n\n {text}'
        try:
            server = smtplib.SMTP(params['smtp_server'], 587)
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(params['sender_email'], params['smtp_password'])
            server.sendmail(params['sender_email'], params['receiver_email'], message)
        except Exception as e:
            import pdb;pdb.set_trace()
            print(e)
        finally:
            server.quit()
