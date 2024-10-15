"use client";

import { Button } from "@/components/ui/button";
import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();
  return (
    <div className="flex h-screen w-full items-center justify-center flex-col gap-8">
      <h1 className="text-8xl font-light font-display text-transparent bg-clip-text bg-gradient-to-r from-primary to-highlight">
        Apto-FL
      </h1>
      <p className="text-2xl text-muted-foreground">
        Privacy preserving federated learning, now on Aptos
      </p>
      <Button
        variant={"shine"}
        size={"lg"}
        className="font-semibold"
        onClick={() => router.push("/dashboard")}
      >
        Get Started
      </Button>
    </div>
  );
}
