import { ImageResponse } from "next/og";

export const runtime = "edge";

export const alt = "PingDiff - Know Your Connection Before You Queue";
export const size = {
  width: 1200,
  height: 630,
};
export const contentType = "image/png";

export default function Image() {
  return new ImageResponse(
    (
      <div
        style={{
          background: "linear-gradient(135deg, #09090b 0%, #18181b 50%, #09090b 100%)",
          width: "100%",
          height: "100%",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          fontFamily: "Inter, sans-serif",
          padding: "60px",
        }}
      >
        {/* Logo / Title */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "16px",
            marginBottom: "24px",
          }}
        >
          <div
            style={{
              width: "56px",
              height: "56px",
              borderRadius: "12px",
              background: "linear-gradient(135deg, #22c55e, #16a34a)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: "28px",
            }}
          >
            ⚡
          </div>
          <span
            style={{
              fontSize: "56px",
              fontWeight: 700,
              color: "#ffffff",
              letterSpacing: "-1px",
            }}
          >
            PingDiff
          </span>
        </div>

        {/* Tagline */}
        <div
          style={{
            fontSize: "28px",
            color: "#a1a1aa",
            marginBottom: "48px",
            textAlign: "center",
          }}
        >
          Know Your Connection Before You Queue
        </div>

        {/* Stats row */}
        <div
          style={{
            display: "flex",
            gap: "48px",
          }}
        >
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              padding: "24px 40px",
              background: "rgba(255,255,255,0.05)",
              borderRadius: "16px",
              border: "1px solid rgba(255,255,255,0.1)",
            }}
          >
            <span style={{ fontSize: "40px", fontWeight: 700, color: "#22c55e" }}>9</span>
            <span style={{ fontSize: "18px", color: "#a1a1aa", marginTop: "4px" }}>Games</span>
          </div>
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              padding: "24px 40px",
              background: "rgba(255,255,255,0.05)",
              borderRadius: "16px",
              border: "1px solid rgba(255,255,255,0.1)",
            }}
          >
            <span style={{ fontSize: "40px", fontWeight: 700, color: "#22c55e" }}>141</span>
            <span style={{ fontSize: "18px", color: "#a1a1aa", marginTop: "4px" }}>Servers</span>
          </div>
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              padding: "24px 40px",
              background: "rgba(255,255,255,0.05)",
              borderRadius: "16px",
              border: "1px solid rgba(255,255,255,0.1)",
            }}
          >
            <span style={{ fontSize: "40px", fontWeight: 700, color: "#22c55e" }}>Free</span>
            <span style={{ fontSize: "18px", color: "#a1a1aa", marginTop: "4px" }}>Forever</span>
          </div>
        </div>

        {/* URL */}
        <div
          style={{
            position: "absolute",
            bottom: "32px",
            fontSize: "20px",
            color: "#52525b",
          }}
        >
          pingdiff.com
        </div>
      </div>
    ),
    {
      ...size,
    },
  );
}
