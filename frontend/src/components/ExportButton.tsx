import { useState } from "react";
import API from "../services/api";

interface Props {
  data: any[];
  timetableType?: "course" | "exam";
}

export default function ExportButton({ data, timetableType = "course" }: Props) {
  const [isExporting, setIsExporting] = useState(false);
  const [showDialog, setShowDialog] = useState(false);
  const [filename, setFilename] = useState("timetable");
  const [format, setFormat] = useState("xlsx");

  const handleExport = async () => {
    if (!data || data.length === 0) {
      alert("No timetable data to export");
      return;
    }

    const fullFilename = `${filename}.${format}`;

    setIsExporting(true);

    try {
      const res = await API.post(
        "/export",
        { timetable: data, filename: fullFilename, format, timetable_type: timetableType },
        { responseType: "blob" }
      );

      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement("a");

      link.href = url;
      link.setAttribute("download", fullFilename);
      document.body.appendChild(link);
      link.click();
      
      // Clean up
      window.URL.revokeObjectURL(url);
      document.body.removeChild(link);
      
      setShowDialog(false);
      setFilename("timetable");
      setFormat("xlsx");
      alert("Timetable exported successfully!");
    } catch (err) {
      console.error("EXPORT ERROR:", err);
      alert("Export failed: " + ((err as any).response?.data?.error || (err as any).message));
    } finally {
      setIsExporting(false);
    }
  };

  return (
    <>
      <button 
        className="export-button" 
        onClick={() => setShowDialog(true)}
        disabled={isExporting || !data || data.length === 0}
      >
        {isExporting ? (
          <>
            <svg className="loading-spinner" viewBox="0 0 24 24">
              <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" strokeDasharray="31.416" strokeDashoffset="31.416">
                <animate attributeName="stroke-dashoffset" dur="1s" values="31.416;0" repeatCount="indefinite"/>
              </circle>
            </svg>
            Exporting...
          </>
        ) : (
          "Export Timetable"
        )}
      </button>

      {showDialog && (
        <div className="export-modal-overlay">
          <div className="export-modal">
            <div className="export-modal-header">
              <h2>Export Timetable</h2>
              <button 
                className="export-modal-close"
                onClick={() => setShowDialog(false)}
                disabled={isExporting}
              >
                ✕
              </button>
            </div>

            <div className="export-modal-content">
              <div className="export-form-group">
                <label htmlFor="filename">Filename:</label>
                <div className="export-filename-input">
                  <input 
                    id="filename"
                    type="text" 
                    value={filename}
                    onChange={(e) => setFilename(e.target.value.replace(/[<>:"/\\|?*]/g, ""))}
                    placeholder="timetable"
                    disabled={isExporting}
                  />
                  <span className="export-extension">.{format}</span>
                </div>
              </div>

              <div className="export-form-group">
                <label htmlFor="format">Format:</label>
                <select 
                  id="format"
                  value={format}
                  onChange={(e) => setFormat(e.target.value)}
                  disabled={isExporting}
                >
                  <option value="xlsx">Excel (.xlsx)</option>
                  <option value="csv">CSV (.csv)</option>
                </select>
              </div>
            </div>

            <div className="export-modal-footer">
              <button 
                className="export-modal-cancel"
                onClick={() => setShowDialog(false)}
                disabled={isExporting}
              >
                Cancel
              </button>
              <button 
                className="export-modal-confirm"
                onClick={handleExport}
                disabled={isExporting || !filename.trim()}
              >
                {isExporting ? "Exporting..." : "Export"}
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}