# Data Engineering Challenge

## Package Dependency

pip install datetime

##  Explanation
1. Four Variables:
    * ***user_list*** - list, store all current active user and ordered by their first request time in the session
    * ***user_update_list*** - list, store all current active user and ordered by their last request time in the session
    * ***request_dict*** - dictionary/map, formatted as {ip:{firstTime:timestamp1, lastTime:timestamp2, pageCount:num}}
    * ***currentTime*** - string, timestamp of current log be processed

2. Go over every log and check the timestamp at first. If hitting a new timestamp, check ***user_update_list*** and see whether there is any session is expired according to time difference between ***currentTime*** and the last time that user requested document.
    * Check from the start of ***user_update_list***. The first user will be the person whose last request is from the longest time ago
    * Once the first user's last request time is within active period, then stop checking since all the rest users must also be active.
    * Remove all relevant record if a session is expired.

3. Process every log. If this is a new user, which means a new session, then add a record to ***user_list***, ***user_update_list*** and ***request_dict***. If this is not a new user, just update the records.

4. When it comes to the end of logs, put an end to all the existing sessions.
