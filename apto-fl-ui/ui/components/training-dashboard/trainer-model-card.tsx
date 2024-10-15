import { TrainerModel } from "@/lib/types";
import React from "react";

const TrainerModelCard = (props: TrainerModel) => {
  // reward calc
  const aptosToDollar = 10;
  const rewardInAptos = props.epochs * 0.1;
  const rewardInDollars = rewardInAptos * aptosToDollar; // TODO: Calculate reward, ye to aise hi kra hai abhi
  const formattedRewardInUSD = Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(Number(rewardInDollars));

  const truncatedWallet =
    props.walletAddress.slice(0, 6) + "..." + props.walletAddress.slice(-6);

  return (
    <div className="rounded-t bg-accent/50 p-3 border-b transition-all duration-200 hover:bg-accent/70">
      <div className="flex flex-row gap-2">
        <div className="flex-1">
          <p
            className="text-lg font-semibold text-card-foreground line-clamp-2"
            title={props.title}
          >
            {props.title}
          </p>
          <p
            className="text-sm font-medium text-muted-foreground mt-1 line-clamp-2"
            title={props.description}
          >
            {props.description}
          </p>
        </div>
        <div className="w-36 bg-card rounded-md flex flex-col p-3 border-t justify-between">
          <p className="text-xs text-muted-foreground font-medium mb-2">
            Reward
          </p>
          <div>
            <p className="text-3xl  font-display text-primary">
              {formattedRewardInUSD}
            </p>
            <p className="text-xs font-bold text-muted-foreground">
              {rewardInAptos.toFixed(3)} APT
            </p>
          </div>
        </div>
      </div>
      <div className="flex flex-col lg:flex-row gap-2 mt-4 text-sm *:rounded">
        <div className="flex items-center justify-between flex-1 p-2 bg-card">
          <p className="font-medium">Epochs</p>
          <p className="bg-accent text-accent-foreground px-2 rounded font-bold text-xs py-1">
            {props.epochs}
          </p>
        </div>
        <div className="flex items-center justify-between flex-1 p-2 bg-card">
          <p className="font-medium">Stake</p>
          <p className="bg-accent text-highlight px-2 rounded font-bold inline-flex text-xs py-1">
            {props.stakeAmount.toFixed(3)} APT
          </p>
        </div>
      </div>
      <div className="flex justify-between items-center mt-2">
        <span className="text-xs font-medium text-muted-foreground">
          {props.createdAt.toLocaleDateString("en-US", {
            day: "2-digit",
            month: "2-digit",
            year: "numeric",
          })}{" "}
          | <span className="text-foreground"> {truncatedWallet} </span>
        </span>
      </div>
    </div>
  );
};

export default TrainerModelCard;
