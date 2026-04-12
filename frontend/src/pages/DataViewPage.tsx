import { useState, useEffect } from "react";
import API from "../services/api";

interface Lecturer {
  id: number;
  name: string;
  unavailable_slots: string[];
}

interface Room {
  id: string;
  capacity: number;
}

interface Timeslot {
  id: string;
  day: string;
  time: string;
}

interface Course {
  id: number;
  name: string;
  lecturer: string;
  group: string;
  students: number;
  capacity: number;
  room: string | null;
}

export default function DataViewPage() {
  const [lecturers, setLecturers] = useState<Lecturer[]>([]);
  const [rooms, setRooms] = useState<Room[]>([]);
  const [timeslots, setTimeslots] = useState<Timeslot[]>([]);
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      const [lectRes, roomRes, timeRes, courseRes] = await Promise.all([
        API.get("/data/lecturers"),
        API.get("/data/rooms"),
        API.get("/data/timeslots"),
        API.get("/data/courses")
      ]);
      setLecturers(lectRes.data);
      setRooms(roomRes.data);
      setTimeslots(timeRes.data);
      setCourses(courseRes.data);
    } catch (error) {
      console.error("Error loading data:", error);
      setError("Failed to load data. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p className="loading-text">Loading data...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6">
        <div className="error-container">
          <p className="error-text">{error}</p>
          <button
            onClick={loadData}
            className="retry-button"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="data-view-container p-6">
      <div className="data-view-header">
        <h1 className="data-view-title">Data Overview</h1>
        <p className="data-view-subtitle">View all your timetable data in one place</p>
      </div>

      <div className="data-grid">
        {/* Lecturers Section */}
        <div className="data-card">
          <div className="data-card-header">
            <h2 className="data-card-title">Lecturers</h2>
            <span className="data-count data-count-blue">{lecturers.length}</span>
          </div>
          <div className="data-list">
            {lecturers.length === 0 ? (
              <p className="text-gray-500 text-center py-4">No lecturers added yet</p>
            ) : (
              lecturers.map((lecturer) => (
                <div key={lecturer.id} className="data-item">
                  <div className="data-item-header">
                    <p className="data-item-title">{lecturer.name}</p>
                  </div>
                  {lecturer.unavailable_slots.length > 0 && (
                    <div className="data-item-details">
                      <p>Unavailability: {lecturer.unavailable_slots.join(", ")}</p>
                    </div>
                  )}
                </div>
              ))
            )}
          </div>
        </div>

        {/* Rooms Section */}
        <div className="data-card">
          <div className="data-card-header">
            <h2 className="data-card-title">Rooms</h2>
            <span className="data-count data-count-green">{rooms.length}</span>
          </div>
          <div className="data-list">
            {rooms.length === 0 ? (
              <p className="text-gray-500 text-center py-4">No rooms added yet</p>
            ) : (
              rooms.map((room) => (
                <div key={room.id} className="data-item">
                  <div className="data-item-header">
                    <p className="data-item-title">{room.id}</p>
                  </div>
                  <div className="data-item-details">
                    <p>Capacity: {room.capacity} students</p>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Timeslots Section */}
        <div className="data-card">
          <div className="data-card-header">
            <h2 className="data-card-title">Timeslots</h2>
            <span className="data-count data-count-purple">{timeslots.length}</span>
          </div>
          <div className="data-list">
            {timeslots.length === 0 ? (
              <p className="text-gray-500 text-center py-4">No timeslots added yet</p>
            ) : (
              timeslots.map((timeslot) => (
                <div key={timeslot.id} className="data-item">
                  <div className="data-item-header">
                    <p className="data-item-title">{timeslot.id}</p>
                  </div>
                  <div className="data-item-details">
                    <p>{timeslot.day} - {timeslot.time}</p>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Courses Section */}
        <div className="data-card">
          <div className="data-card-header">
            <h2 className="data-card-title">Courses</h2>
            <span className="data-count data-count-orange">{courses.length}</span>
          </div>
          <div className="data-list max-h-96 overflow-y-auto">
            {courses.length === 0 ? (
              <p className="text-gray-500 text-center py-4">No courses added yet</p>
            ) : (
              courses.map((course) => (
                <div key={course.id} className="data-item">
                  <div className="data-item-header">
                    <p className="data-item-title">{course.name}</p>
                    <span className="data-item-badge">{course.group}</span>
                  </div>
                  <div className="data-item-details">
                    <p>Lecturer: {course.lecturer}</p>
                    <p>Students: {course.students} | Capacity: {course.capacity}</p>
                    {course.room && <p>Room: {course.room}</p>}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>

      {/* Summary Stats */}
      <div className="summary-card">
        <h2 className="summary-title">Summary</h2>
        <div className="summary-grid">
          <div className="summary-stat">
            <div className="summary-number summary-number-blue">{lecturers.length}</div>
            <div className="summary-label">Lecturers</div>
          </div>
          <div className="summary-stat">
            <div className="summary-number summary-number-green">{rooms.length}</div>
            <div className="summary-label">Rooms</div>
          </div>
          <div className="summary-stat">
            <div className="summary-number summary-number-purple">{timeslots.length}</div>
            <div className="summary-label">Timeslots</div>
          </div>
          <div className="summary-stat">
            <div className="summary-number summary-number-orange">{courses.length}</div>
            <div className="summary-label">Courses</div>
          </div>
        </div>
      </div>
    </div>
  );
}