#!/usr/bin/python3

from zoopla import Zoopla
import configparser
import os
import smtplib
import email
import email.mime
import email.mime.text
import email.mime.multipart
import time
import sys

################################
###### HELPER FUNCTIONS ########
################################


def generateHtmlOutput(output_fields, search):
    output_string = ''

    output_string += '<h3> Search parameters: ' + str(search_params) + '</h3><br/><br/>'

    output_string += '<table border="1" style="width:100%"><tr align="center">'

    for field in output_fields:
        output_string += '<th>'+field.upper()+'</th>'

    output_string += '</tr>'

    for result in search:
        output_string += '<tr align="center">'
        for field in output_fields:
            if getattr(result, field, None) is not None:
                if field.endswith('url'):
                    output_string += '<td><a href="' + str(getattr(result, field)) + '">' + str(field) + '</a></td>'
                else:
                    output_string += '<td>' + str(getattr(result, field)) + '</td>'
        output_string += '</tr>'

    output_string += '</table>'

    return output_string


def sendZooplaScreenerViaEmail(area, data, email_address_recipient, email_address_username, pwd, server_name, port):

    # You must configure these smpt-server settings before using this script
    use_tsl = True  # For Gmail use True
    smpt_server_requires_authentication = True  # For Gmail use True
    smtp_username = email_address_username  # This is the smtp server username and also the sender name of the email.
    smtp_password = pwd
    smtp_server_name = server_name  # For Gmail use smtp.gmail.com
    smtp_server_port = port  # For Gmail use 587
    adesso = time.strftime("%c")  # what time is it now?

    # Example email message contents
    message_recipient = email_address_recipient
    message_title = area + ' - ZooplaScreener - ' + adesso
    message_text_list = data
    message_attachment_path = ''  # Set this to the full path of the file you want to attach to the mail or to ''
    # if you do not want to attach anything.

    # Compile the start of the email message.
    email_message_content = email.mime.multipart.MIMEMultipart('alternative')
    email_message_content['From'] = smtp_username
    email_message_content['To'] = ", ".join(message_recipient)
    email_message_content['Subject'] = message_title

    # Append the user given lines of text to the email message.
    email_message_content.attach(email.mime.text.MIMEText(message_text_list.encode('utf-8'), _charset='utf-8', _subtype='html'))

    # Read attachment file, encode it and append it to the email message.
    if message_attachment_path != '':  # If no attachment path is defined, do nothing.
        email_attachment_content = email.mime.base.MIMEBase('application', 'octet-stream')
        email_attachment_content.set_payload(open(message_attachment_path, 'rb').read())
        email.encoders.encode_base64(email_attachment_content)
        email_attachment_content.add_header('Content-Disposition',
                                            'attachment; filename="%s"' % os.path.basename(message_attachment_path))
        email_message_content.attach(email_attachment_content)

    # Email message is ready, before sending it, it must be compiled  into a long string of characters.
    email_message_content_string = email_message_content.as_string()

    # Start communication with the smtp-server.
    try:
        mailServer = smtplib.SMTP(smtp_server_name, smtp_server_port, 'localhost',
                                  15)  # Timeout is set to 15 seconds.
        mailServer.ehlo()

        # Check if message size is below the max limit the smpt server announced.
        message_size_is_within_limits = True  # Set the default that is used if smtp-server does not annouce max message size.
        if 'size' in mailServer.esmtp_features:
            server_max_message_size = int(
                mailServer.esmtp_features['size'])  # Get smtp server announced max message size
            message_size = len(email_message_content_string)  # Get our message size
            if message_size > server_max_message_size:  # Message is too large for the smtp server to accept, abort sending.
                message_size_is_within_limits = False
                print('Message_size (', str(message_size), ') is larger than the max supported size (',
                      str(server_max_message_size), ') of server:', smtp_server_name, 'Sending aborted.')
                sys.exit(1)
        if message_size_is_within_limits == True:
            # Uncomment the following line if you want to see printed out the final message that is sent to the smtp server
            # print('email_message_content_string =', email_message_content_string)
            if use_tsl == True:
                mailServer.starttls()
                mailServer.ehlo()  # After starting tls, ehlo must be done again.
            if smpt_server_requires_authentication == True:
                mailServer.login(smtp_username, smtp_password)
            mailServer.sendmail(smtp_username, message_recipient, email_message_content_string)
        mailServer.close()
        print("Email sent!")

    except smtplib.socket.timeout as reason_for_error:
        print('Error, Timeout error:', reason_for_error)
        sys.exit(1)
    except smtplib.socket.error as reason_for_error:
        print('Error, Socket error:', reason_for_error)
        sys.exit(1)
    except smtplib.SMTPRecipientsRefused as reason_for_error:
        print('Error, All recipients were refused:', reason_for_error)
        sys.exit(1)
    except smtplib.SMTPHeloError as reason_for_error:
        print('Error, The server didn’t reply properly to the HELO greeting:', reason_for_error)
        sys.exit(1)
    except smtplib.SMTPSenderRefused as reason_for_error:
        print('Error, The server didn’t accept the sender address:', reason_for_error)
        sys.exit(1)
    except smtplib.SMTPDataError as reason_for_error:
        print(
            'Error, The server replied with an unexpected error code or The SMTP server refused to accept the message data:',
            reason_for_error)
        sys.exit(1)
    except smtplib.SMTPException as reason_for_error:
        print(
            'Error, The server does not support the STARTTLS extension or No suitable authentication method was found:',
            reason_for_error)
        sys.exit(1)
    except smtplib.SMTPAuthenticationError as reason_for_error:
        print('Error, The server didn’t accept the username/password combination:', reason_for_error)
        sys.exit(1)
    except smtplib.SMTPConnectError as reason_for_error:
        print('Error, Error occurred during establishment of a connection with the server:', reason_for_error)
        sys.exit(1)
    except RuntimeError as reason_for_error:
        print('Error, SSL/TLS support is not available to your Python interpreter:', reason_for_error)
        sys.exit(1)


##############################
###### MAIN LOGIC ############
##############################

# Finds the path of the file
zoopla_bot_path = os.path.dirname(os.path.abspath(__file__))

# Reads the config file
#configFileName = 'zoopla_config.ini'

namesofconfigs = ["zoopla_config1.ini","zoopla_config2.ini","zoopla_config3.ini"]

for configFileName in namesofconfigs:
    config = configparser.ConfigParser()
    try:
        config.read(os.path.join(zoopla_bot_path, configFileName))
    except IOError:
        print('Config does not exist')
        sys.exit(1)

    api_key = config['api_data']['api_key']

    zoopla = Zoopla(api_key=api_key, debug=True, wait_on_rate_limit=True)

    search_params = {}

    for key in config['flat_data_str']:
        if config['flat_data_str'][key]:
            search_params[key] = config['flat_data_str'][key]

    for key in config['flat_data_num']:
        if config['flat_data_num'][key]:
            search_params[key] = int(config['flat_data_num'][key])

    try:
        search = zoopla.search_property_listings(params=search_params)
    except Exception:
        print("Something went wrong!")
        sys.exit(1)

    # Email Data
    recipient = config['email_data']['recipient'].replace(" ", "").split(',')
    sender = config['email_data']['sender']
    pwd_sender = config['email_data']['pwd_sender']
    server_name = config['email_data']['server_name']
    server_port = config['email_data']['server_port']

    # Set send to True if you want to use email module and send
    send = config['email_data']['send_email'].lower()

    output_fields = config['output']['output_fields'].lower().replace(" ", "").split(',')

    output_string = generateHtmlOutput(output_fields, search)

    area = search_params['area']

    if send == "true":
        print("\nSending....")
        sendZooplaScreenerViaEmail(area, output_string, recipient, sender, pwd_sender, server_name, server_port)  # send via email
    else:
        print("\nClosing module without sending....")

    time.sleep(5)
