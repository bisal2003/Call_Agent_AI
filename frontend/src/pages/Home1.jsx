import { useState, useRef, useEffect } from "react";
import axios from "axios";
import { Mic } from "lucide-react";
import AuthImagePattern from "../components/AuthImagePattern";
import { toast } from "react-hot-toast";

const HomePage = () => {
  // Form states
  const [salespersonName, setSalespersonName] = useState("chinmoy");
  const [salespersonRole, setSalespersonRole] = useState("salesman");
  const [companyName, setCompanyName] = useState("bharat electrconic");
  const [companyBusiness, setCompanyBusiness] = useState("selling electronics");
  const [companyValues, setCompanyValues] = useState("honesty");
  const [conversationPurpose, setConversationPurpose] = useState("sell tv");
  const [conversationType, setConversationType] = useState("call");
  const [withTools, setWithTools] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [errors, setErrors] = useState({});

  // Audio states
  const [audioUrl, setAudioUrl] = useState(null);
  const [isRecording, setIsRecording] = useState(false);
  const [isMicActive, setIsMicActive] = useState(false);
  const [audioMessage, setAudioMessage] = useState("");
  const [isEndOfCall, setIsEndOfCall] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);

  // Refs for audio handling
  const mediaRecorderRef = useRef(null);
  const streamRef = useRef(null);
  const audioChunksRef = useRef([]);
  const audioRef = useRef(null);
  const silenceCounterRef = useRef(0); // Counter for consecutive silent chunks

  // Form validation
  const validateForm = () => {
    const newErrors = {};
    if (!salespersonName.trim()) newErrors.salespersonName = "Required";
    if (!salespersonRole.trim()) newErrors.salespersonRole = "Required";
    if (!companyName.trim()) newErrors.companyName = "Required";
    if (!companyBusiness.trim()) newErrors.companyBusiness = "Required";
    if (!companyValues.trim()) newErrors.companyValues = "Required";
    if (!conversationPurpose.trim()) newErrors.conversationPurpose = "Required";
    if (!conversationType.trim()) newErrors.conversationType = "Required";
    return newErrors;
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    const newErrors = validateForm();
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    try {
      await axios.post(
        "http://127.0.0.1:5000/get_info",
        {
          salespersonName,
          salespersonRole,
          companyName,
          companyBusiness,
          companyValues,
          conversationPurpose,
          conversationType,
          withTools,
        },
        { withCredentials: true }
      );
      setIsSubmitted(true);
      toast.success("Form submitted successfully!");
      handleMicClick(); // Trigger initial audio playback
    } catch (error) {
      toast.error("Failed to submit form. Please try again.");
      console.error("Error submitting form:", error);
    }
  };

  // Start recording
  const startRecording = async () => {
    try {
      if (!streamRef.current) {
        const stream = await navigator.mediaDevices.getUserMedia({
          audio: {
            sampleRate: 16000,
            sampleSize: 16,
            channelCount: 1,
            echoCancellation: true,
            noiseSuppression: true,
          },
        });
        streamRef.current = stream;
      }

      audioChunksRef.current = [];
      mediaRecorderRef.current = new MediaRecorder(streamRef.current, {
        mimeType: "audio/webm",
      });

      mediaRecorderRef.current.ondataavailable = async (event) => {
        if (event.data.size > 0) {
          const audioBlob = new Blob([event.data], { type: "audio/webm" });
          await sendAudioChunkToServer(audioBlob);
        }
      };

      mediaRecorderRef.current.start(1000); // Record in 1-second chunks
      setIsRecording(true);
      setIsMicActive(true);
    } catch (error) {
      console.error("Error starting recording:", error);
      toast.error("Failed to start recording");
    }
  };

  // Stop recording
  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      setIsMicActive(false);
    }
  };

  // Send audio chunk to backend
  const sendAudioChunkToServer = async (audioBlob) => {
    const formData = new FormData();
    formData.append("audio", audioBlob, "user-audio-chunk.webm");

    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/upload_audio_chunk",
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
          timeout: 30000,
        }
      );

      if (response.data.isSilent) {
        silenceCounterRef.current += 1;
        if (silenceCounterRef.current >= 3) {
          stopRecording(); // Stop recording if 3 consecutive silent chunks
          silenceCounterRef.current = 0;
        }
      } else {
        silenceCounterRef.current = 0; // Reset silence counter
      }
    } catch (error) {
      console.error("Error sending audio chunk:", error);
      toast.error("Failed to send audio chunk. Please try again.");
    }
  };

  // Handle mic click (initial audio playback)
  const handleMicClick = async () => {
    try {
      setIsMicActive(true);
      setIsProcessing(true);

      const response = await axios.get("http://127.0.0.1:5000/agent", {
        timeout: 30000,
      });

      setAudioUrl(response.data.audioUrl);
      setAudioMessage(response.data.message || "");
      setIsEndOfCall(response.data.isEndOfCall || false);

      if (response.data.isEndOfCall) {
        toast.success("Call completed successfully!");
      }

      setIsProcessing(false);
    } catch (error) {
      console.error("Error fetching initial audio:", error);
      toast.error("Failed to start conversation");
      setIsMicActive(false);
      setIsProcessing(false);
    }
  };

  // Automatically start recording after audio playback ends
  useEffect(() => {
    if (audioRef.current) {
      audioRef.current.onended = () => {
        if (!isEndOfCall) {
          startRecording(); // Automatically start recording
        }
      };
    }
  }, [audioUrl, isEndOfCall]);

  // Audio playback
  useEffect(() => {
    if (audioUrl) {
      const fullAudioUrl = `http://127.0.0.1:5000/audio/${audioUrl}`;
      console.log("Attempting to play audio from:", fullAudioUrl);

      const audio = new Audio(fullAudioUrl);
      audioRef.current = audio;

      audio.play().catch((error) => {
        console.error("Error playing audio:", error);
        toast.error("Failed to play audio: " + error.message);
      });
    }
  }, [audioUrl, isEndOfCall]);

  // Cleanup
  useEffect(() => {
    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((track) => track.stop());
      }
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current = null;
      }
    };
  }, []);

  return (
    <div className="h-screen grid lg:grid-cols-2">
      {/* Left Side - Form */}
      <div className="flex flex-col justify-center items-center p-6 sm:p-12">
        <div className="w-full max-w-md space-y-8">
          <div className="flex justify-center">
            <p className="text-2xl font-semibold">CallMate</p>
          </div>

        
          {/* Form */}
          <form
            onSubmit={handleSubmit}
            className="space-y-6"
            style={{
              pointerEvents: isSubmitted ? "none" : "auto",
              opacity: isSubmitted ? 0.5 : 1,
            }}
          >
            {/* Salesperson Name */}
            <div className="form-control">
              <label className="label">
                <span className="label-text font-medium">Salesperson Name</span>
              </label>
              <input
                type="text"
                value={salespersonName}
                onChange={(e) => setSalespersonName(e.target.value)}
                placeholder="Enter salesperson name"
                className={`input input-bordered w-full ${
                  errors.salespersonName ? "input-error" : ""
                }`}
              />
              {errors.salespersonName && (
                <p className="text-red-500 text-sm mt-1">
                  {errors.salespersonName}
                </p>
              )}
            </div>

            {/* Salesperson Role */}
            <div className="form-control">
              <label className="label">
                <span className="label-text font-medium">Salesperson Role</span>
              </label>
              <input
                type="text"
                value={salespersonRole}
                onChange={(e) => setSalespersonRole(e.target.value)}
                placeholder="Enter salesperson role"
                className={`input input-bordered w-full ${
                  errors.salespersonRole ? "input-error" : ""
                }`}
              />
              {errors.salespersonRole && (
                <p className="text-red-500 text-sm mt-1">
                  {errors.salespersonRole}
                </p>
              )}
            </div>

            {/* Company Name */}
            <div className="form-control">
              <label className="label">
                <span className="label-text font-medium">Company Name</span>
              </label>
              <input
                type="text"
                value={companyName}
                onChange={(e) => setCompanyName(e.target.value)}
                placeholder="Enter company name"
                className={`input input-bordered w-full ${
                  errors.companyName ? "input-error" : ""
                }`}
              />
              {errors.companyName && (
                <p className="text-red-500 text-sm mt-1">
                  {errors.companyName}
                </p>
              )}
            </div>

            {/* Company Business */}
            <div className="form-control">
              <label className="label">
                <span className="label-text font-medium">Company Business</span>
              </label>
              <input
                type="text"
                value={companyBusiness}
                onChange={(e) => setCompanyBusiness(e.target.value)}
                placeholder="Enter company business"
                className={`input input-bordered w-full ${
                  errors.companyBusiness ? "input-error" : ""
                }`}
              />
              {errors.companyBusiness && (
                <p className="text-red-500 text-sm mt-1">
                  {errors.companyBusiness}
                </p>
              )}
            </div>

            {/* Company Values */}
            <div className="form-control">
              <label className="label">
                <span className="label-text font-medium">Company Values</span>
              </label>
              <input
                type="text"
                value={companyValues}
                onChange={(e) => setCompanyValues(e.target.value)}
                placeholder="Enter company values"
                className={`input input-bordered w-full ${
                  errors.companyValues ? "input-error" : ""
                }`}
              />
              {errors.companyValues && (
                <p className="text-red-500 text-sm mt-1">
                  {errors.companyValues}
                </p>
              )}
            </div>

            {/* Conversation Purpose */}
            <div className="form-control">
              <label className="label">
                <span className="label-text font-medium">
                  Conversation Purpose
                </span>
              </label>
              <input
                type="text"
                value={conversationPurpose}
                onChange={(e) => setConversationPurpose(e.target.value)}
                placeholder="Enter purpose of conversation"
                className={`input input-bordered w-full ${
                  errors.conversationPurpose ? "input-error" : ""
                }`}
              />
              {errors.conversationPurpose && (
                <p className="text-red-500 text-sm mt-1">
                  {errors.conversationPurpose}
                </p>
              )}
            </div>

            {/* Conversation Type */}
            <div className="form-control">
              <label className="label">
                <span className="label-text font-medium">
                  Conversation Type
                </span>
              </label>
              <input
                type="text"
                value={conversationType}
                onChange={(e) => setConversationType(e.target.value)}
                placeholder="Enter type of conversation"
                className={`input input-bordered w-full ${
                  errors.conversationType ? "input-error" : ""
                }`}
              />
              {errors.conversationType && (
                <p className="text-red-500 text-sm mt-1">
                  {errors.conversationType}
                </p>
              )}
            </div>

            <div className="form-control">
              <label className="label cursor-pointer">
                <span className="label-text font-medium">With Tools</span>
                <input
                  type="checkbox"
                  checked={withTools}
                  onChange={(e) => setWithTools(e.target.checked)}
                  className="checkbox checkbox-primary ml-2"
                />
              </label>
            </div>

            {/* Submit Button */}
            <button type="submit" className="btn btn-primary w-full">
              Submit
            </button>
          </form>
        </div>
      </div>

      {/* Right Side - Conversation Interface */}
      <div className="h-screen flex flex-col items-center justify-center">
        {!isSubmitted ? (
          <AuthImagePattern
            title="Welcome to CallMate"
            subtitle="Submit the form to start your conversation"
          />
        ) : (
          <div className="flex flex-col items-center justify-center space-y-6">
            <Mic
              onClick={isProcessing ? null : startRecording}
              className={`w-16 h-16 cursor-pointer transition-all duration-200 ${
                isProcessing
                  ? "text-gray-400"
                  : isMicActive
                  ? "text-red-500 scale-110"
                  : "text-primary"
              }`}
            />

            {isProcessing && (
              <div className="flex flex-col items-center">
                <div className="text-blue-500 text-lg font-semibold animate-pulse">
                  Processing...
                </div>
                <p className="text-gray-500 text-sm mt-2">
                  Please wait while we process your request
                </p>
              </div>
            )}

            {isRecording && !isProcessing && (
              <div className="flex flex-col items-center">
                <div className="text-red-500 text-lg font-semibold animate-pulse">
                  Recording...
                </div>
                <p className="text-gray-500 text-sm mt-2">
                  Speak now. Recording will stop automatically (after 3 sec of
                  silence).
                </p>
              </div>
            )}

            {audioUrl && !isRecording && !isProcessing && (
              <div className="flex flex-col items-center">
                <div className="text-blue-500 text-lg font-semibold">
                  {isEndOfCall ? "Call Completed" : "Playing response..."}
                </div>
                <p className="text-gray-600 text-sm mt-4 max-w-md text-center">
                  {audioMessage}
                </p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default HomePage;