import { useState } from "react";
import API from "../services/api";
import Upload from "../components/Upload";
import TimetableGrid from "../components/TimetableGrid";
import ExportButton from "../components/ExportButton";

export default function Dashboard() {
  const [path, setPath] = useState<string>("");
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [useDatabase, setUseDatabase] = useState(false);
  const [timetableType, setTimetableType] = useState<"course" | "exam">("course");

  const generate = async () => {
    if (!useDatabase && (!path || path.trim() === "")) {
      alert("Please upload a file first or switch to database mode");
      return;
    }

    setLoading(true);

    try {
      const res = await API.post("/timetable/generate", {
        path: useDatabase ? null : path,
        use_database: useDatabase,
        type: timetableType
      });

      let responseData = res.data;
      if (typeof res.data === 'string') {
        try {
          responseData = JSON.parse(res.data);
        } catch (parseError) {
          console.error("Failed to parse server response:", parseError);
          alert("Failed to parse server response. Please check the console for details.");
          return;
        }
      }

      if (responseData.error) {
        alert("Generation failed: " + responseData.error);
        return;
      }

      if (responseData.timetable) {
        setData(responseData.timetable);
      } else {
        alert("Generation failed: No timetable data received");
      }
    } catch (err) {
      console.error("Generation error:", err);
      alert("Generation failed: " + ((err as any).response?.data?.error || (err as any).message));
    }

    setLoading(false);
  };

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1 className="dashboard-title">AI TIMETABLE RESOURCE ALLOCATOR</h1>
        <p className="dashboard-subtitle">Upload your course data or use database data to generate optimized timetables</p>
      </div>

      <div className="dashboard-content">
        <div className="upload-section">
          <div className="section-header">
            <h2>Upload Data</h2>
            <p>Upload your CSV file containing course, lecturer, and student information</p>
            <div className="mt-2">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={useDatabase}
                  onChange={(e) => setUseDatabase(e.target.checked)}
                  className="mr-2"
                />
                Use database data instead of uploaded file
              </label>
            </div>
          </div>
          {!useDatabase && (
            <div className="upload-card">
              <Upload setPath={setPath} />
            </div>
          )}
        </div>

        <div className="generate-section">
          <div className="section-header">
            <h2>Generate Timetable</h2>
            <p>Select timetable type and click the button below to generate an optimized timetable using AI</p>
          </div>
          <div className="generate-card">
            <div className="timetable-type-selector">
              <label className="type-label">
                <input
                  type="radio"
                  value="course"
                  checked={timetableType === "course"}
                  onChange={(e) => setTimetableType(e.target.value as "course" | "exam")}
                />
                Course Timetable
              </label>
              <label className="type-label">
                <input
                  type="radio"
                  value="exam"
                  checked={timetableType === "exam"}
                  onChange={(e) => setTimetableType(e.target.value as "course" | "exam")}
                />
                Exam Timetable
              </label>
            </div>
            <button
              onClick={generate}
              disabled={loading || (!useDatabase && !path)}
              className={`generate-btn ${loading ? 'loading' : ''}`}
            >
              {loading ? (
                <>
                  <svg className="loading-spinner" viewBox="0 0 24 24">
                    <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" strokeDasharray="31.416" strokeDashoffset="31.416">
                      <animate attributeName="stroke-dashoffset" dur="1s" values="31.416;0" repeatCount="indefinite"/>
                    </circle>
                  </svg>
                  Generating...
                </>
              ) : (
                <>
                  <svg className="generate-icon" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-8.293l-3-3a1 1 0 00-1.414 0l-3 3a1 1 0 001.414 1.414L9 9.414V13a1 1 0 102 0V9.414l1.293 1.293a1 1 0 001.414-1.414z" clipRule="evenodd"/>
                  </svg>
                  Generate Timetable
                </>
              )}
            </button>
            {(!useDatabase && !path) && (
              <p className="generate-hint">Please upload a file first or switch to database mode</p>
            )}
          </div>
        </div>

        {data.length > 0 && (
          <div className="results-section">
            <div className="section-header">
              <h2>Generated Timetable</h2>
              <p>Your optimized timetable is ready. You can view it below or export to Excel.</p>
            </div>
            <div className="results-card">
              <div className="results-actions">
                <ExportButton data={data} />
                <div className="results-stats">
                  <span className="stat">
                    <strong>{data.length}</strong> scheduled classes
                  </span>
                </div>
              </div>
              <div className="timetable-container">
                <TimetableGrid data={data} />
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}