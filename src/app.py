"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
        "category": "Games",
        "duration_per_session": 1.5,  # hours per session
        "attendance_records": {}  # Will store student attendance by date
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
        "category": "Academic",
        "duration_per_session": 1.0,  # hours per session
        "attendance_records": {}  # Will store student attendance by date
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"],
        "category": "Sports",
        "duration_per_session": 1.0,  # hours per session
        "attendance_records": {}  # Will store student attendance by date
    },
    "Soccer Team": {
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"],
        "category": "Sports",
        "duration_per_session": 1.5,  # hours per session
        "attendance_records": {}  # Will store student attendance by date
    },
    "Basketball Team": {
        "description": "Practice and play basketball with the school team",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"],
        "category": "Sports",
        "duration_per_session": 1.5,  # hours per session
        "attendance_records": {}  # Will store student attendance by date
    },
    "Art Club": {
        "description": "Explore your creativity through painting and drawing",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["amelia@mergington.edu", "harper@mergington.edu"],
        "category": "Arts",
        "duration_per_session": 1.5,  # hours per session
        "attendance_records": {}  # Will store student attendance by date
    },
    "Drama Club": {
        "description": "Act, direct, and produce plays and performances",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["ella@mergington.edu", "scarlett@mergington.edu"],
        "category": "Arts",
        "duration_per_session": 1.5,  # hours per session
        "attendance_records": {}  # Will store student attendance by date
    },
    "Math Club": {
        "description": "Solve challenging problems and participate in math competitions",
        "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
        "max_participants": 10,
        "participants": ["james@mergington.edu", "benjamin@mergington.edu"],
        "category": "Academic",
        "duration_per_session": 1.0,  # hours per session
        "attendance_records": {}  # Will store student attendance by date
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 12,
        "participants": ["charlotte@mergington.edu", "henry@mergington.edu"],
        "category": "Academic",
        "duration_per_session": 1.5,  # hours per session
        "attendance_records": {}  # Will store student attendance by date
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(
            status_code=400,
            detail="Student is already signed up"
        )

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is signed up
    if email not in activity["participants"]:
        raise HTTPException(
            status_code=400,
            detail="Student is not signed up for this activity"
        )

    # Remove student
    activity["participants"].remove(email)
    return {"message": f"Unregistered {email} from {activity_name}"}


@app.get("/activities/categories")
def get_categories():
    """Get all available activity categories"""
    categories = set()
    for activity in activities.values():
        categories.add(activity["category"])
    return sorted(list(categories))


@app.get("/activities/filter")
def filter_activities(category: str = None):
    """Filter activities by category"""
    if category is None or category == "All":
        return activities
    
    filtered_activities = {}
    for name, activity in activities.items():
        if activity["category"] == category:
            filtered_activities[name] = activity
    
    return filtered_activities


@app.post("/activities/{activity_name}/record-attendance")
def record_attendance(activity_name: str, email: str, date: str):
    """Record attendance for a student at an activity session"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is signed up
    if email not in activity["participants"]:
        raise HTTPException(
            status_code=400,
            detail="Student is not signed up for this activity"
        )
    
    # Initialize attendance records for this date if needed
    if date not in activity["attendance_records"]:
        activity["attendance_records"][date] = []
    
    # Check if student is already marked as attended
    if email in activity["attendance_records"][date]:
        raise HTTPException(
            status_code=400,
            detail="Student attendance already recorded for this date"
        )
    
    # Record attendance
    activity["attendance_records"][date].append(email)
    return {"message": f"Recorded attendance for {email} at {activity_name} on {date}"}


@app.get("/activities/{activity_name}/attendance")
def get_activity_attendance(activity_name: str, email: str = None):
    """Get attendance records for an activity or a specific student in an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    activity = activities[activity_name]
    
    if email:
        # Validate student is signed up
        if email not in activity["participants"]:
            raise HTTPException(
                status_code=400,
                detail="Student is not signed up for this activity"
            )
        
        # Get dates this student attended
        attended_dates = []
        for date, attendees in activity["attendance_records"].items():
            if email in attendees:
                attended_dates.append(date)
        
        # Calculate total hours
        total_hours = len(attended_dates) * activity["duration_per_session"]
        
        return {
            "student": email,
            "activity": activity_name,
            "attended_dates": attended_dates,
            "total_sessions": len(attended_dates),
            "total_hours": total_hours
        }
    
    # Return all attendance records for the activity
    return {
        "activity": activity_name,
        "attendance_records": activity["attendance_records"],
        "session_duration": activity["duration_per_session"]
    }


@app.get("/students/{email}/activity-report")
def get_student_activity_report(email: str):
    """Get a report of all activities and hours for a student (for college applications)"""
    student_activities = {}
    total_hours = 0
    
    for activity_name, activity in activities.items():
        if email in activity["participants"]:
            # Count attended sessions
            attended_sessions = 0
            for date, attendees in activity["attendance_records"].items():
                if email in attendees:
                    attended_sessions += 1
            
            hours = attended_sessions * activity["duration_per_session"]
            total_hours += hours
            
            student_activities[activity_name] = {
                "category": activity["category"],
                "attended_sessions": attended_sessions,
                "hours": hours
            }
    
    return {
        "student": email,
        "activities": student_activities,
        "total_activities": len(student_activities),
        "total_hours": total_hours
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
