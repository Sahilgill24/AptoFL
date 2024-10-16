/** @type {import('next').NextConfig} */
import MiniCssExtractPlugin from "mini-css-extract-plugin";
const nextConfig = {
  async redirects() {
    return [
      {
        source: "/dashboard",
        destination: "/dashboard/publisher",
        permanent: true,
      },
    ];
  },
  plugins: [new MiniCssExtractPlugin()]
};

export default nextConfig;
