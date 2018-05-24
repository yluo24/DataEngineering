import sys
import datetime

def getInactivityPeriod(path):
    with open(path, 'r') as reader:
        period = int(reader.readline().strip())
    
    if period <= 0:
        print("Inactivity period is invalid.\n")
        exit(2)
    else:
        return period

def getLogs(path):
    with open(path, 'r') as log_reader:
        headline = log_reader.readline()
        logs = log_reader.readlines()
    
    return logs

def getSessionWriter(path):
    try:
        writer = open(output_path, 'a')
    except:
        print('Output path is invalid')
        exit(3)
    
    return writer

def divideSession(input_period_path, input_log_path, output_path):
    inactivity_period = getInactivityPeriod(input_period_path)
    logs = getLogs(input_log_path)
    session_writer = getSessionWriter(output_path)

    user_list = []  # List of active users/ips basedthat have requested for document.
    user_updated_list = []  # List of active users/ips ordered by last request time.
    request_dict = {}  # Dictionary of users/ips and their relevant information.

    currentTime = '1970-01-01 00:00:00'
    timestamp = datetime.datetime.strptime(currentTime, '%Y-%m-%d %H:%M:%S')
    
    for log in logs:
        log = log.strip().split(',')
        if len(log) == 0:
            continue
        ip = log[0].strip()
        date = log[1].strip()
        time = log[2].strip()
        cik = log[4].strip()
        accession = log[5].strip()
        extention = log[6].strip()
        webpage = cik + accession + extention

        requestTime = date + ' ' + time
        if requestTime != currentTime:  # If a new time shows up, check if any session is expired
            timestamp = datetime.datetime.strptime(requestTime, '%Y-%m-%d %H:%M:%S')
            currentTime = requestTime

            while user_updated_list:
                # Check from the start of user_updated_list. If the first user of list is active then break
                user = user_updated_list[0]

                if (timestamp - request_dict[user]['lastTime']).total_seconds() > inactivity_period:
                    # If a session is expired, delete all relevant record of this session.
                    values = request_dict.pop(user)
                    user_updated_list.remove(user)
                    user_list.remove(user)

                    start = datetime.datetime.strftime(values['startTime'], '%Y-%m-%d %H:%M:%S')
                    end = datetime.datetime.strftime(values['lastTime'], '%Y-%m-%d %H:%M:%S')
                    session_writer.write('%s,%s,%s,%d,%d\n' % (user, start, end, int((values['lastTime'] - values['startTime']).total_seconds()) + 1, values['pageCount']))
                
                else:
                    break  # All the users in user_updated_list are active so far
        
        if ip not in user_list:  # If user starts a new session, initialize all related record of this session
            user_list.append(ip)
            request_dict[ip] = {'startTime':timestamp, 'lastTime':timestamp, 'pageCount':1}
            user_updated_list.append(ip)

        else:                    # If user is active, update all related record of current session
            request_dict[ip]['lastTime'] = timestamp
            request_dict[ip]['pageCount'] += 1
            user_updated_list.remove(ip)  # Change user's order in user_updated_list by remove and append
            user_updated_list.append(ip)
        
    while len(user_list) > 0:  # When there is no more new requests, identify all the rest sessions
        user = user_list.pop(0)
        values = request_dict.pop(user)

        start = datetime.datetime.strftime(values['startTime'], '%Y-%m-%d %H:%M:%S')
        end = datetime.datetime.strftime(values['lastTime'], '%Y-%m-%d %H:%M:%S')
        session_writer.write('%s,%s,%s,%d,%d\n' % (user, start, end, int((values['lastTime'] - values['startTime']).total_seconds()) + 1, values['pageCount']))
    
        user_updated_list.remove(user)
    
    session_writer.close()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Please input the command correctly: python3 src/sessionization.py input/inactivity_period.txt input/log.csv output/sessionization.txt")
        exit(1)
    
    input_period_path = sys.argv[1]
    input_log_path = sys.argv[2]
    output_path = sys.argv[3]

    divideSession(input_period_path, input_log_path, output_path)
    
