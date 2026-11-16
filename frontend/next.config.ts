import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Produces a self-contained server in .next/standalone for the Docker image.
  // Vercel ignores this and uses its own build output.
  output: "standalone",
};

export default nextConfig;
