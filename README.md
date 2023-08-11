
# TokTik

A simple program to calculate statistics from a TikTok data export.


## Features

- Calculates TikTok usage statistics from a data export.
    - Username
    - App Launches
    - Video Watch Count
    - Favorite Counts
        - Videos
        - Sounds
        - Effects
        - Hashtags
    - Like Count
    - Search Count
    - Comment Count
    - Direct Messages
        - Count per person
        - Total Counts
    - Lives
        - Joined
        - Comment Count
    - Follower Count
    - Following Count
- Outputs formatted statistics to a text file.
- Flexible and robust design.
## FAQ

#### How do you get a TikTok data export?

You can obtain your TikTok data export by going to the app, going to your profile, clicking the hamburger icon (☰), clicking **Settings and Privacy** -> **Account** -> **Download your data** and then selecting **`JSON`** as the file format. Wait a couple days for the data to be processed and then download it from the same location within the app.

#### Can I do this for multiple people?

Yes, you can instantiate multiple objects with different data files and perform analysis on each of them.

#### Does this store any sensitive data?

No, this program is run client-side and stores no data. For confirmation, the code is made open source and readily available to view.


#### What does a **`InvalidDataFile`** error mean?

An `InvalidDataFile` exception is thrown for many reasons, including: an invalid argument provided, an empty file, an invalid file path, an invalid file type or a file that is missing data. Ensure that you fix the following issues before running the code again. 


## Usage

```py
from toktik import TokTik

user = TokTik("user_data.json")

comments = user.comments()
username = user.username()
videos = user.videos()
likes = user.likes()

print(f"{username} has commented {comments} times.")
print(f"{username} watched {videos['count']} videos in the last {videos['days']} days.")
print(f"Thats an average of {round(videos['count'] / videos['days'])} videos a day.")

print(f"You like {round(likes['count'] / videos['count'] * 100)}% of the videos you watch.")
```
## Example

`main.py`

```py
from toktik import InvalidDataFile, generate_stats_file

file_path = input("JSON File: ").strip()

try:
    stats_file = generate_stats_file(file_path)
except InvalidDataFile:
    print("The provided file was not valid.")
```

`username-stats.txt`

```
---------- TikTok User Statistics (username) ----------

A simple program to calculate statistics from a TikTok data export.

✅ File read successfully.


---------- 🔑 LAUNCHES ----------
In the past 180 days, you've launched TikTok 8020 times.
- Thats an average of 45 launches a day.

---------- 👀 VIDEOS WATCHED ----------
In the last 180 days, you've watched 66824 videos.
- Thats an average of 371 videos a day.

---------- 💖 LIKES ----------
You've liked 8000 videos in the last 44 days.
- Thats an average of 182 likes a day.
- You like 12% of all the videos you watch.

---------- 💬 COMMENTS ----------
You've commented 345 times.

---------- ⭐ FAVORITES ----------
167 favorite videos.
17 favorite sounds.
5 favorite effects.
1 favorite hashtag.

---------- 🎁 SHARES ----------
You have shared 382 videos.

---------- 🔴 LIVES ----------
You have joined 89 lives.
- And commented a total of 28 times.

---------- 🔎 SEARCHES ----------
You have searched 472 times.

---------- 🗣️ DIRECT MESSAGES ----------
Chat with person_one: 5637 messages
Chat with person_two: 2266 messages
Chat with person_three: 46 messages

Total messages: 7949

---------- 👥 FOLLOWS ----------
You follow 37 people.

1 person follows your account.

```
## License

```MIT License

Copyright (c) 2023

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```


## Roadmap

- Add data to each function
    - Contents of messages, comments
    - Videos watched / likes
    - List of favorites
    - App launch times
    - Search queries
    - Followers / following
- Perform analysis on data
    - Watch time
    - Average time per session
    - Most active time / day
