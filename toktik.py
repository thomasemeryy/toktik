import json
from datetime import datetime


class InvalidDataFile(Exception):
    pass


class TokTik:
    def __init__(self, user_data_file):
        self.user_data = self._load_valid_json(user_data_file)

    def _load_valid_json(self, data_file):
        try:
            if isinstance(data_file, str):
                with open(data_file, "r", encoding="utf-8") as file:
                    file_data = file.read()
            elif hasattr(data_file, "read"):
                file_data = data_file.read()
            else:
                raise InvalidDataFile("Invalid argument provided")

            if len(file_data) != 0:
                user_data = json.loads(file_data)
                return user_data

            else:
                raise InvalidDataFile("File is empty")
        except FileNotFoundError as e:
            raise InvalidDataFile(f"Invalid file path ('{data_file}')") from e
        except json.JSONDecodeError as e:
            raise InvalidDataFile("Invalid file type (must be JSON)") from e

    def username(self):
        try:
            profile_map = (
                self.user_data.get("Profile")
                .get("Profile Information")
                .get("ProfileMap")
            )

            username = profile_map.get("userName")

            return username

        except AttributeError:
            raise InvalidDataFile("Data file is missing data or has corrupted")

    def launches(self):
        try:
            login_history = (
                self.user_data.get("Activity")
                .get("Login History")
                .get("LoginHistoryList")
            )

            launch_count = len(login_history)

            first_login_date = datetime.strptime(
                login_history[0]["Date"], "%Y-%m-%d %H:%M:%S %Z"
            )
            last_login_date = datetime.strptime(
                login_history[-1]["Date"], "%Y-%m-%d %H:%M:%S %Z"
            )

            # Calculate the difference in days
            time_difference = last_login_date - first_login_date
            days_difference = abs(time_difference.days)

            return {"count": launch_count, "days": days_difference}

        except AttributeError:
            raise InvalidDataFile("Data file is missing data or has corrupted")

    def videos(self):
        try:
            video_list = (
                self.user_data.get("Activity")
                .get("Video Browsing History")
                .get("VideoList")
            )

            watch_count = len(video_list)

            first_video_date = datetime.strptime(
                video_list[0]["Date"], "%Y-%m-%d %H:%M:%S"
            )
            last_video_date = datetime.strptime(
                video_list[-1]["Date"], "%Y-%m-%d %H:%M:%S"
            )

            time_difference = last_video_date - first_video_date
            days_difference = abs(time_difference.days)

            return {"count": watch_count, "days": days_difference}

        except AttributeError:
            raise InvalidDataFile("Data file is missing data or has corrupted")

    def favorites(self):
        try:
            activity = self.user_data.get("Activity")

            videos = activity.get("Favorite Videos").get("FavoriteVideoList")
            sounds = activity.get("Favorite Sounds").get("FavoriteSoundList")
            effects = activity.get("Favorite Effects").get("FavoriteEffectsList", {})
            hashtags = activity.get("Favorite Hashtags").get("FavoriteHashtagList", {})

            return {
                "videos": len(videos) if videos is not None else 0,
                "sounds": len(sounds) if sounds is not None else 0,
                "effects": len(effects) if effects is not None else 0,
                "hashtags": len(hashtags) if hashtags is not None else 0,
            }

        except AttributeError:
            raise InvalidDataFile("Data file is missing data or has corrupted")

    def likes(self):
        try:
            likes = (
                self.user_data.get("Activity").get("Like List").get("ItemFavoriteList")
            )

            like_count = len(likes)

            first_like_date = datetime.strptime(likes[0]["Date"], "%Y-%m-%d %H:%M:%S")
            last_like_date = datetime.strptime(likes[-1]["Date"], "%Y-%m-%d %H:%M:%S")

            # Calculate the difference in days
            time_difference = last_like_date - first_like_date
            days_difference = abs(time_difference.days)

            return {"count": like_count, "days": days_difference}

        except AttributeError:
            raise InvalidDataFile("Data file is missing data or has corrupted")

    def searches(self):
        try:
            searches = (
                self.user_data.get("Activity").get("Search History").get("SearchList")
            )

            return len(searches)

        except AttributeError:
            raise InvalidDataFile("Data file is missing data or has corrupted")

    def comments(self):
        try:
            comments = self.user_data.get("Comment").get("Comments").get("CommentsList")

            return len(comments)

        except AttributeError:
            raise InvalidDataFile("Data file is missing data or has corrupted")

    def shares(self):
        try:
            shares = (
                self.user_data.get("Activity")
                .get("Share History")
                .get("ShareHistoryList")
            )

            return len(shares)

        except AttributeError:
            raise InvalidDataFile("Data file is missing data or has corrupted")

    def direct_messages(self):
        try:
            direct_messages = (
                self.user_data.get("Direct Messages")
                .get("Chat History")
                .get("ChatHistory")
            )

            dm_list = {}

            for dm in direct_messages:
                name = dm.removeprefix("Chat History with ").removesuffix(":")
                count = len(direct_messages.get(dm))

                dm_list[name] = count

            return dm_list

        except AttributeError:
            raise InvalidDataFile("Data file is missing data or has corrupted")

    def lives(self):
        try:
            live_map = (
                self.user_data.get("Tiktok Live")
                .get("Watch Live History")
                .get("WatchLiveMap")
            )

            comments_count = 0

            for id in live_map:
                live = live_map.get(id)

                comments_list = live.get("Comments")

                if comments_list:
                    comments_count += len(comments_list)

            return {"count": len(live_map), "comments": comments_count}

        except AttributeError:
            raise InvalidDataFile("Data file is missing data or has corrupted")

    def followers(self):
        try:
            followers = (
                self.user_data.get("Activity").get("Follower List").get("FansList")
            )

            return len(followers)

        except AttributeError:
            raise InvalidDataFile("Data file is missing data or has corrupted")

    def following(self):
        try:
            following = (
                self.user_data.get("Activity").get("Following List").get("Following")
            )

            return len(following)

        except AttributeError:
            raise InvalidDataFile("Data file is missing data or has corrupted")


def generate_stats_file(data_file):
    try:
        tiktok_user = TokTik(data_file)

        username = tiktok_user.username()
        launches = tiktok_user.launches()
        videos = tiktok_user.videos()
        favorites = tiktok_user.favorites()
        likes = tiktok_user.likes()
        searches = tiktok_user.searches()
        comments = tiktok_user.comments()
        shares = tiktok_user.shares()
        direct_messages = tiktok_user.direct_messages()
        lives = tiktok_user.lives()
        followers = tiktok_user.followers()
        following = tiktok_user.following()

        formatted_dm_string = ""

        for name, count in direct_messages.items():
            formatted_dm_string += (
                f"Chat with {name}: {count} message{'s' if count != 1 else ''}\n"
            )

        lines = [
            f"{'-' * 10} TikTok User Statistics ({username}) {'-' * 10}\n",
            "A simple program to calculate statistics from a TikTok data export.\n",
            "✅ File read successfully.\n\n",
            f"{'-' * 10} 🔑 LAUNCHES {'-' * 10}",
            f"In the past {launches['days']} day{'s' if launches['days'] != 1 else ''},"
            f" you've launched TikTok {launches['count']} "
            f"time{'s' if launches['count'] != 1 else ''}.",
            f"- Thats an average of {round(launches['count'] / launches['days'])}"
            " launches a day.\n",
            f"{'-' * 10} 👀 VIDEOS WATCHED {'-' * 10}",
            f"In the last {videos['days']} "
            f"day{'s' if videos['days'] != 1 else ''}, you've "
            f"watched {videos['count']} video{'s' if videos['count'] != 1 else ''}.",
            "- Thats an average of "
            f"{round(videos['count'] / videos['days'])} videos a day.\n",
            f"{'-' * 10} 💖 LIKES {'-' * 10}",
            f"You've liked {likes['count']} video{'s' if likes['count'] != 1 else ''} "
            f"in the last {likes['days']} day{'s' if likes['days'] != 1 else ''}.",
            f"- Thats an average of {round(likes['count'] / likes['days'])}"
            " likes a day.",
            f"- You like {round(likes['count'] / videos['count'] * 100)}% of all the"
            " videos you watch.\n",
            f"{'-' * 10} 💬 COMMENTS {'-' * 10}",
            f"You've commented {comments} time{'s' if comments != 1 else ''}.\n",
            f"{'-' * 10} ⭐ FAVORITES {'-' * 10}",
            f"{favorites['videos']} favorite"
            f" video{'s' if favorites['videos'] != 1 else ''}.",
            f"{favorites['sounds']} favorite "
            f"sound{'s' if favorites['sounds'] != 1 else ''}.",
            f"{favorites['effects']} favorite "
            f"effect{'s' if favorites['effects'] != 1 else ''}.",
            f"{favorites['hashtags']} favorite "
            f"hashtag{'s' if favorites['hashtags'] != 1 else ''}.\n",
            f"{'-' * 10} 🎁 SHARES {'-' * 10}",
            f"You have shared {shares} video{'s' if shares != 1 else ''}.\n",
            f"{'-' * 10} 🔴 LIVES {'-' * 10}",
            f"You have joined {lives['count']}"
            f" live{'s' if lives['count'] != 1 else ''}.",
            f"- And commented a total of {lives['comments']} times.\n",
            f"{'-' * 10} 🔎 SEARCHES {'-' * 10}",
            f"You have searched {searches} time{'s' if searches != 1 else ''}.\n",
            f"{'-' * 10} 🗣️ DIRECT MESSAGES {'-' * 10}",
            f"{formatted_dm_string}",
            f"Total messages: {sum(direct_messages.values())}\n",
            f"{'-' * 10} 👥 FOLLOWS {'-' * 10}",
            f"You follow {following} {'people' if following != 1 else 'person'}.\n",
            f"{followers} {'people' if followers != 1 else 'person'} "
            f"follow{'' if followers != 1 else 's'} your account.",
        ]

        with open(f"{username}-stats.txt", "w", encoding="utf-8") as file:
            for line in lines:
                file.write(line + "\n")

        print("✅ Successfully generated stats file.")

        return f"{username}-stats.txt"

    except InvalidDataFile:
        lines = [
            f"{'-' * 10} TikTok User Statistics {'-' * 10}\n",
            "A simple program to calculate statistics from a TikTok data export.\n",
            "❌ Error reading user data file.",
        ]

        with open("error-stats.txt", "w", encoding="utf-8") as file:
            for line in lines:
                file.write(line + "\n")

        print("❌ Failure generating TikTok stats.")

        return "unknown-stats.txt"
