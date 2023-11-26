from kineticemail import KineticEmail
from kineticpdf import KineticPdf
from kineticforms import KineticForms
import copy


class KineticGlue:
    def __init__(self, connection_path, email_path):
        self.kf = KineticForms(connection_path)
        self.ke = KineticEmail(email_path)

    def is_pdf_blank(self, message):
        default_keys = ["message_number", "from_address", "to_address", "forwarded", "original_sender",
                        "original_recipient", "subject", "body", "Author", "CreationDate",
                        "ModDate", "Producer", "Title", "Keywords"]
        not_found = True
        for key in message:
            if key not in default_keys:
                if message[key] != "" and message[key] is not None:
                    not_found = False

        return not_found

    def save_email_message(self, message):
        # Save Email Message so conversations can be continued without being in the
        # reply stream.
        pass

    def is_email_processed(self, message):
        # Boolean to determine if an email has already been processed.
        pass

    def is_attachment_processed(self, attachment):
        # Boolean returns true if an attachment was processed.
        pass

    def is_reply_processed(self, message):
        # Boolean returns true if a reply was sent.
        pass

    def send_reply(self, message):
        # Send a reply to an email.
        pass

    def post_pdf_email(self, attachment_path, mailbox, message_function=None,
                       attachment_function=None, noatttachment_function=None, blankattachment_function=None):
        # Get the List of Emails and Forms.

        lst = self.ke.get_mailbox_messages(attachment_path, mailbox, None,
                                                KineticPdf.process_pdf_form)

        if lst['error_code']=="0":
            data=lst['data']
            output=[]
            for i in data:
                message = copy.deepcopy(i)
                if 'attachment_results' in i:
                    print('attachment_results')
                    print(i)
                    del message['attachment_results']
                    attachment_results = i['attachment_results']
                    if isinstance(attachment_results, list):
                        for attachment in i['attachment_results']:
                            print('attachment')
                            print(attachment)
                            if isinstance(attachment, list):
                                pass
                            elif isinstance(attachment, dict):
                                message = copy.deepcopy(i)
                                tmp = {}
                                if 'info' in attachment:
                                    metadata = attachment['info']
                                    for key in metadata:
                                        message[key] = metadata[key]
                                if 'form' in attachment:
                                    form = attachment['form']
                                    for key in form:
                                        message[key] = form[key]
                                message['pdf_file_path'] = attachment['pdf_file_path']

                                del message['attachment_results']
                                del message['attachments']
                                del message['attachment_path']
                                del message['attachment_count']
                                del message['process_result']
                                output.append(message)
                            else:
                                output.append(message)
                        if len(i['attachment_results']) == 0:
                            # message.pop('attachment_results')
                            message.pop('attachments')
                            message['attachment_path'] = ""
                            del message['attachment_count']
                            message.pop('process_result')
                            output.append(message)
                    else:
                        print('here 2')
                        output.append(message)
                else:
                    print('here')
                    output.append(message)

        if message_function is not None or attachment_function is not None:
            last_message_number = ""

            for i in output:
                has_attachment = True
                if 'attachment_path' in i:
                    if i['attachment_path'] == '':
                        has_attachment = False
                if 'pdf_file_path' in i:
                    if i['pdf_file_path'] == '':
                        has_attachment = False

                if i['message_number'] != last_message_number:
                    last_message_number = i['message_number']
                    if message_function is not None:
                        message_function(i)
                if attachment_function is not None:
                    if 'pdf_file_path' in i:
                        if i['pdf_file_path'] != '':
                            attachment_function(i)
                if noatttachment_function is not None:
                    if not has_attachment:
                        noatttachment_function(i)
                if blankattachment_function is not None:
                    if has_attachment:
                        if self.is_pdf_blank(i):
                            blankattachment_function(i)
        return {"errror_code": "0", "error_msg": "", "data": output }
