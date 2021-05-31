
from NetMap import ( random )

class Tools:

    @staticmethod
    def choose_random_accounts(followers: list, num_accounts: int) -> list:

        collectedFollowers = []

        while len(collectedFollowers) < num_accounts:

            rand_idx = random.randint(0, len(followers)-1)
            follower = followers[rand_idx]
            collectedFollowers.append(follower)
            followers.remove(follower)

        return collectedFollowers