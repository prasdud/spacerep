# SpaceRep

SpaceRep is a spaced repetition scheduling application designed to help learners retain information effectively by integrating revision reminders directly into their Google Calendar. Users enter the topics they are studying, and SpaceRep intelligently schedules spaced revision sessions, taking into account existing events to optimize learning without conflicts.

## Features

- **Easy Topic Entry:** Simple frontend input for users to add study topics.
- **Google Calendar Integration:** Automatically schedules spaced repetition reminders on the user's calendar.
- **Conflict-Aware Scheduling:** Considers existing calendar events to space out revision sessions optimally.
- **Progress & Feedback Tracking:** Users can mark sessions as "easy," "hard," or "need to relearn," allowing dynamic adjustment of future review intervals.
- **Missed & Rescheduled Session Handling:** Automatically adapts the revision schedule when users miss or reschedule sessions to maintain effective learning.
- **User Customization:** Supports preferred study times and flexible scheduling.
- **Secure & Private:** User data is handled with privacy and security in mind.

## Technology Stack

- **Backend:** FastAPI
- **Frontend:** Minimal and intuitive UI (framework agnostic)
- **Calendar API:** Google Calendar API for scheduling reminders

## How It Works

1. User enters a topic they are studying in the frontend.
2. Backend processes the topic and schedules the first revision session on Google Calendar.
3. Future revision sessions are spaced based on user feedback and calendar availability.
4. When the user completes or reschedules a session, the system adapts subsequent intervals accordingly.
5. Users receive notifications via their calendar to review topics on optimal days.

## Getting Started

### Prerequisites

- Python 3.8+
- Google Cloud account with Calendar API enabled
- Google OAuth credentials for API access

### Installation

- TBD