from meeting import Meeting
from exceptions import MeetingNotFoundError

import discord


class MeetingRegister:
    def __init__(self):
        self.meetings = []

    def create_meeting(self, *args, **kwargs):
        """Creates a meeting and adds the meeting to the list of meetings"""
        meeting = Meeting(*args, **kwargs)
        self.meetings.append(meeting)

    def get_meeting(self, user: discord.User):
        """Returns a meeting the user is a participant of"""
        for meeting in self.meetings:
            if user.id in map(lambda participant: participant.id, meeting.participants):
                return meeting
        return None

    def remove_meeting(self, meeting_name: str) -> None:
        """Removes meeting from the meeting_register"""
        for i, meeting in enumerate(self.meetings):
            if meeting.name == meeting_name:
                self.meetings.pop(i)
                return
        raise MeetingNotFoundError("Meeting not found...")

    def remove_user_from_meetings(self, user):
        """Removes all threads, topics and meetings initiated by the given user"""
        for meeting in self.meetings:
            if meeting.initiator.id == user.id:
                self.remove_meeting(meeting)
                meeting.end()
                continue

            for thread in meeting:
                if thread.initiator.id == user.id:
                    meeting.threads.remove(thread)