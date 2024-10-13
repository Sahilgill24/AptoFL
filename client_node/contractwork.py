import asyncio

from aptos_sdk.account import Account
from aptos_sdk.account_address import AccountAddress
from aptos_sdk.async_client import RestClient,FaucetClient
from aptos_sdk.transactions import EntryFunction, TransactionArgument, TransactionPayload

from typing import Any, Dict, Optional
from aptos_sdk.bcs import Serializer

from common import NODE_URL,FAUCET_URL

class HelloBlockchainClient(RestClient):
    async def get_message(
        self, contract_address: AccountAddress, account_address: AccountAddress
    ) -> Optional[Dict[str, Any]]:
        """Retrieve the resource message::MessageHolder::message"""
        try:
            return await self.account_resource(
                account_address, f"{contract_address}::message::MessageHolder"
            )
        except ResourceNotFound:
            return None

    async def set_message(
        self, contract_address: AccountAddress, sender: Account, message: str
    ) -> str:
        """Potentially initialize and set the resource message::MessageHolder::message"""

        payload = EntryFunction.natural(
            f"{contract_address}::message",
            "set_message",
            [],
            [TransactionArgument(message, Serializer.str)],
        )
        signed_transaction = await self.create_bcs_signed_transaction(
            sender, TransactionPayload(payload)
        )
        return await self.submit_bcs_transaction(signed_transaction)


async def main2(contract_address):
    my_account =  Account.generate()
    print(my_account)
    
    
    rest_client = RestClient(NODE_URL)
    faucet_client = FaucetClient(FAUCET_URL, rest_client)
    my_account_fund = await faucet_client.fund_account(my_account.address(), 10_000_000)
    print(NODE_URL)
    rest_cleint2 = HelloBlockchainClient(NODE_URL)
    txn_hash = await rest_cleint2.set_message(
        contract_address, my_account, "Hello, Blockchain"
    )
    total_apt= await rest_client.account_balance(AccountAddress.from_str("0xe24193f1a406f505817f6d16509b738ab35f8e599d34b2a170b07eba46c59880"))
    print(total_apt)
    await rest_client.wait_for_transaction(txn_hash)
    print("Transaction complete")
    print(txn_hash)

if __name__ == "__main__":
    asyncio.run(main2("0xef8351c2a082733387f812b5c96872a1650776cd9a3c9b19711c4754f0ef3fb0"))