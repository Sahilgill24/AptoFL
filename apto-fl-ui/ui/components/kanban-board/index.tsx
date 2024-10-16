"use client";
import React, { useState } from "react";
import Column from "./column";
import { PublisherModel } from "@/lib/types";
import { useModelStore } from "@/lib/stores/model-store";

export const PublisherKanbanBoard: React.FC = () => {
  const { models, setModels} = useModelStore();

  return (
    <div className="flex h-full w-full gap-3 py-6">
      <Column
        title="Drafts"
        column="draft"
        headingColor="text-muted-foreground"
        models={models}
        setModels={setModels}
      />
      <Column
        title="Published"
        column="published"
        headingColor="text-highlight"
        models={models}
        setModels={setModels}
      />
      <Column
        title="Trained"
        column="trained"
        headingColor="text-primary"
        models={models}
        setModels={setModels}
      />
    </div>
  );
};

export default PublisherKanbanBoard;
