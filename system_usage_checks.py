import subprocess, smtplib, socket
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


def check_cpu():
    hyperthreading_enabled = False

    with open('/proc/cpuinfo', 'r') as f:
        if 'ht' in f.read():
            hyperthreading_enabled = True

        f.seek(0)
        num_of_processors = sum('processor' in line for line in cpuinfo) * 2

    if hyperthreading_enabled:
        cpu_usage_limit = num_of_processors / 4
    else:
        cpu_usage_limit = num_of_processors / 2

    cpu_usage = subprocess.check_output('uptime').split()[11]

    if cpu_usage > cpu_usage_limit:
        send_email_notification('CRITICAL - {} CPU usage'.format(socket.gethostname()), 'CPU usage in {} has exceeded '
            'limit {} with a value of {}.'.format(socket.gethostname, cpu_usage_limit, cpu_usage))


def check_memory():
    with open('/proc/meminfo', 'r') as f:
        mem_availability_limit = 80
        meminfo = f.readlines()
        memtotal = meminfo[0].split()[1]
        memavailable = meminfo[2].split()[1]
        memavailability_percent = float(memavailable)/int(memtotal)*100

        if memavailability_percent < mem_availability_limit:
            send_email_notification('CRITICAL - {} memory availability'.format(socket.gethostname()),
                                ' Memory availability '
                'in {} has dropped below limit {}%% with a value of {}%%.'.format(socket.gethostname,
                mem_availability_limit, cpu_usage))


def check_disk():
    disk_limit = 80
    disk_usage = int(subprocess.check_output(['df', '-h']).splitlines()[2].split()[4].rstrip('%'))

    if disk_usage > disk_limit:
        send_email_notification('CRITICAL - {} memory availability'.format(socket.gethostname()), ' Disk usage in {} '
                                                                                                 'has '
            'exceeded limit {}%% with a value of {}%%'.format(socket.gethostname, disk_limit, disk_usage))


def send_email_notification(subject, body):
    fromaddr = 'anastas_zoch@yahoo.gr'
    toaddrs = ['anastas_zoch@yahoo.gr', 'geogour@gmail.com']
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = ','.join(toaddrs)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    try:
        server = smtplib.SMTP('smtp.mail.yahoo.com', 587)
        server.starttls()
        server.login(fromaddr, passwd)
        for toaddr in toaddrs:
            server.sendmail(fromaddr, toaddr, msg.as_string())
    except smtplib.SMTPException:
        print "Message could not be sent."
    finally:
        server.quit()



if __name__ == '__main__':
    check_cpu()
    check_memory()
    check_disk()