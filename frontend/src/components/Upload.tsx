import { useState } from "react";
import API from "../services/api";

interface Props {
  setPath: (path: string) => void;
}

export default function Upload({ setPath }: Props) {
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadedFileName, setUploadedFileName] = useState<string>("");

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file first");
      return;
    }

    // Validate file type
    const validExtensions = [".csv", ".xlsx", ".xls"];
    const fileName = file.name.toLowerCase();
    const hasValidExtension = validExtensions.some(ext => fileName.endsWith(ext));
    
    if (!hasValidExtension) {
      alert("Please upload a CSV or Excel file (.csv, .xlsx, .xls)");
      return;
    }

    setIsUploading(true);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const res = await API.post("/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data"
        }
      });

      console.log("UPLOAD RESPONSE:", res.data);

      if (res.data.path) {
        setPath(res.data.path);
        setUploadedFileName(file.name);
        alert("Upload successful!");
        setFile(null);
      } else {
        alert("Upload failed: No file path returned");
      }
    } catch (err) {
      console.error("UPLOAD ERROR:", err);
      const errorMessage = (err as any).response?.data?.error || (err as any).message || "Unknown error";
      alert("Upload failed: " + errorMessage);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="upload-container">
      <input
        type="file"
        accept=".csv,.xlsx,.xls"
        className="upload-input"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
        disabled={isUploading}
      />
      {file && <p style={{ margin: "0.25rem 0", fontSize: "0.875rem", color: "#059669" }}>Selected: {file.name}</p>}
      {uploadedFileName && <p style={{ margin: "0.25rem 0", fontSize: "0.875rem", color: "#10b981" }}>✓ Uploaded: {uploadedFileName}</p>}
      <button 
        className="upload-button" 
        onClick={handleUpload}
        disabled={isUploading || !file}
      >
        {isUploading ? (
          <>
            <svg className="loading-spinner" viewBox="0 0 24 24">
              <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" strokeDasharray="31.416" strokeDashoffset="31.416">
                <animate attributeName="stroke-dashoffset" dur="1s" values="31.416;0" repeatCount="indefinite"/>
              </circle>
            </svg>
            Uploading...
          </>
        ) : (
          "Upload File"
        )}
      </button>
    </div>
  );
}