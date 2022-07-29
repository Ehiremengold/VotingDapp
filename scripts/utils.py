from brownie import accounts, network, config
import eth_utils

local_dev_env = ["development", "ganache"]


def get_account(index=None, id=None):
    if id:
        return accounts.load(id)
    if index:
        return accounts[index]
    if network.show_active() in local_dev_env:
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


# def encode_function_initializer(initializer=None, *args):
#     if len(args) == 0:
#         return eth_utils.to_bytes(hexstr="0x")
#     return initializer.encode_input(*args)


# def upgrade(
#     new_implementation, proxy, account, proxy_admin=None, initializer=None, *args
# ):
#     transaction = None
#     if proxy_admin:
#         if initializer:
#             encoded_function_data = encode_function_initializer(initializer, *args)
#             transaction = proxy_admin.upradeAndCall(
#                 proxy.address,
#                 new_implementation.address,
#                 encoded_function_data,
#                 {"from": account},
#             )
#             transaction.wait(1)
#         else:
#             transaction = proxy_admin.upgrade(
#                 proxy.address, new_implementation.address, {"from": account}
#             )
#             transaction.wait(1)
#     else:
#         if initializer:
#             encoded_function_data = encode_function_initializer(initializer, *args)
#             transaction = proxy_admin.upgradeToAndCall(
#                 new_implementation.address, encoded_function_data, {"from": account}
#             )
#             transaction.wait(1)
#         else:
#             transaction = proxy_admin.upgradeTo(
#                 new_implementation.address, {"from": account}
#             )
#             transaction.wait(1)
#     return transaction
