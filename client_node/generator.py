# generates the random number that will be used for the commitments

import asyncio

from aptos_sdk.account import Account
from aptos_sdk.account_address import AccountAddress
from aptos_sdk.async_client import RestClient,FaucetClient
from aptos_sdk.transactions import EntryFunction, TransactionArgument, TransactionPayload

from common import NODE_URL,FAUCET_URL
# contract address: 0x1ab6ea4e7d88621e557094b1c80381bb1cb23421db11223b1093e25d313ca012
from typing import Any, Dict, Optional
from aptos_sdk.bcs import Serializer

class generatorClient(RestClient):
    async def generate(self,contract_address: AccountAddress,sender: Account)-> str:
        payload = EntryFunction.natural(
            f"{contract_address}::RandomNumberGenerator",
            "generate_random_value",
            [],
            [],
        )
        signed_transaction = await self.create_bcs_signed_transaction(
            sender, TransactionPayload(payload)
        )
        return await self.submit_bcs_transaction(signed_transaction)


async def generate(contract_address):
    my_account =  Account.generate()
    rest_client = RestClient(NODE_URL)
    faucet_client = FaucetClient(FAUCET_URL, rest_client)
    my_account_fund = await faucet_client.fund_account(my_account.address(), 10_000_000)
    print(NODE_URL)
    generator_client = generatorClient(NODE_URL)
    txn_hash = await generator_client.generate(
        contract_address, my_account
    )
    # total_apt= await rest_client.account_balance(AccountAddress.from_str("0xe24193f1a406f505817f6d16509b738ab35f8e599d34b2a170b07eba46c59880"))
    # print(total_apt)
    await rest_client.wait_for_transaction(txn_hash)
    print("Transaction complete")
    print(txn_hash)


if __name__ == "__main__":
    asyncio.run(generate("0x1ab6ea4e7d88621e557094b1c80381bb1cb23421db11223b1093e25d313ca012"))