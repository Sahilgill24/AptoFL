import {create } from 'zustand';
import { TrainerModel } from '../types';

interface TrainerModelStates {
    models: TrainerModel[];
    updateModel: (model: TrainerModel) => void;
    setModels: (models: TrainerModel[]) => void;
}

export const useTrainerModelStore = create<TrainerModelStates>((set) => ({
    models: [  {
        id: "trainer-1",
        walletAddress: "0x1234567890",
        title: "Federated Learning Model",
        description:
          "A federated learning model.",
        status: "available",
        epochs: 50,
        createdAt: new Date(),
        stakeAmount: 5,
      }],
    updateModel: (model) => set((state) => ({ models: state.models.map((m) => m.id === model.id ? model : m) })),
    setModels: (models) => set({ models }),
}));