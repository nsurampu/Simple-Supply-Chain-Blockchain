import hashlib
import datetime
import random
import pickle
from pathlib import Path

import block_script
import chain_script
import user_script
import miners_script

if __name__=="__main__":

    miners = miners_script.Miners()
    miners.add_miner("Alice", 5)
    miners.add_miner("Bob", 3)
    miners.add_miner("Charlie", 9)
    miners.create_miner_network()
    miner_network = miners.miners

    chain_file = Path("chain_file.pickle")
    user_file = Path("user_file.pickle")

    if chain_file.is_file():
        print("Loading blockchain data...")
        with open('chain_file.pickle', 'rb') as handle:
            chains = pickle.load(handle)
    else:
        chains = {}

    if user_file.is_file():
        print("Loading user data...")
        with open('user_file.pickle', 'rb') as handle:
            users = pickle.load(handle)
    else:
        users = {}

    P = 7919   # prime number for ZKP Verification. Smaller prime chose for faster computation
    G = 7      # Generator of chosen prime

    print("\n*****BLOCKCHAIN FOR PHARMA SUPPLY CHAIN*****")
    print("*****Author: Naren Surampudi*****")

    while(True):

        print("\n")
        prompt = input(">>>")
        command = prompt


        # Command for viewing available commands
        if command=='help':
            print("...Available commands: ")
            print("...add block --- Add new block to existing blockchain")
            print("...add genesis block --- Create new blockchain and add genesis block")
            print("...view blockchain --- View a particular blockchain of a product in detail")
            print("...view product blockchains --- View available blockchains for a product")
            print("...view products --- View products for which blockchain exists")
            print("...view user --- View successful transactions of a user")
            print("...view miners --- View all miners assigned for current session")
            print("...add miner --- Add temporary miner to permanent pool of miners")
            print("...verify product --- Verify product using some hash code")
            print("...exit --- Exit from console. All transactions are written to file and loaded on next run")


        # Command for adding new block on existing chain
        elif command=='add block':
            proceed = False
            product_id = input(">>Product ID: ")
            chain_id = input(">>Chain ID: ")
            user_id = input(">>User ID: ")
            location_id = input(">>Location ID: ")
            if product_id in chains.keys():
                if chain_id in chains[product_id].keys():
                    proceed = True

            if proceed:
                block = block_script.Block()
                block.create_block(product_id, location_id, chains[product_id][chain_id].blockchain[-1].current_hash)

                if user_id in users.keys():
                    user = users[user_id]
                    user.generate_y()
                else:
                    user = user_script.User()
                    user.id = int(user_id, 16)
                    user.p = P
                    user.g = G
                    user.generate_y()

                if(chains[product_id][chain_id].verify_transaction(user)):
                    print("...User Verified")
                    user.transactions.append(product_id + " - " + location_id + " - " + block.time)
                    users[user_id] = user
                    print("...Mining Block")
                    start = datetime.datetime.now().timestamp()
                    miner, nonce = block.mine_block(miner_network)
                    end = datetime.datetime.now().timestamp()
                    print("...Block Mined --- Miner: " + miner + " --- Nonce: " + str(nonce) + " --- Duration(seconds): " + str(end-start))
                    chains[product_id][chain_id].add_block(block)
                    print("...Block added to current chain")
                    print("...Chain update complete")
                    print("...Writing blockchain information")
                    with open('chain_file.pickle', 'wb') as handle:
                        pickle.dump(chains, handle, protocol=pickle.HIGHEST_PROTOCOL)
                    print("...Writing user information")
                    with open('user_file.pickle', 'wb') as handle:
                        pickle.dump(users, handle, protocol=pickle.HIGHEST_PROTOCOL)
                else:
                    print("...Unable to verify User")
                    print("...Rolling back any changes")

            else:
                print("...Product ID/Chain ID mismatch")


        # Command for adding genesis block
        elif command=='add genesis block':
            product_id = input(">>Product ID: ")
            chain_id = input(">>Chain ID: ")
            user_id = input(">>User ID: ")
            location_id = input(">>Location ID: ")
            block = block_script.Block()
            block.create_block(product_id, location_id, "0")

            if user_id in users.keys():
                user = users[user_id]
                user.generate_y()
            else:
                user = user_script.User()
                user.id = int(user_id, 16)
                user.p = P
                user.g = G
                user.generate_y()

            print("...Creating Blockchain for Genesis Block")
            chain = chain_script.Chain()

            if(chain.verify_transaction(user)):
                print("...User Verified")
                user.transactions.append("Product: " + product_id + " --- Location: " + location_id + " --- Timestamp: " + block.time)
                users[user_id] = user
                print("...Mining Block")
                start = datetime.datetime.now().timestamp()
                miner, nonce = block.mine_block(miner_network)
                end = datetime.datetime.now().timestamp()
                print("...Block Mined --- Miner: " + miner + " --- Nonce: " + str(nonce) + " --- Duration(seconds): " + str(end-start))
                chain.add_block(block)
                print("...Block added to current chain")
                if product_id not in chains.keys():
                    chains[product_id] = {}
                chains[product_id][chain_id] = chain
                print("...Chain update complete")
                print("...Writing blockchain information")
                with open('chain_file.pickle', 'wb') as handle:
                    pickle.dump(chains, handle, protocol=pickle.HIGHEST_PROTOCOL)
                print("...Writing user information")
                with open('user_file.pickle', 'wb') as handle:
                    pickle.dump(users, handle, protocol=pickle.HIGHEST_PROTOCOL)
            else:
                print("...Unable to verify User")
                print("...Rolling back any changes")


        # Command for viewing product blockchain IDs
        elif command=='view product blockchains':
            product_id = input(">>Product ID: ")
            if product_id in chains.keys():
                for chain in chains[product_id]:
                    print("...Chain ID: " + chain)
            else:
                print("...Product ID mismatch")


        # Command for viewing blockchain
        elif command=='view blockchain':
            product_id = input(">>Product ID: ")
            chain_id = input(">>Chain ID: ")
            valid = False
            if product_id in chains.keys():
                if chain_id in chains[product_id].keys():
                    valid = True
            if valid:
                for block in chains[product_id][chain_id].blockchain:
                    print("...Block --- Location: " + block.location_id + " --- Timestamp: " + block.time)
            else:
                print("...Product ID/Chain ID Mismatch")


        # Command for viewing product IDs
        elif command=='view products':
            for product in chains.keys():
                print("...Product ID: " + product)


        # Command for viewing user transactions
        elif command=='view user':
            user_id = input(">>User ID: ")
            if user_id in users.keys():
                users[user_id].view_user()
            else:
                print("User ID Mismatch")


        # Command for adding temporary miners
        elif command=="add miner":
            name = input(">>Miner Name: ")
            cpu_units = int(input(">>CPU Units: "))
            miners.add_miner(name, cpu_units)
            print("...Miner information added")
            miners.create_miner_network()
            print("...Miner added to network")


        # Command for verifying product
        elif command=="verify product":
            valid = False
            product_id = input(">>Product ID: ")
            product_hash = input(">>Product Hash: ")
            for chain_id in chains[product_id].keys():
                if chains[product_id][chain_id].blockchain[-1].current_hash==product_hash:
                    valid = True
                    break
            if valid:
                print("...Product verified across existing blockchains")
            else:
                print("...Unable to verify product across existing blockchains")


        # Command for viewing miners for current session
        elif command=="view miners":
            for miner in miners.miner_info.keys():
                print("...Miner --- Name: " + miner + " --- CPU Units: " + str(miners.miner_info[miner]))


        # Command for exiting console
        elif command=='exit':
            print("...Writing blockchain information")
            with open('chain_file.pickle', 'wb') as handle:
                pickle.dump(chains, handle, protocol=pickle.HIGHEST_PROTOCOL)
            print("...Writing user information")
            with open('user_file.pickle', 'wb') as handle:
                pickle.dump(users, handle, protocol=pickle.HIGHEST_PROTOCOL)
            print("...Exiting blockchain console")
            break


        else:
            print("...Invalid Command")
