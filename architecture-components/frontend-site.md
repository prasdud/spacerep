# High Level Architecture for Frontend

## Overview
The frontend is a simple, interactive React application designed to capture user study topics and their learning priorities. The app focuses on minimalism and ease of use, providing a streamlined interface for users to log what they want to learn and how important it is.

## Key Features
- **Topic Input:** A text box where users enter the topic they are studying.
- **Importance/Priority Input:** An input (dropdown, slider, or numeric field) for users to specify how important or urgent the topic is.
- **Timestamp Capture:** The app automatically records the current time when a new topic is entered, marking the start of the learning session.

## Component Structure

```
App
 ├── TopicEntryForm
 │    ├── TopicInput (text box)
 │    ├── ImportanceInput (dropdown/slider)
 │    └── SubmitButton
 └── (Optional) TopicList (shows entered topics)
```

## Data Flow

1. **User Interaction:** User enters a topic and selects importance.
2. **Form Submission:** On submit, the app captures:
    - Topic name
    - Importance/priority value
    - Current timestamp (auto-generated)
3. **State Management:** The app stores the entry in local state (or optionally sends it to a backend API).
4. **Feedback:** Optionally, the app can display a list of entered topics.

## Technologies

- **React** (with hooks for state management)
- **CSS/Styled Components** for styling
- **(Optional) Axios/Fetch** for API calls if backend integration is needed

## Example UI Sketch

```
+--------------------------------------+
| What are you studying?  [__________] |
| Importance:        [Low |---| High]  |
| [ Add Topic ]                        |
+--------------------------------------+
| (Optional: List of entered topics)   |
+--------------------------------------+
```

## Extensibility

- Can be extended to support authentication, topic editing, or integration with spaced repetition algorithms.
- Designed for easy backend integration if needed.


## Other Notes / Ideas / Future features
- maybe we have like bubbles on screen under somewhere that has popular topics, maybe we check already if user is learning specific topics so we dont show them those. Incidentally we can do a recommendation system

---
