import type { Metadata } from "next";
import localFont from "next/font/local";
import "./globals.css";
import { ThemeProvider } from "@/components/theme-provider";

const eiko = localFont({
  src: [
    {
      path: "./fonts/Eiko/PPEiko-Thin.otf",
      weight: "200",
      style: "normal",
    },
    {
      path: "./fonts/Eiko/PPEiko-Medium.otf",
      weight: "400",
      style: "normal",
    },
    {
      path: "./fonts/Eiko/PPEiko-Heavy.otf",
      weight: "700",
      style: "normal",
    },
  ],
  variable: "--font-eiko",
});

const satoshi = localFont({
  src: "./fonts/Satoshi-Variable.ttf",
  variable: "--font-satoshi",
})

export const metadata: Metadata = {
  title: "AptoFL",
  description: "Federated learning built on aptos",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${eiko.variable} ${satoshi.className} antialiased`}>
        <ThemeProvider
          attribute="class"
          defaultTheme="dark"
          enableSystem
          disableTransitionOnChange
        >
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}
