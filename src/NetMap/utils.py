
from NetMap import ( random )

class Tools:

    """suit of pure functions used to build objects"""

    @staticmethod
    def choose_random_accounts(followers: list, num_accounts: int) -> list:

        """Select Declared Number of Random Followers
           ------------------------------------------
           Parameters:
            - followers (list of strings) handles returned from Twitter API
            - num_accounts (integer) to declare number of accounts to randomly choose
            
            Returns:
            - list of handles (list of strings)
        """

        collectedFollowers = []
        # add and count randomly choosen handles
        while len(collectedFollowers) < num_accounts:
            # set random idx
            rand_idx = random.randint(0, len(followers)-1)
            # choose follower
            follower = followers[rand_idx]
            # add the follower
            # remove it from the list to avoid it being recalled
            collectedFollowers.append(follower)
            followers.remove(follower)

        return collectedFollowers