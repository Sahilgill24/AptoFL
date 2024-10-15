import asyncio

from aptos_sdk.account import Account
from aptos_sdk.account_address import AccountAddress
from aptos_sdk.async_client import RestClient,FaucetClient
from aptos_sdk.transactions import EntryFunction, TransactionArgument, TransactionPayload

from common import NODE_URL,FAUCET_URL
# contract object address: 0xe60a1dc08fedd5c73b95f4c7983b12d8c8a22be8dae1ade5a3b98322cb9961b1
from typing import Any, Dict, Optional
from aptos_sdk.bcs import Serializer

class RegistryClient(RestClient):
    async def register_user(self,contract_address: AccountAddress,sender: Account,new_user_id:str)-> str:
        payload = EntryFunction.natural(
            f"{contract_address}::user_registration",
            "register_user",
            [],
            [TransactionArgument(new_user_id, Serializer.str)],
        )
        signed_transaction = await self.create_bcs_signed_transaction(
            sender, TransactionPayload(payload)
        )
        return await self.submit_bcs_transaction(signed_transaction)


async def register_user(contract_address):
    my_account =  Account.generate()
    
    
    
    rest_client = RestClient(NODE_URL)
    faucet_client = FaucetClient(FAUCET_URL, rest_client)
    my_account_fund = await faucet_client.fund_account(my_account.address(), 10_000_000)
    print(NODE_URL)
    registry_client = RegistryClient(NODE_URL)
    txn_hash = await registry_client.register_user(
        contract_address, my_account, "Sahil "
    )
    # total_apt= await rest_client.account_balance(AccountAddress.from_str("0xe24193f1a406f505817f6d16509b738ab35f8e599d34b2a170b07eba46c59880"))
    # print(total_apt)
    await rest_client.wait_for_transaction(txn_hash)
    print("Transaction complete")
    print(txn_hash)


if __name__ == "__main__":
    asyncio.run(register_user("0xe60a1dc08fedd5c73b95f4c7983b12d8c8a22be8dae1ade5a3b98322cb9961b1"))