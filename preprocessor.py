import re
import pandas as pd

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # Function to convert two-digit year to four-digit year
    def convert_year(date_str):
        date_parts = date_str.split('/')
        if len(date_parts[2].split(',')[0]) == 2:  # If year is in two-digit format
            date_parts[2] = '20' + date_parts[2]
        return '/'.join(date_parts)

    # Apply the function to the dates list
    dates = [convert_year(date) for date in dates]

    # Print dates for debugging
    for date in dates:
        print(f"Converted date: {date}")

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Convert message_date type
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %H:%M - ')

    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df

# Example usage
# data = """26/06/24, 16:54 - Messages and calls are end-to-end encrypted. No one outside of this chat, not even WhatsApp, can read or listen to them. Tap to learn more.
# 26/06/24, 16:54 - Aryan Nathani created group "Placement_prep"
# 26/06/24, 16:54 - Aryan Nathani added you
# 26/06/24, 16:55 - Aryan Nathani: Hello guyss , since placement is gonna start from next week , i have created this group where we  can ask our queries and help each other.
# 26/06/24, 16:56 - Saad Shaikh: Niceeeee"""

# df = preprocess(data)
# print(df)