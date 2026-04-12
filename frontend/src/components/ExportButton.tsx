import { useState } from "react";
import API from "../services/api";

interface Props {
  data: any[];
}

export default function ExportButton({ data }: Props) {
  const [isExporting, setIsExporting] = useState(false);

  const handleExport = async () => {
    if (!data || data.length === 0) {
      alert("No timetable data to export");
      return;
    }

    setIsExporting(true);

    try {
      const res = await API.post(
        "/export",
        { timetable: data },
        { responseType: "blob" }
      );

      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement("a");

      link.href = url;
      link.setAttribute("download", "timetable.xlsx");
      document.body.appendChild(link);
      link.click();
      
      // Clean up
      window.URL.revokeObjectURL(url);
      document.body.removeChild(link);
      
      alert("Timetable exported successfully!");
    } catch (err) {
      console.error("EXPORT ERROR:", err);
      alert("Export failed: " + ((err as any).response?.data?.error || (err as any).message));
    } finally {
      setIsExporting(false);
    }
  };

  return (
    <button 
      className="export-button" 
      onClick={handleExport}
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
  );
}