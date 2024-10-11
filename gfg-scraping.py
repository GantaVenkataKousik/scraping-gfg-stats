import csv
import requests
from bs4 import BeautifulSoup


cols = ["user Name", "Institute Rank", "Institution Name", "User Streak", "Global Streak", "Languages Used"]

cols.extend(["Overall Coding Score","Total Problem Solved","Monthly Coding Score"])

cols.extend(["Problems Solved","school","basic","easy","medium","hard"])

csv_file = 'GFG_stats.csv'
with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)
            
    writer.writerow(cols)

    # URL of the website to scrape
    usernames = [
        'gantavenkatakousik2021',
        'rohithkumar45',
        'lakshman511',
        'maheshcheegiti2021',
        '18pa1a05f1',
        'dineshkumar2021',
        'abdulkareem1704',
        '19pa1a04h2',
        'p_varma17'
    ]

    for username in usernames:
        
        url = f"https://auth.geeksforgeeks.org/user/{username}"
        response = requests.get(url)
        
        if response is None or response.status_code != 200:
            print("error.....")
            continue
        else:
            print(f"Scraped : {username} Data")
        user = BeautifulSoup(response.content, 'html.parser')

        # Extracting various details
        profile_pic_src = user.find(class_='profile_pic')['src']


        institute_rank =  user.find(class_='profile_details_section activity-container-1 section_card').find(class_='profile_rank_div tooltipped').find(class_='rankNum').text

        institution = user.find(class_='col l4 m4 s12')
        inst_name = institution.find(class_='basic_details_data').text.strip()

        streak_info = user.find(class_='streakCnt tooltipped').get_text(strip=True).split('/')
        user_streak = streak_info[0].strip()
        global_streak = streak_info[1].strip()

        score_cards = user.find(class_='row score_cards_container').findAll(class_='col xl3 l6 m6 s12')
        scores = {sc.find(class_='score_card_name').text.strip(): sc.find(class_='score_card_value').text.strip() for sc in score_cards}

        languages_used = user.findAll(class_='col l4 m4 s12')[1].find(class_='basic_details_data').text.strip()

        # Extracting the number of problems solved per difficulty level
        problems_solved = {}
        no_solved = user.find(class_='col xl8 l8 m8 s8 typeLangSection').findAll(class_='tab')
        for item in no_solved:
            difficulty, count = item.text.split(' ')
            problems_solved[difficulty] = int(count[1:-1])  # Removing parentheses and converting count to integer

        # Extracting the list of solved problems
        problem_sections = user.find(class_='col xl8 l8 m8 s8 typeLangSection').find(class_='problem_list_section').findAll(class_='row')
        difficulty_levels = ["SCHOOL", "BASIC", "EASY", "MEDIUM", "HARD"]
        problems = {difficulty: [] for difficulty in difficulty_levels}
        data = []
        

         
        data.extend([username, institute_rank, inst_name, user_streak, global_streak, languages_used])
        
        for key, value in scores.items():
                data.append(value)

        # Writing data to CSV
        for difficulty, count in problems_solved.items():
            data.append(count)
        writer.writerow(data)
        print(data)

print("Data written to", csv_file)
