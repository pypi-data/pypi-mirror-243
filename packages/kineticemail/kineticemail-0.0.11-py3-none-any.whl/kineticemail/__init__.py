#
# Kinetic Email - 2023
#    Copyright 2023 - Kinetic Seas Inc, Chicago Illinois
#    Edward Honour, Joseph Lehman
#

import re
import json
import imaplib
import smtplib
from smtplib import SMTPException, SMTPAuthenticationError, SMTPServerDisconnected
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.utils import parseaddr
import socket
from email.header import decode_header
from pathlib import Path
import tempfile
import smtplib
from email.message import EmailMessage
import os
from bs4 import BeautifulSoup
from email.policy import default

__version__ = '0.0.10'

class KineticEmail:
    # Connecton string containing filename or dict with connection info.
    # connection = { "imap_server": "", "email_address": "", "email_password": "" }
    def __init__(self, connection_path):
        if isinstance(connection_path, dict):
            self.connection_dict = connection_path
        else:
            with open(connection_path, 'r') as connection_file:
                self.connection_dict = json.load(connection_file)

    def extract_email_address(self,address_string):
        # Regular expression pattern for matching an email address
        email_pattern = r'[\w\.-]+@[\w\.-]+'

        # Search for the email address in the string
        match = re.search(email_pattern, address_string)

        # Return the found email address or None if no match is found
        return match.group(0) if match else None

    def is_email_forwarded(self, email_message):
        # Parse the email content
        msg = email.message_from_string(email_message, policy=default)

        # Check for common forwarding headers
        forwarded_headers = ['X-Forwarded-For', 'X-Forwarded-Message-Id', 'In-Reply-To', 'References']
        for header in forwarded_headers:
            if msg.get(header) is not None:
                return True

        # Additional checks can be added here based on your specific needs

        return False

    def connect_imap(self, server, email_address, email_password):
        try:
            imap = imaplib.IMAP4_SSL(server)
            imap.login(email_address, email_password)
            return imap
        except imaplib.IMAP4.abort as e:
            return {"error_code": "9000", "error_msg": "IMAP4 connection aborted: " + str(e), "data": {}}
        except imaplib.IMAP4.error as e:
            return {"error_code": "9000", "error_msg": "IMAP4 error occurred: " + str(e), "data": {}}
        except socket.gaierror as e:
            return {"error_code": "9000", "error_msg": "Address-related socket error occurred: " + str(e), "data": {}}
        except socket.timeout as e:
            return {"error_code": "9000", "error_msg": "Socket timeout occurred: " + str(e), "data": {}}
        except socket.error as e:
            return {"error_code": "9000", "error_msg": "Socket error occurred: " + str(e), "data": {}}
        except Exception as e:  # A generic catch-all for any other exceptions
            return {"error_code": "9000", "error_msg": "An unexpected error occurred: " + str(e), "data": {}}


    def reply_to_email(self, message_id, reply_body, attachment = None):
        # Parse the original email
        j = self.get_message_by_id(message_id,"Inbox")

        msg = email.message_from_string(j)

        smtp_server = self.connection_dict['smtp_server']
        smtp_port = self.connection_dict['smtp_port']
        smtp_username = self.connection_dict['email_address']
        smtp_password = self.connection_dict['email_password']

        m = str(msg['Message-ID'])
        m = m.replace('\r', '').replace('\n', '')
        s = str(msg['Subject'])
        s = s.replace('\r', '').replace('\n', '')

        # Create a reply message
        reply = EmailMessage()
        reply['To'] = msg['From']
        reply['From'] = smtp_username
        reply['Subject'] = 'Re: ' + s
        reply['In-Reply-To'] = m
        reply.set_content(reply_body)

        if attachment is not None:
            with open(attachment, 'rb') as file:
                file_data = file.read()
                file_name = file.name
                reply.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)


        # Include the original email's Message-ID in 'References'
        if msg.get('References'):
            mr = msg['References']
            mr = mr.replace('\r', '').replace('\n', '')
            reply['References'] = mr + ' ' + m
        else:
            reply['References'] = m

        # Send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(reply)


    #
    # Function to download an attachment from an email and save to
    # the filesystem.
    #
    def download_attachment(self, emailPart, file_path):
        output_file_name = file_path + '/' + emailPart.get_filename()
        open(output_file_name, 'wb').write(emailPart.get_payload(decode=True))
        return output_file_name

    #
    # Function to move a file from one folder (mailbox) to another.
    #
    def move_file_mailbox(self, imap, messageNum, targetMailbox):
        status, email_data = imap.fetch(messageNum, '(UID)')
        uid = email_data[0].split()[-1].decode("utf-8")  # Get the UID
        uid = uid[:-1]
        a, b = imap.uid('COPY', uid, targetMailbox)
        self.imap.uid('STORE', uid, '+FLAGS', '(\Deleted)')

    def extract_forwarded_details(self, email_message):
        # Parse the email content
        msg = email.message_from_string(email_message, policy=default)

        # Initialize details
        original_sender = None
        original_recipient = None
        original_message = None
        attachments = []

        # Assuming the original details are in the email body
        if msg.is_multipart():
            for part in msg.walk():
                # Check for text/plain parts to find the original message
                if part.get_content_type() == 'text/plain':
                    body = part.get_payload(decode=True).decode('utf-8')
                    # Here you'll need to write custom logic to parse body
                    # Example (this is highly simplified and may not work for all emails):
                    lines = body.split('\n')
                    for i, line in enumerate(lines):
                        if line.startswith("From:"):
                            original_sender = parseaddr(line[6:].strip())[1]
                        elif line.startswith("To:"):
                            original_recipient = self.extract_email_address(line[4:].strip())
                        elif line.startswith("Subject:"):
                            original_message = "\n".join(lines[i + 1:])

                # Check for attachments
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue

                filename = part.get_filename()
                if filename is not None:
                    # attachment_content = part.get_payload(decode=True)
                    attachments.append(filename)

        # Return the extracted details
        return original_sender, original_recipient, original_message, attachments


    #
    # Get all messages from an imap mailbox and return the
    # status of the mailbox request and messages.
    #
    def get_imap_messages(self, imap, mailbox, search="ALL"):
        try:
            imap.select(mailbox)
            status, messages = imap.search(None, search)
            return status, messages
        except Exception as e:
            return {"error_code": "9000", "error_msg": "An unexpected error occurred: " + str(e), "data": {}}


    def get_email_attachments(self, imap, msgnums):
        for msgnum in msgnums[0].split():
            _, data = imap.fetch(msgnum, '(BODY.PEEK[])')
            message = email.message_from_bytes(data[0][1])
            for part in message.walk():
                if part.get_content_type() == "text/plain":
                    pass
                if part.get_content_maintype() != "multipart" and part.get('Content-Disposition') is not None:
                    self.download_attachment(part, "/tmp")

    #
    # Close the imap mailbox connection.
    #
    def close_imap_mail(self, imap):
        imap.expunge()
        imap.close()
        imap.logout()

    #
    # process function is a function to process the entire email without the attachments.  The email
    #                  dictionary object is the only parameter.
    # process_attachment function is a function to process each attachment.  The email object and filename of the
    #                  attachment are the parameters.
    #

    def get_message_by_id(self, in_message_id, mailbox="Inbox", reply_function=None):
        imap = self.connect_imap(
            self.connection_dict['imap_server'],
            self.connection_dict['email_address'],
            self.connection_dict['email_password']
        )
        try:
            status, messages = self.get_imap_messages(imap, mailbox)
        except Exception as e:  # A generic catch-all for any other exceptions
            return {"error_code": "9000", "error_msg": "An unexpected error occurred: " + str(e), "data": {}}

        email_data = []

        #
        # only process if retrieval is OK.
        #
        if status == 'OK':
            output = None
            message_numbers = messages[0].split()
            for num in message_numbers:
                status, data = imap.fetch(num, '(BODY.PEEK[])')
                msg = email.message_from_bytes(data[0][1])
                message_id = msg.get('Message-ID')
                message_id = message_id.strip('<>') if message_id else "unknown"
                if str(in_message_id) == str(message_id):
                    r, d = imap.fetch(num, '(RFC822)')
                    raw_email = d[0][1].decode('utf-8')
                    if reply_function is not None:
                        output = reply_function(raw_email)
                    else:
                        output = raw_email
            return output

    def get_mailbox_messages(self, attachment_path='', mailbox="Inbox", process_function=None,
                             attachment_function=None):

        imap = self.connect_imap(
            self.connection_dict['imap_server'],
            self.connection_dict['email_address'],
            self.connection_dict['email_password']
        )

        # Get the mailbox status and all directories from the inbox.
        #
        try:
            status, messages = self.get_imap_messages(imap, mailbox)
        except Exception as e:  # A generic catch-all for any other exceptions
            return {"error_code": "9000", "error_msg": "An unexpected error occurred: " + str(e), "data": {}}

        # list to return data.
        email_data = []

        #
        # only process if retrieval is OK.
        #
        if status == 'OK':
            #
            # Convert the result list to individual message numbers
            #
            message_numbers = messages[0].split()

            #
            # Process each email.
            for num in message_numbers:
                # Fetch the email by its number (RFC822 protocol for full email)
                # status, data = imap.fetch(num, '(RFC822)')
                status, data = imap.fetch(num, '(BODY.PEEK[])')
                # r, d = imap.fetch(num, '(RFC822)')
                # raw_email = d[0][1].decode('utf-8')
                # self.reply_to_email(raw_email,"Test")

                if status == 'OK':
                    # Parse the email content
                    msg = email.message_from_bytes(data[0][1])
                    # msg = email.message_from_string(data[0][1])
                    raw_email = data[0][1].decode('utf-8')
                    forwarded = 'N'
                    original_sender = ''
                    original_recipient = ''
                    if self.is_email_forwarded(raw_email):
                        forwarded = 'Y'
                        x = self.extract_forwarded_details(raw_email)
                        original_sender = x[0]
                        original_recipient = x[1]

                    #
                    # Get message id, recipient email, subject, and sender
                    #
                    message_id = msg.get('Message-ID')
                    message_id = message_id.strip('<>') if message_id else "unknown"
                    to_address = msg.get('To')

                    subject = decode_header(msg["subject"])[0][0]
                    if isinstance(subject, bytes):
                        subject = subject.decode()

                    sender = decode_header(msg.get("From"))[0][0]
                    if isinstance(sender, bytes):
                        sender = sender.decode()

                    # Count and download attachments.
                    #
                    # Only download attachments if a path was specified.
                    #
                    # Initialize attachment count
                    body = ""
                    attachment_count = 0
                    attachment_filenames = []
                    #
                    # Both single part and multipart emails may have attachments.
                    #      We only download multipart.
                    #
                    if msg.is_multipart():
                        for part in msg.walk():
                            #
                            # Check if part is an attachment
                            #
                            content_type = part.get_content_type()
                            if content_type == "text/plain":
                                body = part.get_payload(decode=True).decode()

                                # Extracting HTML content and converting it to text
                            elif content_type == "text/html":
                                html_content = part.get_payload(decode=True).decode()
                                soup = BeautifulSoup(html_content, "html.parser")
                                body = soup.get_text()

                            if part.get_content_maintype() == 'multipart' or part.get('Content-Disposition') is None:
                                continue
                            disposition = part.get('Content-Disposition')
                            if attachment_path != '' and attachment_path is not None:
                                if 'attachment' in disposition or 'filename' in disposition:
                                    filename = part.get_filename()
                                    if filename:
                                        filename = decode_header(filename)[0][0]
                                        if isinstance(filename, bytes):
                                            filename = filename.decode()
                                        if '/' in filename:
                                            f = filename.split('/')
                                            filename = f[-1]
                                        if attachment_path != '' and attachment_path is not None:

                                            # output_file_name = attachment_path + '/' + message_id + '-' + filename
                                            output_file_name = attachment_path + '/' + message_id + '-' + filename
                                            file_path = Path(attachment_path)

                                            if file_path.exists():
                                                open(output_file_name, 'wb').write(part.get_payload(decode=True))
                                            else:
                                                return {"error_code":"9898", "error_msg": "Output PDF Path does not exist", "data": {}}
                                        else:
                                            output_file_name = filename

                                        attachment_filenames.append(output_file_name)
                                attachment_count += 1
                        if attachment_count == 0:
                            pass
                    else:
                        #
                        # Email does not have multiple parts, so we can identify attachments but
                        # not download them.
                        #
                        payload = msg.get_payload(decode=True).decode()
                        if msg.get_content_type() == "text/plain":
                            body = payload
                        elif msg.get_content_type() == "text/html":
                            soup = BeautifulSoup(payload, "html.parser")
                            body = soup.get_text()

                        if msg.get_content_maintype() != 'text' and msg.get('Content-Disposition') is not None:
                            filename = msg.get_filename()
                            if filename:
                                filename = decode_header(filename)[0][0]
                                if isinstance(filename, bytes):
                                    filename = filename.decode()

                                attachment_filenames.append("single-part:" + filename)
                            attachment_count += 1

                    # Append email to the list.

                    em = {'message_number': num.decode(),
                          'message_id': message_id,
                          'from_address': self.extract_email_address(sender),
                          'to_address': self.extract_email_address(to_address),
                          'forwarded': forwarded,
                          'original_sender': original_sender,
                          'original_recipient': original_recipient,
                          'subject': subject,
                          'body': body,
                          'attachment_path': attachment_path,
                          'attachment_count': attachment_count,
                          'attachments': attachment_filenames}

                    if process_function is not None:
                        result = process_function(self.connection_dict,em)
                        em['process_result'] = result
                    else:
                        em['process_result'] = {}

                    attachment_results = []
                    if attachment_function is not None:
                        for a_path in em['attachments']:
                            path = str(a_path)
                            input_dict= {
                                "connection": self.connection_dict,
                                "input_path": a_path
                            }
                            result = attachment_function(input_dict)
                            attachment_results.append(result)
                        em['attachment_results'] = attachment_results
                    else:
                        em['attachment_results'] = []

                    email_data.append(em)

        return {"error_code": "0", "error_msg": "", "data": email_data}

    def email_form(self, j, connection, attachment):

        message = MIMEMultipart()
        message['To'] = j['to']
        message['From'] = j['from']
        message['Subject'] = j['subject']
        body = j['body']
        message.attach(MIMEText(body,'plain'))

        fn = attachment.split("/")[-1]
        try:
            with open(attachment, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
        except FileNotFoundError:
            return {"error_code": "9011", "error_msg": "File " + attachment + " not found.", "data": {}}

        try:
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename= {fn}')
            message.attach(part)
        except Exception as e:
            return {"error_code": "9011", "error_msg": "An unexpected error occurred." + str(e), "data": {}}

        try:
            with smtplib.SMTP(connection['smtp_server'], connection['smtp_port']) as server:
                try:
                    server.starttls()
                except Exception as e:
                    # If TLS doesn't start, just keep going.
                    pass

                try:
                    server.login(connection['email_address'], connection['email_password'])
                except smtplib.SMTPAuthenticationError:
                    return {"error_code": "9010", "error_msg": "Authentication failed, check email and password.", "data": {}}
                try:
                    server.send_message(message)
                except smtplib.SMTPException:
                    return {"error_code": "9010", "error_msg": "Failed to send the messge.", "data": {}}
                server.quit()
            # Rest of the code
        except smtplib.SMTPConnectError:
            return {"error_code": "9011", "error_msg": "Error: Could not connect to the SMTP server.", "data": {}}
        except Exception as e:
            return {"error_code": "9011", "error_msg": "An unexpected error occurred." + str(e), "data": {}}
