import logging
import re
import paramiko
from telegram import Update, ForceReply, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
import psycopg2
import os


TOKEN = os.environ.get("BOT_TOKEN", "7000000000:AACFGBABOBABOABOBAOBOBABOB-ABOB")

ssh_host = os.environ.get('RM_HOST', "postgres_master")
ssh_port = os.environ.get("RM_PORT", 22)
ssh_user = os.environ.get("RM_USER", "ryan")
ssh_password = os.environ.get("RM_PASSWORD", "123")

db_host = os.environ.get("DB_HOST", "postgres_master")
db_port = os.environ.get("DB_PORT", 5432)
db_user = os.environ.get("DB_USER", "postgres")
db_password = os.environ.get("DB_PASSWORD", "postgres")
db_database = os.environ.get("DB_DATABASE", "tg_bot")

postgresql_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}"

logging.basicConfig(filename='logfile.txt',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def execute_command(command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ssh_host, username=ssh_user,
                password=ssh_password, port=int(ssh_port))

    stdin, stdout, stderr = ssh.exec_command(command)
    result = stdout.read().decode()
    if not result:
        result = stderr.read().decode()

    ssh.close()

    return result

def execute_sql_command(sql):
    conn = psycopg2.connect(postgresql_url)
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.close()
    return result


def insert_into_db(command):
    conn = psycopg2.connect(postgresql_url)
    cursor = conn.cursor()
    cursor.execute(command)
    conn.commit()
    conn.close()



def reply_long_sql_messages(update, result):
    if not result:
        update.message.reply_text("No data found.")
        return
    message = ""
    if isinstance(result, list):
        for row in result:
            for i, item in enumerate(row):
                message += str(item)
                if i != len(row) - 1:
                    message += " | "
            message += "\n"
            
    if len(message) > 4096:
        for x in range(0, len(message), 4096):
            update.message.reply_text(message[x:x+4096])
    else:
        update.message.reply_text(message)


def reply_long_messages(update, result):
    if len(result) > 4096:
        for x in range(0, len(result), 4096):
            update.message.reply_text(result[x:x+4096])
    else:
        update.message.reply_text(result)


def get_release_info(update, _):
    result = execute_command('lsb_release -a')
    reply_long_messages(update, result)


def get_system_info(update, _):
    result = execute_command('uname -a')
    reply_long_messages(update, result)


def get_uptime_info(update, _):
    result = execute_command('uptime')
    reply_long_messages(update, result)


def get_disk_usage(update, _):
    result = execute_command('df -h')
    reply_long_messages(update, result)


def get_memory_usage(update, _):
    result = execute_command('free -h')
    reply_long_messages(update, result)


def get_cpu_stats(update, _):
    result = execute_command('mpstat')
    reply_long_messages(update, result)


def get_logged_in_users(update, _):
    result = execute_command('w')
    reply_long_messages(update, result)


def get_authentication_logs(update, _):
    result = execute_command('last -n 10')
    reply_long_messages(update, result)


def get_critical_logs(update, _):
    result = execute_command('journalctl -p 2 -b -n 5')
    reply_long_messages(update, result)


def get_process_info(update, _):
    result = execute_command('ps aux')
    reply_long_messages(update, result)


def get_network_connections(update, _):
    result = execute_command('ss -tulwn')
    reply_long_messages(update, result)


def get_installed_packages(update, _):
    result = execute_command('apt list --installed')
    reply_long_messages(update, result)


def get_services(update, _):
    result = execute_command('systemctl list-units --type=service')
    reply_long_messages(update, result)


def find_email_addresses(update: Update, _):
    update.message.reply_text('Please send me the text to search for email addresses:',
                              reply_markup=ForceReply(selective=True))
    return 'process_email'


def process_email_addresses(update: Update, context: CallbackContext):
    text = update.message.text
    emails = re.findall(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    if emails:
        update.message.reply_text('\n'.join(emails))
        
        reply_keyboard = [['Yes', 'No']]
        update.message.reply_text("Email addresses found. Do you want to save the email addresses to the database?",
                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                                                   one_time_keyboard=True))
        
        requests = [f"INSERT INTO emails (email) VALUES ('{email}');" for email in emails]
        if context.user_data is None:
            context.user_data = {}
        context.user_data['requests'] = requests
        
        return 'save_to_db'
    else:
        update.message.reply_text('No email addresses found.')
        return ConversationHandler.END


def find_phone_numbers(update: Update, _):
    update.message.reply_text('Please send me the text to search for phone numbers:',
                              reply_markup=ForceReply(selective=True))
    return 'process_phone'


def process_phone_numbers(update: Update, context: CallbackContext):
    text = update.message.text
    phone_numbers = re.findall(
        r'\+7[-\s]?\(?\d{3}\)?[-\s]?\d{3}[-\s]?\d{2}[-\s]?\d{2}|8[-\s]?\(?\d{3}\)?[-\s]?\d{3}[-\s]?\d{2}[-\s]?\d{2}', text)
    if phone_numbers:
        update.message.reply_text('\n'.join(phone_numbers))
        reply_keyboard = [['Yes', 'No']]
        update.message.reply_text("Phone numbers found. Do you want to save the phone numbers to the database?", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        requests = [f"INSERT INTO numbers (number) VALUES ('{phone_number}');" for phone_number in phone_numbers]
        if context.user_data is None:
            context.user_data = {}
        context.user_data['requests'] = requests
        return "save_to_db"
    else:
        update.message.reply_text('No phone numbers found.')
        return ConversationHandler.END

def save_to_db(update: Update, context: CallbackContext):
    user_response = update.message.text

    if user_response == "Yes":
        for request in context.user_data['requests']:
            try:
                insert_into_db(request)
            except Exception as e:
                logger.error("Error adding to DB: %s", e)
                update.message.reply_text("An error occurred while adding to the database. Please try again later…")
                return ConversationHandler.END
        
        update.message.reply_text("Data successfully saved to the database.")
    else:
        update.message.reply_text("Data was not saved to the database.")
    
    return ConversationHandler.END


def verify_password(update: Update, _):
    update.message.reply_text('Enter the password to check:')
    return 'process_password'


def process_password(update: Update, _):
    text = update.message.text
    password_regex = r'^(?=.*[A-Z])(?=.*[!@#$%^&*()])(?=.*[0-9])(?=.*[a-z]).{8,}$'
    if re.match(password_regex, text):
        update.message.reply_text('The password is strong.')
    else:
        update.message.reply_text('The password is weak.')
    return ConversationHandler.END

def get_repl_logs(update: Update, _):
    result = execute_command('cat /var/log/postgresql/postgresql-14-main.log | grep repl')
    reply_long_messages(update, result)
    return ConversationHandler.END

def get_numbers(update: Update, _):
    result = execute_sql_command("SELECT * FROM numbers;")
    reply_long_sql_messages(update, result)
    return ConversationHandler.END

def get_emails(update: Update, _):
    result = execute_sql_command("SELECT * FROM emails;")
    reply_long_sql_messages(update, result)
    return ConversationHandler.END



def cancel(update: Update, _):
    update.message.reply_text(
        'Dialog canceled.', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('find_email', find_email_addresses),
                      CommandHandler('find_phone_number', find_phone_numbers),
                      CommandHandler('verify_password',
                                     verify_password),
                      CommandHandler('get_release', get_release_info),
                      CommandHandler('get_system_info', get_system_info),
                      CommandHandler('get_uptime_info', get_uptime_info),
                      CommandHandler('get_disk_usage', get_disk_usage),
                      CommandHandler('get_memory_usage', get_memory_usage),
                      CommandHandler('get_cpu_stats', get_cpu_stats),
                      CommandHandler('get_logged_in_users', get_logged_in_users),
                      CommandHandler('get_authentication_logs', get_authentication_logs),
                      CommandHandler('get_critical_logs', get_critical_logs),
                      CommandHandler('get_process_info', get_process_info),
                      CommandHandler('get_network_connections', get_network_connections),
                      CommandHandler('get_installed_packages', get_installed_packages),
                      CommandHandler('get_services', get_services),
                      CommandHandler('get_repl_logs', get_repl_logs),
                      CommandHandler('get_numbers', get_numbers),
                      CommandHandler('get_emails', get_emails)],
        
        states={
            'process_email': [MessageHandler(Filters.text & ~Filters.command,
                                             process_email_addresses)],
            'process_phone': [MessageHandler(Filters.text & ~Filters.command,
                                             process_phone_numbers)],
            'process_password': [MessageHandler(Filters.text & ~Filters.command,
                                                process_password)],
            'save_to_db': [MessageHandler(Filters.regex('^(Yes|No)$'),
                                          save_to_db)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    updater.dispatcher.add_handler(conv_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
