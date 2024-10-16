"use client";

import { useEffect, useState } from "react";
import { TrainerModel } from "@/lib/types";
import { sampleTrainerModels } from "@/lib/sample-data/trainer-model-data";
import TrainerModelCard from "./trainer-model-card";
import { useModelStore } from "@/lib/stores/model-store";
import { useTrainerModelStore } from "@/lib/stores/trainer-model-store";

const TrainerModelView = ({ status }: { status: TrainerModel["status"] }) => {
  const [filteredModels, setFilteredModels] = useState<TrainerModel[]>([]);
  const {models} = useTrainerModelStore();
  const [loading, setLoading] = useState<boolean>(true);

    useEffect(() => {
    setFilteredModels(models.filter((model) => model.status === status));
    }, [models, status]);

  return (
    <div className="grid grid-cols-2 lg:grid-cols-3  gap-4">
      {loading ? (
        <p>loading...</p>
      ) : (
        filteredModels.map((model) => (
          <TrainerModelCard key={model.id} {...model} />
        ))
      )}
    </div>
  );
};

export default TrainerModelView;
