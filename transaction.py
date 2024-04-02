from solana.rpc.api import Client
from spl.token.client import Token
from solders.pubkey import Pubkey
from solders.keypair import Keypair
import json

with open('./config.json', 'r') as f:
    config_data = json.load(f)

# Create a client to interact with the Solana beta mainnet
solana_client = Client("https://api.devnet.solana.com")
#solana_client = Client("https://api.mainnet-beta.solana.com")


def get_latest_transaction():

    # Get the latest transaction    
    successs = 0
    triall = 0
    
    while (successs == 0) :
        try:

            latest_slot = solana_client.get_slot().value
            latest_slot = latest_slot - 1

            blockhashhh = str(solana_client.get_block(latest_slot).value.blockhash)
            signaturess = str(solana_client.get_block(latest_slot).value.transactions[0].transaction.signatures[0])
            keyyy = str(solana_client.get_block(latest_slot).value.transactions[0].transaction.message.account_keys[0])
            successs = 1

        except:
            successs = 0
            triall = triall +1
    return blockhashhh,signaturess,keyyy


def transfer_token(winner_address):
    print("transfer token program start")

    coin_addr = config_data["Prize"]["coin_addr"]
    program_id = config_data["Prize"]["program_id"]
    private_key = config_data["Prize"]["private_key"]
    sender_addr = config_data["Prize"]["sender_addr"]

    mintt = Pubkey.from_string(coin_addr) #eg: our coin address
    program_idd = Pubkey.from_string(program_id) #eg: this is default, no need to change for any coins

    privkeyy=private_key #the private address of sender/your address
    key_pairr = Keypair.from_base58_string(privkeyy)

    spl_client = Token(conn=solana_client, pubkey=mintt, program_id=program_idd, payer=key_pairr)

    source = Pubkey.from_string(sender_addr)  #sender address
    print("Winner address is = ",winner_address)
    dest = Pubkey.from_string(winner_address)      #winner address

    try:
        source_token_account = spl_client.get_accounts_by_owner(owner=source, commitment=None, encoding='base64').value[0].pubkey
    except:
        source_token_account = spl_client.create_associated_token_account(owner=source, skip_confirmation=False, recent_blockhash=None)
    try:
        dest_token_account = spl_client.get_accounts_by_owner(owner=dest, commitment=None, encoding='base64').value[0].pubkey
    except:
        dest_token_account = spl_client.create_associated_token_account(owner=dest, skip_confirmation=False, recent_blockhash=None)

    amountt = 1.0
    amountt = int(float(amountt)*10000) #send 10 token

    try:
        transaction = spl_client.transfer(source=source_token_account, dest=dest_token_account, owner=key_pairr, amount=amountt, multi_signers=None, opts=None, recent_blockhash=None)
    except:
        transaction ='error in transaction'

    return transaction




